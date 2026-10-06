from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page(viewport={'width':1366,'height':768});g.goto('http://localhost:8080/');g.evaluate("""async()=>{let m=await import('/habit-shifts.js?v=2');window.scene=m.mountHabit(document.querySelector('#app'),{mode:'magazine',seed:0,onExit:()=>{},onFinish:()=>{}});document.querySelector('#habitStart').click()}""")
 box=g.locator('#habitCanvas').bounding_box();g.mouse.click(box['x']+box['width']*6.5/27,box['y']+box['height']*3.5/17);assert g.evaluate('scene.state.shots')==1
 assert g.evaluate('scene.state.tracer')>0,'shot needs visible path feedback'
 print('PASS visible tracer');b.close()
