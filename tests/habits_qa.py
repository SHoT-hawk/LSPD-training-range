from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':1280,'height':800});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://localhost:8080/')
 page.evaluate('''async()=>{let {mountHabit}=await import('/habit-shifts.js');window.results=[];window.scene=mountHabit(document.querySelector('#app'),{mode:'bandage',onExit:()=>{},onFinish:r=>results.push(r),seed:2});document.querySelector('#habitStart').click()}''')
 def key(k,kind='keydown'):page.evaluate("([k,kind])=>window.dispatchEvent(new KeyboardEvent(kind,{code:k,bubbles:true}))",[k,kind])
 def state():return page.evaluate('scene.state')
 # Bandaging is not instant: walking remains possible, shooting remains blocked.
 key('KeyF');assert state()['bandaging']>0 and not state()['cover'],'F should start wrapping in the open'
 key('KeyD');page.wait_for_timeout(120);key('KeyD','keyup');assert state()['x']!=state()['startX'],'movement allowed during wrapping'
 shots=state()['shots'];page.evaluate("document.querySelector('#habitCanvas').dispatchEvent(new MouseEvent('mousedown',{button:0}))");assert state()['shots']==shots
 page.evaluate('scene.state.bandaging=.02');page.wait_for_timeout(100);assert state()['mistakes']>=1 and state()['completed']==0,'open bandaging fails with debrief'
 page.evaluate('scene.state.x=scene.state.coverX;scene.state.bandaging=0');key('KeyF');assert state()['bandaging']>0
 page.evaluate('scene.state.bandaging=.02');page.wait_for_timeout(100);assert state()['completed']==1,'bandage behind cover completes'
 page.evaluate('scene.dispose()')
 # Holding R reveals a graphical approximate magazine; a tap replaces it.
 page.evaluate('''async()=>{let {mountHabit}=await import('/habit-shifts.js');window.scene=mountHabit(document.querySelector('#app'),{mode:'magazine',onExit:()=>{},onFinish:r=>results.push(r),seed:1});document.querySelector('#habitStart').click()}''')
 initial=state()['ammo'];key('KeyR');page.wait_for_timeout(730);assert state()['inspect'] and state()['ammo']==initial,'holding R must inspect without replacing'
 assert page.locator('#magazineGraphic').is_visible();key('KeyR','keyup');assert state()['ammo']==initial
 # A short tap replaces the magazine, but only after the reload animation.
 key('KeyR');page.wait_for_timeout(90);key('KeyR','keyup');assert state()['reloading']>0
 page.evaluate('scene.state.reloading=.02');page.wait_for_timeout(100);assert state()['ammo']>initial
 # Exposure without a check should count as a decision mistake on the next scenario.
 page.evaluate('scene.nextScenario()');key('KeyW');page.wait_for_timeout(170);assert state()['mistakes']>=1
 assert not errors,errors
 print('PASS bandage cover, motion/blocked fire; hold R inspect vs tap reload; uninspected exit')
 b.close()
