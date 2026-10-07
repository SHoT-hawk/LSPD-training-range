from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/')
 def mount(ex):
  g.evaluate("async ex=>{game?.dispose?.();let m=await import('/fps-game.js');window.result=null;window.game=m.mountFPS(document.querySelector('#app'),{exercise:ex,onFinish:r=>result=r});document.querySelector('#fpsCanvas').requestPointerLock=()=>Promise.resolve()}",ex);g.click('#fpsStart')
 g.evaluate('window.game=null')
 mount('judgement');g.evaluate("()=>{let s=game.state;s.scan=new Set([5.5,8.5,11.5]);s.yaw=Math.atan2(-1,5);s.raised=false;s.ads=true;}");g.keyboard.press('f');g.wait_for_timeout(1200);g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0});assert g.evaluate('result.reason')=='civilian_hit';print('PASS surrendered suspect shot fails')
 mount('bandage');g.evaluate("()=>{let s=game.state;s.entities=[{kind:'enemy',x:s.x+.4,y:s.y,hp:2,clock:99}];}");g.keyboard.press('r');g.wait_for_timeout(100);assert g.evaluate('game.state.unsafeReloads')==1;g.keyboard.press('x');assert g.evaluate('game.state.reload')==0;assert g.evaluate('game.state.ammo')==12;print('PASS unsafe reload identified and cancellable without ammo magic')
 mount('bandage');g.evaluate("()=>{let s=game.state;s.wounded=true;s.bleed=7;s.entities=[{kind:'exit',x:s.x,y:s.y,hp:1}];}");g.wait_for_timeout(120);assert g.evaluate('game.state.completed')==0;g.keyboard.press('f');g.wait_for_timeout(3400);assert not g.evaluate('game.state.wounded');assert g.evaluate('game.state.completed')==1;print('PASS last threat absent still requires wound closure, genuine cover return credited')
 mount('memory');g.keyboard.press('m')
 for i in range(4):g.select_option(f'[data-cell="{i}"]','civilian')
 g.click('#memoryQuestion button');assert g.evaluate('game.state.mistakes')==1;assert g.evaluate('game.state.completed')==0;assert not g.locator('#memoryQuestion').count();print('PASS wrong memory answer retries same scene without credit')
 mount('moving');assert g.locator('#fpsVoiceMode').input_value()=='important';g.keyboard.press('Space');g.keyboard.press('r');g.wait_for_timeout(1700);assert g.locator('#fpsPartner').get_attribute('data-voice-state')!='playing';print('PASS routine moving shift chatter muted by default')
 b.close()
