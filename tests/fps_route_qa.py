from playwright.sync_api import sync_playwright
import math,time
from collections import deque
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();errors=[];g.on('pageerror',lambda e:errors.append(str(e)));g.goto('http://localhost:8080/');g.evaluate("""async()=>{let m=await import('/fps-game.js');window.result=null;window.game=m.mountFPS(document.querySelector('#app'),{exercise:'bandage',onExit:()=>{},onFinish:r=>window.result=r})}""");g.click('#fpsStart')
 def face(x,y):
  g.evaluate('''({x,y})=>{const s=game.state,angle=Math.atan2(y-s.y,x-s.x),delta=Math.atan2(Math.sin(angle-s.yaw),Math.cos(angle-s.yaw));document.querySelector('#fpsCanvas').dispatchEvent(new MouseEvent('mousemove',{movementX:delta/(.0023*(s.ads?.55:1)),movementY:-s.pitch/.0018,bubbles:true}))}''',{'x':x,'y':y})
 def shoot_visible():
  s=g.evaluate('game.state');
  if s['raised']:g.keyboard.press('Space')
  g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':2})
  for e in s['entities']:
   if e['kind']!='enemy' or e['hp']<=0:continue
   d=math.hypot(e['x']-s['x'],e['y']-s['y']);n=max(1,int(d/.05))
   if any(s['map'][int(s['y']+(e['y']-s['y'])*i/n)][int(s['x']+(e['x']-s['x'])*i/n)] for i in range(1,n)):continue
   face(e['x'],e['y']);g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0});face(e['x'],e['y']);g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0})
  g.locator('#fpsCanvas').dispatch_event('mouseup',{'button':2})
 def route():
  s=g.evaluate('game.state');start=(int(s['x']),int(s['y']));end=(15,14);q=deque([start]);prev={start:None}
  while q:
   v=q.popleft()
   if v==end:break
   for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
    n=(v[0]+dx,v[1]+dy)
    if n not in prev and 0<=n[0]<17 and 0<=n[1]<17 and s['map'][n[1]][n[0]]==0:prev[n]=v;q.append(n)
  assert end in prev;out=[];v=end
  while v!=start:out.append(v);v=prev[v]
  return list(reversed(out))
 # Walk all three sectors using actual keys. State is read for navigation, never teleported.
 for sector in range(1,4):
  for x,y in route():
   if g.evaluate('game.state.round')!=sector:break
   shoot_visible();face(x+.5,y+.5)
   deadline=time.monotonic()+2
   g.keyboard.down('w')
   while time.monotonic()<deadline:
    s=g.evaluate('({x:game.state.x,y:game.state.y,round:game.state.round})')
    if s['round']!=sector or math.hypot(s['x']-x-.5,s['y']-y-.5)<.14:break
    g.wait_for_timeout(30)
   g.keyboard.up('w')
  print('sector',sector,'completed',g.evaluate('game.state.completed'),flush=True)
 assert g.evaluate('result.completed')==3 and g.evaluate('result.reason')=='extracted';assert not errors;print('PASS three sectors walked with collision and spatial aimed fire',g.evaluate('result'));b.close()
