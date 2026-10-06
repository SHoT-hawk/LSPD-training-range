from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/');g.evaluate("async()=>{let m=await import('/fps-game.js');window.game=m.mountFPS(document.querySelector('#app'),{exercise:'moving'})}");g.click('#fpsStart');g.keyboard.press('Space');g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':2})
 for _ in range(2):
  for side in ['left','right']:
   for n in range(3):
    g.evaluate("side=>{const s=game.state,e=s.entities.find(e=>e.side===side),a=Math.atan2(e.y-s.y,e.x-s.x),d=Math.atan2(Math.sin(a-s.yaw),Math.cos(a-s.yaw));document.querySelector('#fpsCanvas').dispatchEvent(new MouseEvent('mousemove',{movementX:d/(.0023*s.sensitivity*.55),movementY:s.pitch/(.0018*s.sensitivity)}))}",side);g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0});g.wait_for_timeout(80)
  g.wait_for_timeout(1450)
 assert g.evaluate('game.state.destroyed')==4 and g.evaluate('game.state.wave')==3;print('PASS moving targets two fired series and respawn');b.close()
