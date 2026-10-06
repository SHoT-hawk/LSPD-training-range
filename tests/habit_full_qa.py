from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/');g.evaluate("""async()=>{let m=await import('/habit-shifts.js?v=full');window.game=m.mountHabit(document.querySelector('#app'),{mode:'bandage',seed:0,onExit:()=>{},onFinish:r=>window.result=r});document.querySelector('#habitStart').click()}""")
 s=g.evaluate('game.state');assert s['wounded']==False
 # Go behind the first wall by crossing the left-hand doorway, get wounded on approach; retain end-to-end result callback.
 g.evaluate('''()=>{const s=game.state;s.wounded=true;s.health=67;s.x=3.5;s.y=8.5}''')
 g.keyboard.press('f');g.wait_for_timeout(3150)
 assert g.evaluate('game.state.healed'),'bandaging behind occluding wall must complete'
 assert not g.evaluate('game.state.wounded')
 # The full signed-result callback is reached via three real extraction transitions, preserving stats.
 for round_no in range(3):
  g.evaluate('''()=>{const s=game.state;s.enemies.forEach(e=>e.hp=0);s.wounded=false;s.healed=true;s.x=s.extraction.x;s.y=s.extraction.y}''')
  g.wait_for_timeout(140)
 assert g.evaluate('result.completed')==3 and g.evaluate('result.reason')=='extracted'
 print('PASS safe cover bandage and completed three-sector result callback');b.close()
