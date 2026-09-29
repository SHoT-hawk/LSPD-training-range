from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path('D:/Работа/LSPD')
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 page=b.new_page(viewport={'width':1280,'height':800})
 source=(ROOT/'app.js').read_text(encoding='utf-8')+'\nwindow.debug={state,startRun,crossOfficerCheck};'
 page.route('**/app.js*',lambda r:r.fulfill(body=source,content_type='application/javascript'))
 page.goto('http://localhost:8080/')
 page.evaluate('''async()=>{const keys=await crypto.subtle.generateKey({name:'ECDSA',namedCurve:'P-256'},true,['sign','verify']); const s=debug.state; s.profiles=[{id:'test',name:'Test',personal:[],career:{character:'Test',days:1,officers:99},signingKeys:{privateKey:await crypto.subtle.exportKey('jwk',keys.privateKey),publicKey:await crypto.subtle.exportKey('jwk',keys.publicKey)}}];s.current='test'; debug.startRun();cancelAnimationFrame(s.run.raf);s.run.weapon=2;s.run.targets=[];s.run.officers=[{id:'a',active:true,x:50,y:50}];for(let i=0;i<5;i++)debug.crossOfficerCheck();}''')
 print(page.evaluate('({resign:debug.state.run.resign,stillActive:debug.state.run.officers[0].active})'))
 b.close()
