from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/')
 g.evaluate("""async()=>{let m=await import('/habit-shifts.js?v=2');window.game=m.mountHabit(document.querySelector('#app'),{mode:'magazine',seed:0,onExit:()=>{},onFinish:()=>{}});document.querySelector('#habitStart').click()}""")
 assert g.evaluate('game.state.ammo')>=2,'first firefight must allow at least one enemy takedown before refill'
 g.click('#habitMusic');assert g.inner_text('#habitMusic').count('вкл.')==1
 assert g.evaluate("document.querySelector('#habitMusic').getAttribute('aria-pressed')")=='true','music control must reflect actual playing state'
 print('PASS default first combat ammo and auditable music state');b.close()
