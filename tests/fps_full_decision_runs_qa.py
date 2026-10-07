from playwright.sync_api import sync_playwright
import math
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/');errors=[];g.on('pageerror',lambda e:errors.append(str(e)))
 def mount(ex):
  g.evaluate("async ex=>{window.game?.dispose();const m=await import('/fps-game.js');window.result=null;window.game=m.mountFPS(document.querySelector('#app'),{exercise:ex,seed:0,onFinish:r=>result=r});document.querySelector('#fpsCanvas').requestPointerLock=()=>Promise.resolve()}",ex);g.click('#fpsStart')
 def face(e):g.evaluate("e=>{let s=game.state;s.yaw=Math.atan2(e.y-s.y,e.x-s.x);s.pitch=0;s.raised=false;s.ads=true}",e)
 def shot(e):
  face(e);g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0});face(e);g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0})
 mount('attention')
 for room in range(1,4):
  free=g.evaluate('game.state.team.free');g.keyboard.press(str(free+1));deadline=0
  while g.evaluate('!game.state.done&&game.state.wave')==room and deadline<230:
   es=g.evaluate('game.state.entities');state=g.evaluate('({loan:game.state.teamLoan,sector:game.state.loanSector,choice:game.state.teamChoice})')
   for e in es:
    if e['kind']=='enemy' and e['hp']>0 and (e['teamSector']==state['choice'] or state['loan'] and e['teamSector']==state['sector']):shot(e)
   g.wait_for_timeout(100);deadline+=1
  assert g.evaluate('game.state.completed')==room,(room,g.evaluate('game.state'))
 assert g.evaluate('result.reason')=='scenarios_done';assert g.evaluate('result.completed')==3;print('PASS three attention rooms, player shoots own and borrowed sectors, NPC handles others')
 mount('memory')
 for wave in range(1,4):
  # no arbitrary countdown; real key and form
  g.keyboard.press('m');expected=g.evaluate('game.state.memory.expected')
  for i,v in enumerate(expected):g.select_option(f'[data-cell="{i}"]',v)
  g.click('#memoryQuestion button')
 assert g.evaluate('result.reason')=='scenarios_done';print('PASS three memory scenes and finish')
 mount('pace')
 for wave in range(1,7):
  g.wait_for_function('w=>game.state.wave===w||game.state.done',arg=wave)
  count=0
  while g.evaluate('!game.state.done&&game.state.wave')==wave and count<250:
   es=g.evaluate('game.state.entities');pos=g.evaluate('({x:game.state.x,y:game.state.y})');es.sort(key=lambda e: (0 if e.get('posture') in ['armed','aiming'] else 1,math.hypot(e['x']-pos['x'],e['y']-pos['y'])))
   for e in es:
    if e['hp']<=0 or e.get('hidden'):continue
    face(e)
    if e.get('posture')=='aiming':shot(e);continue
    if e.get('posture')=='armed':g.keyboard.press('f');continue
    if e['kind'] in ['civilian','hostage'] or e.get('posture')=='kneeling':
     pos=g.evaluate('({x:game.state.x,y:game.state.y})');d=math.hypot(e['x']-pos['x'],e['y']-pos['y'])
     if d>1.35:
      # slow enough to stop within arrest reach; no teleport
      g.locator('#fpsCanvas').dispatch_event('mouseup',{'button':2});g.keyboard.down('w');g.wait_for_timeout(160);g.keyboard.up('w')
     else:g.keyboard.press('f')
     break
   g.wait_for_timeout(80);count+=1
  assert g.evaluate('game.state.completed')==wave,(wave,g.evaluate('game.state'),g.evaluate('result'))
 assert g.evaluate('result.reason')=='scenarios_done';print('PASS six variable pace scenes, surrender/refusal/reversal, civilians and real walking')
 assert not errors,errors;b.close()
