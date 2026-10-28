import json
from pathlib import Path
from playwright.sync_api import sync_playwright
REPO=Path(__file__).resolve().parents[2]
r=REPO/'projects/onergy_europe_industry_v2_ppt169_20261028'
records=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium');page=b.new_page(viewport={'width':1280,'height':720})
 for svg in sorted((r/'svg_output').glob('*.svg')):
  page.goto('http://127.0.0.1:15052/')
  page.evaluate('''async name=>{let d=await(await fetch('/api/slide/'+name)).json();document.body.innerHTML=d.content;document.body.style.margin='0';await document.fonts.ready;}''',svg.name)
  rows=page.evaluate('''()=>Array.from(document.querySelectorAll('svg text')).map(e=>{let b=e.getBBox();return {text:e.textContent,x:b.x,y:b.y,w:b.width,h:b.height};})''')
  assert any(x['text']=='历橙 你的能源历程伙伴' for x in rows)
  assert page.locator('svg image').first.get_attribute('x')=='1104'
  issues=[]
  for a in rows:
   if a['x']<-.5 or a['y']<-.5 or a['x']+a['w']>1280.5 or a['y']+a['h']>720.5:issues.append({'type':'out_of_bounds','text':a['text']})
  for i,a in enumerate(rows):
   for c in rows[i+1:]:
    if min(a['x']+a['w'],c['x']+c['w'])-max(a['x'],c['x'])>1 and min(a['y']+a['h'],c['y']+c['h'])-max(a['y'],c['y'])>1:issues.append({'type':'overlap','a':a['text'],'b':c['text']})
  records.append({'page':svg.name,'text_count':len(rows),'issues':issues})
 b.close()
(r/'.review/browser_geometry.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
print(json.dumps([x for x in records if x['issues']],ensure_ascii=False,indent=2))
print('Checked',len(records),'pages; mandatory branding present on every page.')
assert not any(x['issues'] for x in records)
