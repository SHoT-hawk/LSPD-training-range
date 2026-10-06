from playwright.sync_api import sync_playwright
from collections import deque
import math,time
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();errors=[];g.on('pageerror',lambda e:errors.append(str(e)));g.goto('http://localhost:8080/');g.evaluate("async()=>{let m=await import('/fps-game.js');window.result=null;window.game=m.mountFPS(document.querySelector('#app'),{exercise:'bandage',seed:2,onFinish:r=>window.result=r})}");g.click('#fpsStart')
 def face(x,y):g.evaluate("({x,y})=>{const s=game.state,a=Math.atan2(y-s.y,x-s.x),d=Math.atan2(Math.sin(a-s.yaw),Math.cos(a-s.yaw));document.querySelector('#fpsCanvas').dispatchEvent(new MouseEvent('mousemove',{movementX:d/(.0023*s.sensitivity*(s.ads?.55:1)),movementY:s.pitch/(.0018*s.sensitivity)}))}",{'x':x,'y':y})
 def combat():
  s=g.evaluate('game.state')
  if s['question']:
   g.fill('#fpsAmmoAnswer',str(s['ammo']));g.click('#fpsAmmoQuestion button');s=g.evaluate('game.state')
  if s['exercise']=='magazine' and (not s['inspect'] or s['ammo']<2):
   if s['ammo']<2:g.keyboard.press('r');g.wait_for_timeout(1600)
   g.keyboard.down('r');g.wait_for_timeout(600);g.keyboard.up('r')
  if s['raised']:g.keyboard.press('Space')
  g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':2})
  for e in s['entities']:
   if e['kind']!='enemy' or e['hp']<=0 or e.get('hidden'):continue
   d=math.hypot(e['x']-s['x'],e['y']-s['y']);n=max(1,int(d/.04))
   if any(s['map'][int(s['y']+(e['y']-s['y'])*i/n)][int(s['x']+(e['x']-s['x'])*i/n)] for i in range(1,n)):continue
   face(e['x'],e['y']);g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0});face(e['x'],e['y']);g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0})
  g.locator('#fpsCanvas').dispatch_event('mouseup',{'button':2})
 def path(end):
  s=g.evaluate('game.state');start=(int(s['x']),int(s['y']));q=deque([start]);prev={start:None}
  while q:
   v=q.popleft()
   if v==end:break
   for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
    n=(v[0]+dx,v[1]+dy)
    if n not in prev and 0<=n[0]<17 and 0<=n[1]<17 and s['map'][n[1]][n[0]]==0:prev[n]=v;q.append(n)
  assert end in prev;out=[];v=end
  while v!=start:out.append(v);v=prev[v]
  return out[::-1]
 for sector in range(1,4):
  es=g.evaluate('game.state.entities');goals=[(int(e['x']),int(e['y'])) for e in es if e['kind']=='enemy']+[(int(es[-1]['x']),int(es[-1]['y']))]
  for end in goals:
   if g.evaluate('game.state.round')!=sector:break
   for x,y in path(end):
    if g.evaluate('game.state.round')!=sector:break
    combat();face(x+.5,y+.5);g.keyboard.down('w');deadline=time.monotonic()+1.8
    while time.monotonic()<deadline:
     pos=g.evaluate('({x:game.state.x,y:game.state.y,round:game.state.round,question:!!game.state.question,done:game.state.done})')
     if pos['question']:g.keyboard.up('w');combat();face(x+.5,y+.5);g.keyboard.down('w')
     if pos['done'] or pos['round']!=sector or math.hypot(pos['x']-x-.5,pos['y']-y-.5)<.12:break
     g.wait_for_timeout(25)
    g.keyboard.up('w');g.wait_for_timeout(35);combat()
  print('sector',sector,g.evaluate('game.state.completed'),flush=True)
 assert g.evaluate('result&&result.reason')=='extracted',g.evaluate('result');assert not errors,errors;print('PASS generated three-sector real-input route',g.evaluate('result'));b.close()
