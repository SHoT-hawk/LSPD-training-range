from playwright.sync_api import sync_playwright
import math
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/')
 for exercise in ['front','circle']:
  g.evaluate("""async ex=>{let m=await import('/fps-game.js');window.game=m.mountFPS(document.querySelector('#app'),{exercise:ex,onExit:()=>{},onFinish:()=>{}})}""",exercise);g.click('#fpsStart')
  def aim(side):
   e=g.evaluate("side=>game.state.entities.find(e=>e.side===side)",side)
   g.evaluate('''({x,y})=>{const s=game.state,a=Math.atan2(y-s.y,x-s.x),t=Math.atan2(Math.sin(a-s.yaw),Math.cos(a-s.yaw));document.querySelector('#fpsCanvas').dispatchEvent(new MouseEvent('mousemove',{movementX:t/(.0023*(s.ads?.55:1)),movementY:s.pitch/.0018,bubbles:true}))}''',e)
  aim('right');g.keyboard.press('Space');g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':2});g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0})
  if exercise=='front':assert g.evaluate('game.state.orderErrors')==1 and g.evaluate('game.state.entities[1].hp')==3
  else:assert g.evaluate('game.state.entities[1].hp')==2 and g.evaluate('game.state.orderErrors')==0
  for side in ['left','right']:
   if not g.evaluate('game.state.raised'):g.keyboard.press('Space')
   aim(side);g.keyboard.press('Space');g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':2})
   for _ in range(3):aim(side);g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0})
  assert g.evaluate('game.state.destroyed')==2;g.wait_for_timeout(1350);assert g.evaluate('game.state.wave')==2;print('PASS',exercise,'pair and next wave');g.evaluate('game.dispose()')
 b.close()
