from pathlib import Path
from playwright.sync_api import sync_playwright
src=Path('D:/Работа/LSPD/app.js').read_text(encoding='utf8')+'\nwindow.qa={state,startRun,renderDashboard,renderShiftBoards,saveRunResult};'
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.route('**/app.js*',lambda r:r.fulfill(body=src,content_type='application/javascript'));g.goto('http://localhost:8080/');g.click('#create');g.fill('#name','Variant');g.fill('#password','1234');g.fill('#password2','1234');g.click('button.primary');g.click('#start');g.fill('#character','QA');g.click('button.primary')
 for mode in ['static','moving']:
  for ex in ['attention','pace','memory']:
   g.evaluate("([ex,mode])=>qa.saveRunResult({reason:'scenarios_done',motion:mode,duration:22,points:300,destroyed:0,resign:0,killed:0,completed:3,mistakes:0,streak:3,arrests:2,shots:0,hitCount:0,misses:0},ex)",[ex,mode]);g.wait_for_selector('#saveResult');g.click('#again');g.select_option('#personalShift',ex);g.select_option('#boardMotion',mode);assert g.locator('tbody tr').count()==1
 assert g.evaluate('qa.state.profiles[0].personal.length')==6
 g.click('#shared');g.select_option('#boardShift','memory');g.select_option('#boardMotion','moving');assert g.locator('tbody tr').count()==1
 g.reload();assert g.evaluate("JSON.parse(localStorage.getItem('lspd-training-v1')).profiles[0].personal.length")==6;print('PASS signed new drill results persist, static/moving boards never mix')
 b.close()
