from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path('D:/Работа/LSPD')
with sync_playwright() as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1280,'height':800});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 src=(R/'app.js').read_text(encoding='utf-8')+'\nwindow.debug={state,startRun,renderTutorial,renderDashboard};'
 page.route('**/app.js*',lambda r:r.fulfill(body=src,content_type='application/javascript'))
 page.goto('http://localhost:8080/');page.click('#create');page.fill('#name','Browser QA');page.fill('#password','test123');page.fill('#password2','test123');page.click('button.primary');page.wait_for_selector('#trainingButton')
 before=page.evaluate("localStorage.getItem('lspd-training-v1')")
 page.click('#trainingButton');page.click('#capture')
 def key(k):page.keyboard.press(k);page.wait_for_timeout(80)
 def next_step():
  assert page.is_visible('#nextLesson');key('Enter')
 def aim(dx,dy=0):page.dispatch_event('#rangeCanvas','mousemove',{'movementX':dx,'movementY':dy})
 def shot():page.dispatch_event('#rangeCanvas','mousedown',{'button':0});page.wait_for_timeout(550)
 def point_target(i):
  delta=page.evaluate("""i=>{const s=debug.state.scene.state,t=s.targets[i],f=800*(s.aimed?.95:.68),ox=s.aimed?0:1280*.12,oy=s.aimed?0:800*.44-290;let yaw=Math.atan2(t.x-s.x,t.z-s.z)-Math.atan(ox/f),pitch=s.pitch;for(let k=0;k<12;k++){let dx=t.x-s.x,dz=t.z-s.z,side=dx*Math.cos(yaw)-dz*Math.sin(yaw),depth=dx*Math.sin(yaw)+dz*Math.cos(yaw),up=t.y-1.65,yy=up*Math.cos(pitch)-depth*Math.sin(pitch),zz=up*Math.sin(pitch)+depth*Math.cos(pitch);yaw+=(side*f/zz-ox)/f;pitch-=( -yy*f/zz-oy)/f;}const sens=.002*(s.aimed?.55:1);return [(yaw-s.yaw)/sens,(s.pitch-pitch)/sens];}""",i)
  aim(*delta)
 for k in ['w','s','a','d']:
  page.keyboard.down(k);page.wait_for_timeout(180);page.keyboard.up(k)
 next_step();key('Space');key('Space');next_step()
 point_target(0)
 for _ in range(3):shot()
 assert page.evaluate('debug.state.scene.state.destroyed')==1
 next_step();key('Space');aim(400);key('Space');page.dispatch_event('#rangeCanvas','mousedown',{'button':2});point_target(1);shot();page.dispatch_event('#rangeCanvas','mouseup',{'button':2});next_step()
 key('r');page.wait_for_timeout(1900);next_step()
 key('Space');aim(500);key('Space');assert page.is_visible('#nextLesson')
 page.screenshot(path=str(R/'tests/tutorial-passed.png'))
 next_step()
 def hit_target(i):
  # Compute pointer movement from world geometry; do not mutate gameplay state.
  circular=page.evaluate('debug.state.scene.state.stage===8')
  if circular and not page.evaluate('debug.state.scene.state.raised'):key('Space')
  point_target(i)
  if circular:key('Space')
  for _ in range(3):shot()
 for stage in [6,7]:
  hit_target(0);hit_target(1);next_step()
 first=page.evaluate('debug.state.scene.state.targets.map(t=>({...t}))')
 for wave in range(2):
  key('Space');page.wait_for_timeout(80);key('Space')
  hit_target(0);hit_target(1)
  if wave==0:page.wait_for_timeout(1400)
 assert page.is_visible('#nextLesson')
 page.screenshot(path=str(R/'tests/tutorial-circle.png'))
 next_step();page.wait_for_selector('#trainingButton');assert page.evaluate("localStorage.getItem('lspd-training-v1')")==before
 print('PASS nine tutorial steps, keyboard/mouse, hits, ADS, reload, safe crossing, no career writes')
 page.click('#start');page.fill('#character','QA');page.click('button.primary');page.click('#enterRange');page.click('#capture');page.wait_for_timeout(1000);assert page.is_visible('#rangeCanvas');page.evaluate("Object.assign(debug.state.scene.state.ally,{status:'active',x:1.98,z:7})");key('Space');page.wait_for_timeout(1800)
 assert page.evaluate('debug.state.scene.state.resign')==1
 assert page.is_visible('#rangeCanvas');print('PASS one officer counts once; range remains running')
 page.evaluate('document.exitPointerLock()');page.wait_for_timeout(200);page.click('#leaveRange');page.click('#start');page.click('#enterRange');page.click('#capture');key('Space');assert page.evaluate('debug.state.scene.state.raised')==False
 print('PASS repeat entry and single input handler')
 page.evaluate('debug.state.scene.state.elapsed=90');page.wait_for_selector('#again');assert page.evaluate('debug.state.profiles[0].personal.length')==1
 print('PASS timed finish and stored signed result')
 page.click('#again');page.evaluate('debug.state.profiles[0].career.officers=0');page.click('#start');page.click('#enterRange');page.wait_for_selector('#character');print('PASS exhausted career routes to character creation')
 assert not errors,errors
 print('PASS no browser JS errors');b.close()
