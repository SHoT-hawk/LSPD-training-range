from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/');g.evaluate("""async()=>{let m=await import('/fps-game.js');window.game=m.mountFPS(document.querySelector('#app'),{exercise:'third',onExit:()=>{},onFinish:()=>{}})}""");g.click('#fpsStart');g.keyboard.press('q');g.keyboard.press('Space');g.keyboard.press('f');g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':2})
 def aim(x,y):
  # Use mouse input rather than mutating camera. Aim at projected target with leaning offset.
  g.evaluate('''({x,y})=>{const s=game.state,a=Math.atan2(y-s.y,x-s.x),turn=a-s.yaw;document.querySelector('#fpsCanvas').dispatchEvent(new MouseEvent('mousemove',{movementX:turn/(.0023*(s.ads?.55:1)),movementY:s.pitch/.0018,bubbles:true}))}''',{'x':x,'y':y})
 for _ in range(3):
  aim(8.5+5.7*__import__('math').cos(-.35),8.5+5.7*__import__('math').sin(-.35));g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0});g.wait_for_timeout(70)
 assert g.evaluate('game.state.hits[0].length')==3
 g.locator('#fpsCanvas').dispatch_event('mouseup',{'button':2});g.keyboard.press('Space');g.keyboard.press('e');aim(8.5+5.7*__import__('math').cos(.35),8.5+5.7*__import__('math').sin(.35));assert g.evaluate('game.state.transferCrossed');g.keyboard.press('Space');g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':2})
 for _ in range(3):
  aim(8.5+5.7*__import__('math').cos(.35),8.5+5.7*__import__('math').sin(.35));g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0});g.wait_for_timeout(70)
 assert g.evaluate('game.state.hits[1].length')==3;g.keyboard.press('e');g.keyboard.press('Space');g.keyboard.press('f');assert g.evaluate('game.state.series')==1;print('PASS third full decision series through mouse/key input');b.close()
