from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/');g.evaluate("""async()=>{let m=await import('/habit-shifts.js?v=2');window.game=m.mountHabit(document.querySelector('#app'),{mode:'bandage',onExit:()=>{},onFinish:()=>{}});document.querySelector('#habitStart').click();let s=game.state;s.x=5.5;s.y=4.5;s.wounded=true;s.enemies=[{x:5.5,y:3.5,hp:2,clock:8}]}""")
 assert g.inner_text('#habitStatus').startswith('◆ ПОД ОГНЁМ'),'adjacent crate off firing line is not cover'
 g.keyboard.press('f');g.wait_for_timeout(3500)
 assert g.evaluate('game.state.wounded') and not g.evaluate('game.state.healed'),'open-line bandage cannot heal'
 print('PASS cover requires actual blocked line of sight');b.close()
