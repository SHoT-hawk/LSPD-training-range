from playwright.sync_api import sync_playwright
from pathlib import Path
src=Path('D:/Работа/LSPD/app.js').read_text(encoding='utf8')+'\nwindow.qa={state,startRun,renderDashboard};'
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();errors=[];g.on('pageerror',lambda e:errors.append(str(e)));g.route('**/app.js*',lambda r:r.fulfill(body=src,content_type='application/javascript'));g.goto('http://localhost:8080/');g.click('#create');g.fill('#name','FPS-QA');g.fill('#password','pass1234');g.fill('#password2','pass1234');g.click('button.primary');g.click('#start');g.fill('#character','Officer');g.click('button.primary');g.click('#back')
 for ex in ['circle','front','third','bandage','magazine']:
  g.evaluate('ex=>{qa.state.exercise=ex;qa.startRun()}',ex);g.click('#fpsStart');g.evaluate('qa.state.scene.state.elapsed=300');g.wait_for_selector('#again');rec=g.evaluate('qa.state.profiles[0].personal.at(-1)');assert rec['exercise']==ex and rec['signature'];assert 'shots' in rec and rec['gameVersion']=='fps-1';g.click('#again');g.get_by_role('button',name='Таблицы смен').click();g.select_option('#boardShift',ex);assert 'Officer' in g.inner_text('table');g.evaluate('qa.renderDashboard()')
 assert g.evaluate('qa.state.profiles[0].career.days')==5 and not errors;print('PASS five production runs, signed FPS metrics and per-shift boards');b.close()
