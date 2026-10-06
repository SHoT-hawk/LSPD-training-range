from pathlib import Path
from playwright.sync_api import sync_playwright
src=Path('D:/Работа/LSPD/app.js').read_text(encoding='utf8')+'\nwindow.qa={state,startRun,renderDashboard,renderShiftBoards};'
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.route('**/app.js*',lambda r:r.fulfill(body=src,content_type='application/javascript'));g.goto('http://localhost:8080/');g.click('#create');g.fill('#name','Seven');g.fill('#password','1234');g.fill('#password2','1234');g.click('button.primary');g.click('#start');g.fill('#character','QA');g.click('button.primary')
 for ex in ['circle','front','third','bandage','magazine','moving','judgement']:
  g.select_option('#shiftSelect',ex);g.click('#enterRange');g.click('#fpsStart');g.evaluate('qa.state.scene.state.elapsed=241');g.wait_for_selector('#saveResult');assert g.evaluate('qa.state.profiles[0].personal.at(-1).exercise')==ex;g.click('#again');g.select_option('#personalShift',ex);assert g.locator('tbody tr').count()==1;g.click('#start')
 g.click('#back');g.evaluate("()=>{let p=qa.state.profiles[0];for(let i=0;i<15;i++)p.personal.push({...p.personal[0],id:'extra'+i,rating:99999});qa.renderShiftBoards('moving')}");assert g.locator('tbody tr').count()==1;assert g.locator('tbody').inner_text().find('Шестая')>=0
 assert g.evaluate('qa.state.profiles[0].personal.filter(r=>r.signature).length')>=7;g.select_option('#boardShift','judgement');assert g.locator('tbody tr').count()==1;print('PASS seven saved signed runs and isolated personal/shared boards despite >11 other results');b.close()
