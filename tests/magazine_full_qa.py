from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/');g.evaluate('''async()=>{window.out=[];window.sim=(await import('/habit-shifts.js')).mountHabit(document.querySelector('#app'),{mode:'magazine',seed:0,onExit:()=>{},onFinish:r=>out.push(r)});document.querySelector('#habitStart').click()}''')
 for round in range(8):
  g.keyboard.down('r');g.wait_for_timeout(610);g.keyboard.up('r')
  ammo=g.evaluate('sim.state.ammo');needed=g.evaluate('sim.state.required')
  if ammo<needed:
   g.keyboard.down('r');g.wait_for_timeout(80);g.keyboard.up('r');g.wait_for_timeout(1500)
   g.keyboard.down('r');g.wait_for_timeout(610);g.keyboard.up('r')
  g.keyboard.down('w');g.wait_for_timeout(65);g.keyboard.up('w')
  for _ in range(needed):g.evaluate("document.querySelector('#habitCanvas').dispatchEvent(new MouseEvent('mousedown',{button:0}))")
 assert len(g.evaluate('out'))==1 and g.evaluate('out[0].completed')==8,g.evaluate('out')
 print('PASS eight magazine decisions with R inspect/reload/recheck, no unnecessary reloads')
 b.close()
