from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();errors=[];g.on('pageerror',lambda e:errors.append(str(e)));g.goto('http://localhost:8080/');g.evaluate("async()=>{let m=await import('/fps-game.js');window.game=m.mountFPS(document.querySelector('#app'),{exercise:'moving'})}");g.click('#fpsStart');y=g.evaluate('game.state.entities[0].y');g.wait_for_timeout(500);assert g.evaluate('game.state.entities[0].y')!=y
 g.evaluate('game.dispose()');g.evaluate("async()=>{let m=await import('/fps-game.js');window.game=m.mountFPS(document.querySelector('#app'),{exercise:'judgement',onFinish:r=>window.result=r})}");g.click('#fpsStart');g.wait_for_timeout(600)
 def aim(x,y):g.evaluate("({x,y})=>{let s=game.state,a=Math.atan2(y-s.y,x-s.x),d=a-s.yaw;document.querySelector('#fpsCanvas').dispatchEvent(new MouseEvent('mousemove',{movementX:d/(.0023*s.sensitivity*(s.ads?.55:1)),movementY:s.pitch/(.0018*s.sensitivity)}))}",{'x':x,'y':y})
 for y in [5.5,8.5,11.5]:
  aim(14.5,8.5);target=7.7 if y==5.5 else 9.3 if y==11.5 else 8.5
  current=g.evaluate('game.state.y');key='d' if current<target else 'a';g.locator('#fpsCanvas').dispatch_event('mouseup',{'button':2});g.evaluate('game.state.yaw=0');g.keyboard.down(key)
  for _ in range(50):
   if abs(g.evaluate('game.state.y')-target)<.1:break
   g.wait_for_timeout(25)
  g.keyboard.up(key);aim(14.5,y);g.wait_for_timeout(100)
 assert g.evaluate('game.state.scan.size')==3
 aim(13.5,8.5);g.keyboard.press('Space');g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':2});g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0});assert g.evaluate('game.state.destroyed')==1;g.wait_for_timeout(2800);assert g.evaluate('game.state.wave')==2
 for y in [5.5,8.5,11.5]:
  aim(14.5,8.5);target=7.7 if y==5.5 else 9.3 if y==11.5 else 8.5
  current=g.evaluate('game.state.y');key='d' if current<target else 'a';g.locator('#fpsCanvas').dispatch_event('mouseup',{'button':2});g.evaluate('game.state.yaw=0');g.keyboard.down(key)
  for _ in range(50):
   if abs(g.evaluate('game.state.y')-target)<.1:break
   g.wait_for_timeout(25)
  g.keyboard.up(key);aim(14.5,y);g.wait_for_timeout(100)
 aim(13.5,10.5);g.wait_for_timeout(2800);assert g.evaluate('game.state.wave')==3
 g.wait_for_timeout(600);aim(13.5,7.35);g.keyboard.press('Space');g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':2});g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0});assert g.evaluate('game.state.entities[0].hp')==1 and g.evaluate('game.state.entities[1].hp')==0;assert not errors,errors;print('PASS moving motion, scanned room, enemy, peaceful no-fire and hostage offset shot');b.close()
