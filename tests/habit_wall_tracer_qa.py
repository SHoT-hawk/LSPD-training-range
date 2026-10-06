from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page(viewport={'width':1366,'height':768});g.goto('http://localhost:8080/');g.evaluate("""async()=>{let m=await import('/habit-shifts.js?v=2');window.scene=m.mountHabit(document.querySelector('#app'),{mode:'magazine',seed:0,onExit:()=>{},onFinish:()=>{}});document.querySelector('#habitStart').click()}""");g.wait_for_timeout(100)
 box=g.locator('#habitCanvas').bounding_box();x=box['x']+box['width']*6.5/27;y=box['y']+box['height']*3.5/17
 # Shot into solid wall must not damage an enemy behind it.
 g.evaluate("scene.state.enemies=[{x:10.5,y:4.5,hp:2,clock:5}]")
 g.mouse.click(box['x']+box['width']*10.5/27,box['y']+box['height']*4.5/17)
 assert g.evaluate('scene.state.enemies[0].hp')==2
 assert g.evaluate('scene.state.tracerEnd.x')<9.1,'tracer must stop at the wall, not render through masonry'
 print('PASS shot collision and visible path agree');b.close()
