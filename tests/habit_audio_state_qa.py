from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/');g.evaluate("""async()=>{let m=await import('/habit-shifts.js?v=2');window.scene=m.mountHabit(document.querySelector('#app'),{mode:'magazine',onExit:()=>{},onFinish:()=>{}});document.querySelector('#habitStart').click()}""")
 g.click('#habitMusic');g.wait_for_timeout(70)
 assert g.evaluate("document.querySelector('#habitMusic').getAttribute('aria-pressed')")=='true'
 assert g.evaluate("getComputedStyle(document.querySelector('#habitMusic')).color")
 # AudioContext state must be reflected, not merely a label.
 assert g.evaluate("document.querySelector('#habitMusic').dataset.audioState")=='running'
 print('PASS verified running music state');b.close()
