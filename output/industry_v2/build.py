#!/usr/bin/env python3
"""Rebuild ONERGY's editable draft from the 22 hand-authored SVG source pages.
Uses the existing minimal runtime; does not install anything or call APIs.
Usage: /workspace/shared/ppt-master-minimal/bin/python output/build_onergy.py --stage split|finalize|export
Re-exporting an existing deliverable requires --replace.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROJECT = REPO / 'projects/onergy_europe_industry_v2_ppt169_20261028'
SCRIPTS = REPO / '.agents/skills/ppt-master/scripts'
TARGET = REPO / 'output/industry_v2/onergy_europe_om_industry_v2.pptx'

def run(script, *args):
    subprocess.run([sys.executable, str(SCRIPTS / script), str(PROJECT), *map(str,args)],
                   cwd=REPO, env={**os.environ, 'PYTHONDONTWRITEBYTECODE':'1'}, check=True)

def walk_shapes(shapes):
    for shape in shapes:
        yield shape
        if hasattr(shape, "shapes"):
            yield from walk_shapes(shape.shapes)

def fix_typefaces():
    # The upstream font classifier does not recognize "Noto Sans CJK SC" as
    # East Asian. Set all DrawingML text font slots explicitly on the OUTPUT.
    # No skill source files are changed.
    from pptx import Presentation
    from pptx.enum.text import MSO_AUTO_SIZE, PP_ALIGN
    from PIL import ImageFont
    from pptx.oxml.xmlchemy import OxmlElement
    deck = Presentation(TARGET)
    for slide in deck.slides:
        for shape in walk_shapes(slide.shapes):
            if not shape.has_text_frame:
                continue
            shape.text_frame.word_wrap = False
            shape.text_frame.auto_size = MSO_AUTO_SIZE.NONE
            measured = 0
            for paragraph in shape.text_frame.paragraphs:
                total = 0
                for run_ in paragraph.runs:
                    size_px = (run_.font.size.pt if run_.font.size else 16.5) * 96 / 72
                    fontfile = '/usr/share/fonts/opentype/noto/NotoSansCJK-' + ('Bold' if run_.font.bold else 'Regular') + '.ttc'
                    font = ImageFont.truetype(fontfile, round(size_px * 4), index=2)
                    total += font.getlength(run_.text) / 4
                measured = max(measured, total)
            required = round((measured * 1.12 + 18) * 9525)
            if required > shape.width:
                old_right = shape.left + shape.width
                old_center = shape.left + shape.width // 2
                alignment = shape.text_frame.paragraphs[0].alignment
                shape.width = required
                if alignment == PP_ALIGN.RIGHT:
                    shape.left = old_right - required
                elif alignment == PP_ALIGN.CENTER:
                    shape.left = old_center - required // 2
            for paragraph in shape.text_frame.paragraphs:
                for run_ in paragraph.runs:
                    run_.font.name = 'Noto Sans CJK SC'
                    prop = run_._r.get_or_add_rPr()
                    for tag in ('a:ea','a:cs'):
                        element = prop.find('{http://schemas.openxmlformats.org/drawingml/2006/main}' + tag[2:])
                        if element is None:
                            element = OxmlElement(tag); prop.append(element)
                        element.set('typeface','Noto Sans CJK SC')
    deck.save(TARGET)
    loaded = Presentation(TARGET)
    assert len(loaded.slides) == 22
    assert all(any(sh.has_text_frame and sh.text.strip() for sh in walk_shapes(sl.shapes)) for sl in loaded.slides)
    print('Validated: 22 slides with native editable text; explicit Noto Sans CJK SC font slots.')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage',choices=['check','split','finalize','export'],required=True)
    parser.add_argument('--replace',action='store_true')
    args=parser.parse_args()
    if args.stage=='check': run('svg_quality_checker.py')
    elif args.stage=='split': run('total_md_split.py')
    elif args.stage=='finalize': run('finalize_svg.py')
    else:
        if TARGET.exists() and not args.replace: raise SystemExit('Output exists; use --replace to rebuild intentionally.')
        run('svg_to_pptx.py','-o',TARGET,'--workers','2')
        fix_typefaces()
if __name__=='__main__': main()
