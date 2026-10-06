from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page(viewport={'width':1366,'height':768});g.goto('http://localhost:8080/');g.evaluate("""async()=>{let m=await import('/habit-shifts.js?v=2');window.scene=m.mountHabit(document.querySelector('#app'),{mode:'magazine',seed:0,onExit:()=>{},onFinish:()=>{}});document.querySelector('#habitStart').click()}""");g.wait_for_timeout(100)
 box=g.locator('#habitCanvas').bounding_box()
 assert g.locator('#habitHint').count()==1,'distinct actionable prompt should exist outside arena'
 assert g.locator('.habit-brief').bounding_box()['width']<=box['width']*.43,'instruction overlay covers too much of combat floor'
 print('PASS unobstructed training HUD');b.close()
