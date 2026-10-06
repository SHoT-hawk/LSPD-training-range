from playwright.sync_api import sync_playwright
from collections import deque
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/');data=g.evaluate("async()=>{let m=await import('/fps-sector.js');return Array.from({length:100},(_,i)=>m.generateSector(i))}");layouts=set();places=set()
 for s in data:
  layouts.add(str(s['map']));places.add(str(s['entities']));q=deque([(1,1)]);seen={(1,1)}
  while q:
   x,y=q.popleft()
   for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
    v=(x+dx,y+dy)
    if v not in seen and 0<=v[0]<17 and 0<=v[1]<17 and not s['map'][v[1]][v[0]]:seen.add(v);q.append(v)
  assert all((int(e['x']),int(e['y'])) in seen for e in s['entities'])
 assert len(layouts)>90 and len(places)>90;print('PASS 100 connected maps and varied enemy placements',len(layouts),len(places));b.close()
