from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page(viewport={'width':1200,'height':800});g.goto('http://localhost:8080/');g.evaluate("""async()=>{let m=await import('/habit-shifts.js?v=aim');window.game=m.mountHabit(document.querySelector('#app'),{mode:'magazine',onExit:()=>{},onFinish:r=>window.result=r});document.querySelector('#habitStart').click()}""")
 def target(x,y):
  rect=g.locator('#habitCanvas').bounding_box();g.mouse.move(rect['x']+rect['width']*x/27,rect['y']+rect['height']*y/17);g.mouse.click(rect['x']+rect['width']*x/27,rect['y']+rect['height']*y/17)
 hp=g.evaluate('game.state.enemies[0].hp');target(6.5,3.5);assert g.evaluate('game.state.enemies[0].hp')==hp-1,'aimed shot must hit'
 hp=g.evaluate('game.state.enemies[0].hp');target(3.5,6.5);assert g.evaluate('game.state.enemies[0].hp')==hp,'off-target shot must miss'
 print('PASS spatial aimed shot and off-target miss');b.close()
