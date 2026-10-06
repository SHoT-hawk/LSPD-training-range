from playwright.sync_api import sync_playwright
from pathlib import Path
src=Path('D:/Работа/LSPD/app.js').read_text(encoding='utf-8')+'\nwindow.boardQA={state,renderDashboard,renderShared,saveRunResult};'
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();err=[];g.on('pageerror',lambda e:err.append(str(e)))
 g.route('**/app.js*',lambda route:route.fulfill(body=src,content_type='application/javascript'))
 g.goto('http://localhost:8080/');g.click('#create');g.fill('#name','board-test');g.fill('#password','pass1234');g.fill('#password2','pass1234');g.click('button.primary');g.click('#start');g.fill('#character','Tester');g.click('button.primary');g.click('#back')
 # Regression: twelve first-shift scores must not discard the signed fourth-shift result.
 g.evaluate("""()=>{const p=boardQA.state.profiles[0];p.personal=[{id:'fourth',player:p.name,character:'Tester',exercise:'bandage',rating:1,targets:1,date:new Date().toISOString()}];for(let i=0;i<12;i++)p.personal.push({id:'circle'+i,player:p.name,character:'Tester',exercise:'circle',rating:100+i,targets:1,date:new Date().toISOString()});boardQA.renderDashboard()}""")
 assert g.get_by_role('button',name='Таблицы смен').count()==1,'Missing per-shift leaderboards'
 g.get_by_role('button',name='Таблицы смен').click()
 g.select_option('#boardShift','bandage');assert 'Tester' in g.inner_text('table') and 'Четвёртая' in g.inner_text('table')
 assert 'Успешно' in g.inner_text('table thead') and 'Ошибки' in g.inner_text('table thead')
 g.select_option('#boardShift','circle');assert 'Четвёртая' not in g.inner_text('table')
 assert g.locator('table tbody tr').count()==11
 g.select_option('#boardShift','magazine');assert g.locator('table').count()==0,'Fifth table should be empty before any fifth-shift result'
 g.select_option('#boardShift','bandage')
 # Saving any new score must not truncate historic records for other shifts.
 g.evaluate("boardQA.saveRunResult({duration:50,points:120,completed:2,mistakes:1,streak:1,destroyed:2,resign:0,killed:0,reason:'scenarios_done'},'bandage')")
 g.wait_for_selector('#again');assert g.evaluate('boardQA.state.profiles[0].personal.length')==14
 assert g.evaluate("JSON.parse(localStorage.getItem('lspd-training-v1')).profiles[0].personal.length")==14
 g.click('#again');g.get_by_role('button',name='Таблицы смен').click();g.select_option('#boardShift','bandage');assert 'Tester' in g.inner_text('table') and g.locator('table tbody tr').count()==2
 assert not err,err
 print('PASS fourth signed result in per-shift table and separate filters')
 b.close()
