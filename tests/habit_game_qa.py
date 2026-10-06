from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':1200,'height':800});err=[];page.on('pageerror',lambda e:err.append(str(e)))
 page.goto('http://localhost:8080/')
 def mount(mode):
  page.evaluate('''async mode=>{window.lastResult=null;window.game?.dispose();let m=await import('/habit-shifts.js?v=test-game');window.game=m.mountHabit(document.querySelector('#app'),{mode,seed:0,onExit:()=>{},onFinish:r=>window.lastResult=r});document.querySelector('#habitStart').click()}''',mode)
 mount('bandage')
 s=page.evaluate('game.state');assert 'maze' in s and len(s['maze'])>=10,'Need navigable rooms, not one-dimensional cover'
 assert s['wounded']==False,'wound must be caused by incoming fire'
 assert 'KeyW' in page.evaluate("document.querySelector('#habitInstruction').textContent") or 'WASD' in page.evaluate("document.querySelector('#habitInstruction').textContent")
 page.evaluate('game.state.enemyClock=0.01');page.wait_for_timeout(1700)
 assert page.evaluate('game.state.wounded'),'enemy must cause injury'
 assert page.evaluate('game.state.health')<100
 before=page.evaluate('game.state.shots');page.keyboard.press('f');assert page.evaluate('game.state.bandaging')>0
 page.locator('#habitCanvas').dispatch_event('mousedown',{'button':0,'clientX':600,'clientY':400});assert page.evaluate('game.state.shots')==before,'shooting blocked during bandage'
 x=page.evaluate('game.state.x');page.keyboard.down('a');page.wait_for_timeout(200);page.keyboard.up('a');assert page.evaluate('game.state.x')!=x,'movement allowed while bandaging'
 assert not err,err
 mount('magazine');assert page.evaluate('game.state.ammo')<30
 page.keyboard.down('r');page.wait_for_timeout(680);assert page.locator('#magazineGraphic').is_visible();page.keyboard.up('r')
 assert page.evaluate('game.state.reloading')==0,'holding R cannot reload'
 page.keyboard.press('r');assert page.evaluate('game.state.reloading')>0,'short R reloads'
 assert 'ammo' not in page.inner_text('#habitStats').lower() and 'патронов:' not in page.inner_text('#habitStatus').lower(),'no exact ammo HUD'
 assert not err,err
 print('PASS maze, incoming wound, moving/blocked fire while bandaging, graphic hold R vs tap R')
 b.close()
