from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/')
 def mount(mode,seed):g.evaluate('''async({mode,seed})=>{if(window.sim)sim.dispose();window.out=[];window.sim=(await import('/habit-shifts.js')).mountHabit(document.querySelector('#app'),{mode,seed,onExit:()=>{},onFinish:r=>out.push(r)});document.querySelector('#habitStart').click()}''',{'mode':mode,'seed':seed})
 def key(k):g.keyboard.press(k)
 mount('bandage',2)
 g.evaluate('sim.state.x=sim.state.coverX');key('f');assert g.evaluate('sim.state.bandageSafe');g.evaluate('sim.state.bandaging=.02');g.wait_for_timeout(90);assert g.evaluate('sim.state.completed')==1
 mount('magazine',1)
 g.keyboard.down('r');g.wait_for_timeout(680);g.keyboard.up('r');assert g.evaluate('sim.state.inspect');assert g.locator('#magazineGraphic').is_visible();assert g.locator('#magEstimate').inner_text()=='Почти пусто'
 key('r');g.evaluate('sim.state.reloading=.02');g.wait_for_timeout(90);assert not g.evaluate('sim.state.inspect')
 g.keyboard.down('r');g.wait_for_timeout(680);g.keyboard.up('r');assert g.evaluate('sim.state.inspect');g.keyboard.down('w');g.wait_for_timeout(55);g.keyboard.up('w');assert g.evaluate('sim.state.exposed');need=g.evaluate('sim.state.required')
 for _ in range(need):g.evaluate("document.querySelector('#habitCanvas').dispatchEvent(new MouseEvent('mousedown',{button:0}))")
 assert g.evaluate('sim.state.completed')==1
 mount('magazine',2);g.keyboard.down('r');g.wait_for_timeout(680);g.keyboard.up('r');assert g.evaluate('sim.state.ammo')>=g.evaluate('sim.state.required');g.keyboard.down('w');g.wait_for_timeout(60);g.keyboard.up('w');assert g.evaluate('sim.state.exposed');g.evaluate('sim.state.exposure=.02');g.wait_for_timeout(95);assert g.evaluate('sim.state.mistakes')==1
 print('PASS safe cover finish, reload requires recheck, sufficient and deficient decisions, exposed timeout')
 b.close()
