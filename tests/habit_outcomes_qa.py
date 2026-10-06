from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/')
 def start(mode):
  g.evaluate('''async mode=>{window.game?.dispose();window.result=null;let m=await import('/habit-shifts.js?v=outcome');window.game=m.mountHabit(document.querySelector('#app'),{mode,seed:0,onExit:()=>{},onFinish:r=>window.result=r});document.querySelector('#habitStart').click()}''',mode)
 start('bandage');g.evaluate('''()=>{const s=game.state;s.enemies.forEach(e=>e.hp=0);s.x=s.extraction.x;s.y=s.extraction.y;s.tookDamage=true}''');g.wait_for_timeout(120);assert g.evaluate('game.state.completed')==0,'Cannot skip care after being wounded'
 start('bandage');g.evaluate('''()=>{const s=game.state;s.enemies.forEach(e=>e.hp=0);s.x=s.extraction.x;s.y=s.extraction.y;s.healed=true;s.wounded=true;s.tookDamage=true}''');g.wait_for_timeout(120);assert g.evaluate('game.state.completed')==0,'Cannot finish while wounded'
 start('magazine');g.evaluate('''()=>{const s=game.state;s.enemies.forEach(e=>e.hp=0);s.required=0;s.x=s.extraction.x;s.y=s.extraction.y;s.inspect=true}''');g.wait_for_timeout(120);assert g.evaluate('game.state.completed')==0,'Cannot score fifth by skipping inspection before contact'
 start('magazine');g.evaluate('''()=>{const s=game.state;s.shots=3;s.round=2;game.nextScenario()}''');g.keyboard.down('r');g.wait_for_timeout(650);g.keyboard.up('r');assert g.evaluate('game.state.inspectedBeforeContact'),'second sector must allow fresh pre-contact inspection'
 print('PASS wounded-care gates and new-sector pre-contact check');b.close()
