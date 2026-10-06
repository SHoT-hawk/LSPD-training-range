from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/');g.evaluate("async()=>{let m=await import('/fps-game.js');window.game=m.mountFPS(document.querySelector('#app'),{exercise:'bandage'})}");g.click('#fpsStart')
 g.locator('#fpsCanvas').dispatch_event('mousemove',{'movementX':0,'movementY':100});assert g.evaluate('game.state.pitch')<0,'mouse down must move horizon up: look down'
 g.locator('#fpsCanvas').dispatch_event('mousemove',{'movementX':0,'movementY':-200});assert g.evaluate('game.state.pitch')>0,'mouse up must move horizon down: look up'
 g.keyboard.press('Space');before=g.evaluate('game.state.pitch');g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0});assert g.evaluate('game.state.pitch')>before,'recoil must lift view';print('PASS normal vertical mouse and upward recoil');b.close()
