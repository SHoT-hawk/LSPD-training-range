from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/');g.evaluate("async()=>{let m=await import('/fps-game.js');window.game=m.mountFPS(document.querySelector('#app'),{exercise:'third'})}");g.click('#fpsStart');g.keyboard.press('q');g.keyboard.press('Space');g.keyboard.press('f');g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':2})
 def aim(side):g.evaluate("side=>{const s=game.state,e=s.entities.find(e=>e.side===side),a=Math.atan2(e.y-s.y,e.x-s.x),d=Math.atan2(Math.sin(a-s.yaw),Math.cos(a-s.yaw));document.querySelector('#fpsCanvas').dispatchEvent(new MouseEvent('mousemove',{movementX:d/(.0023*s.sensitivity*(s.ads?.55:1)),movementY:s.pitch/(.0018*s.sensitivity)}))}",side)
 for n in range(3):aim('left');g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0});g.wait_for_timeout(80)
 g.keyboard.press('Space');aim('right');g.keyboard.press('e');g.keyboard.press('Space');g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':2})
 for n in range(3):aim('right');g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0});g.wait_for_timeout(80)
 g.wait_for_timeout(1450);assert g.evaluate('game.state.series')==1 and g.evaluate('game.state.wave')==2;assert all(e['hp']==3 for e in g.evaluate('game.state.entities') if e['kind']=='target');print('PASS third actual 6 shots auto next pair without extra finishing keys');b.close()
