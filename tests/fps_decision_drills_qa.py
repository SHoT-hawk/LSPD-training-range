from playwright.sync_api import sync_playwright
import sys
URL=sys.argv[1] if len(sys.argv)>1 else 'http://localhost:8080/'
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page(viewport={'width':1280,'height':720});errors=[];g.on('pageerror',lambda e:errors.append(str(e)));g.goto(URL)
 def mount(ex,seed=0,motion='static'):
  g.evaluate("async o=>{window.game?.dispose();let m=await import('./fps-game.js?v=5');window.result=null;window.game=m.mountFPS(document.querySelector('#app'),{...o,onFinish:r=>window.result=r});}",dict(exercise=ex,seed=seed,motion=motion));g.evaluate("document.querySelector('#fpsCanvas').requestPointerLock=()=>Promise.resolve()");g.click('#fpsStart');g.evaluate('document.exitPointerLock()');g.wait_for_timeout(150);g.evaluate("game.state.active=true;document.querySelector('#fpsPause').hidden=true")
 def aim(x,y):g.evaluate("([x,y])=>{let s=game.state;s.yaw=Math.atan2(y-s.y,x-s.x);s.pitch=0;s.raised=false;s.ads=true}",[x,y])
 mount('judgement');g.evaluate("game.state.scan=new Set([5.5,8.5,11.5])");aim(13.5,7.5);g.keyboard.press('f');g.wait_for_timeout(1200);assert g.evaluate("game.state.entities.find(e=>e.kind==='enemy').posture")=='kneeling';assert g.evaluate("game.state.entities.some(e=>e.kind==='civilian')");g.screenshot(path='D:/Работа/LSPD/tests/decision-kneeling.png')
 g.keyboard.press('f');assert g.evaluate('game.state.arrests')==0
 # approach through actual WASD
 g.keyboard.down('w');g.wait_for_timeout(2800);g.keyboard.up('w');aim(13.5,7.5);g.keyboard.press('f');assert g.evaluate('game.state.arrests')==1
 print('PASS command, visible surrender, distance gate and real approach arrest')
 mount('judgement',seed=3);g.evaluate("game.state.scan=new Set([5.5,8.5,11.5])");aim(13.5,7.5);g.keyboard.press('f');g.wait_for_timeout(1200);assert g.evaluate("game.state.entities.find(e=>e.kind==='enemy').posture")=='kneeling';g.wait_for_timeout(3600);assert g.evaluate("game.state.entities.find(e=>e.kind==='enemy').posture")=='aiming';g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0});g.wait_for_timeout(150);aim(13.5,7.5);g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0});assert g.evaluate('game.state.destroyed')==1
 print('PASS surrender reversal and aimed shots')
 mount('judgement',seed=2);assert g.evaluate("game.state.entities.some(e=>e.kind==='hostage')");aim(12.5,8.5);g.screenshot(path='D:/Работа/LSPD/tests/decision-hostage.png');g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0});assert g.evaluate('result.reason')=='civilian_hit';print('PASS distinct hostage and protected bullet priority')
 mount('judgement');aim(13.5,7.5);g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0});assert g.evaluate('result.reason')=='unjustified_shot';print('PASS armed non-aiming suspect not automatic free shot')
 mount('memory');g.keyboard.press('m');assert g.locator('#memoryQuestion').count();expected=g.evaluate('game.state.memory.expected');
 for i,v in enumerate(expected):g.select_option(f'[data-cell="{i}"]',v)
 g.click('#memoryQuestion button');assert g.evaluate('game.state.completed')==1;print('PASS observed scene and memory answers')
 mount('moving',motion='moving');assert g.evaluate('game.state.map.length')==17;assert g.evaluate("game.state.entities.filter(e=>e.kind==='enemy').length")>=3;g.evaluate("game.state.entities.filter(e=>e.kind==='enemy').forEach(e=>e.hidden=false)");before=g.evaluate("game.state.entities.filter(e=>e.kind==='enemy').map(e=>[e.x,e.y])");g.wait_for_timeout(600);after=g.evaluate("game.state.entities.filter(e=>e.kind==='enemy').map(e=>[e.x,e.y])");assert before!=after;print('PASS sixth generated maze, multiple enemies and actual moving positions')
 mount('attention');free=g.evaluate('game.state.team.free');g.keyboard.press(str(free+1));g.wait_for_timeout(4200);assert g.evaluate('game.state.teamSpawn')>=2;g.screenshot(path='D:/Работа/LSPD/tests/team-sector.png');assert g.evaluate("game.state.entities.some(e=>e.kind==='enemy'&&e.hp===0)");print('PASS free sector selection and NPC handles own threat')
 assert not errors,errors;b.close()
