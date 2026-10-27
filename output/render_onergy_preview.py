#!/usr/bin/env python3
"""Render through PPT Master's existing visual_review.py using system Chromium.
Requires the existing live preview server on port 15051; installs nothing.
"""
import runpy
import sys
from pathlib import Path
from playwright.sync_api import BrowserType
repo=Path(__file__).resolve().parent.parent
original_launch=BrowserType.launch
def launch_system_browser(self,*args,**kwargs):
    kwargs.setdefault('executable_path','/usr/bin/chromium')
    return original_launch(self,*args,**kwargs)
BrowserType.launch=launch_system_browser
script=repo/'.agents/skills/ppt-master/scripts/visual_review.py'
sys.argv=[str(script),str(repo/'projects/onergy_europe_om_ppt169_20261027'),'--server-url','http://127.0.0.1:15051']
runpy.run_path(str(script),run_name='__main__')
