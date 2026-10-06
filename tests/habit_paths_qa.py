from playwright.sync_api import sync_playwright
from collections import deque
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/');g.evaluate("""async()=>{let m=await import('/habit-shifts.js?v=pathqa');window.game=m.mountHabit(document.querySelector('#app'),{mode:'bandage',seed:0,onExit:()=>{},onFinish:r=>window.lastResult=r});document.querySelector('#habitStart').click()}""")
 for seed in range(4):
  g.evaluate('(seed)=>{game.state.round=seed+1;game.nextScenario()}',seed)
  s=g.evaluate('game.state');maze=s['maze'];start=(int(s['x']),int(s['y']));end=(int(s['extraction']['x']),int(s['extraction']['y']))
  todo=deque([start]);seen={start}
  while todo:
   x,y=todo.popleft()
   for nx,ny in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
    if 0<=ny<len(maze) and 0<=nx<len(maze[0]) and maze[ny][nx]=='.' and (nx,ny) not in seen:seen.add((nx,ny));todo.append((nx,ny))
  assert end in seen,(seed,start,end,len(seen))
  assert all((int(e['x']),int(e['y'])) in seen for e in s['enemies']),(seed,'enemy trapped')
 print('PASS exit and enemies reachable in four maze variants')
 b.close()
