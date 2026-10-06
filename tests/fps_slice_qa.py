from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page(viewport={'width':1280,'height':800});errors=[];g.on('pageerror',lambda e:errors.append(str(e)));g.goto('http://localhost:8080/')
 g.evaluate("""async()=>{let m=await import('/fps-game.js');window.game=m.mountFPS(document.querySelector('#app'),{exercise:'bandage',seed:0,onExit:()=>{},onFinish:()=>{}})}""")
 g.click('#fpsStart');before=g.evaluate('game.state.y');g.keyboard.down('d');g.wait_for_timeout(220);g.keyboard.up('d');assert g.evaluate('game.state.y')!=before
 g.keyboard.press('Space');ammo=g.evaluate('game.state.ammo');g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0});g.wait_for_timeout(100);assert g.evaluate('game.state.ammo')==ammo-1
 assert g.evaluate('game.state.shots')==1 and not errors;print('PASS FPS movement and actual fired round');g.screenshot(path='D:/Работа/LSPD/tests/fps-slice.png');b.close()
