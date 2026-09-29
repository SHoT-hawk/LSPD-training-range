from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path('D:/Работа/LSPD')
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':1280,'height':800});errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
 page.goto('http://localhost:8080/')
 page.evaluate('''async()=>{const {mountRange}=await import('/range.js?v=test');window.mount=mountRange;window.scene=mountRange(document.querySelector('#app'),{tutorial:true,onExit:()=>{},onFinish:()=>{}});}''')
 page.click('#capture');page.wait_for_timeout(150)
 # deterministic geometry: hip aim projection matches muzzle, not screen center
 page.evaluate('''()=>{const s=scene.state;s.raised=false;s.ally.status='gone';s.pitch=0;s.yaw=0;s.targets=[{x:153.6/544*11,y:1.65-62/544*11,z:11,hits:0},{x:-4,y:1.5,z:11,hits:0}];}''')
 page.dispatch_event('#rangeCanvas','mousedown',{'button':0});assert page.evaluate('scene.state.targets[0].hits')==1
 page.screenshot(path=str(R/'tests/hip.png'));print('PASS hip hit uses visible muzzle')
 page.evaluate('''()=>{const s=scene.state;s.recoil=0;s.targets[0]={x:0,y:1.65,z:11,hits:0};}''');page.dispatch_event('#rangeCanvas','mousedown',{'button':2});page.dispatch_event('#rangeCanvas','mousedown',{'button':0});assert page.evaluate('scene.state.targets[0].hits')==1;print('PASS ADS hit uses center')
 page.evaluate('''()=>{const s=scene.state;s.recoil=0;s.ally={x:0,y:1,z:7,status:'active'};}''');page.wait_for_timeout(100);assert page.evaluate('Boolean(scene.state.failure)');assert 'Enter' in page.inner_text('#lessonText');print('PASS pointing at ally blocks lesson')
 page.keyboard.press('Enter');assert page.evaluate('!scene.state.failure && scene.state.raised')
 page.evaluate('''()=>{const s=scene.state;s.raised=false;s.aimed=true;s.yaw=0;s.pitch=0;s.recoil=0;document.querySelector('canvas').dispatchEvent(new MouseEvent('mousedown',{button:0}));}''');assert page.evaluate("scene.state.ally.status==='killed' && Boolean(scene.state.failure)");print('PASS ally shot marks failure; retry clears it')
 page.evaluate('''()=>{scene.dispose();scene=mount(document.querySelector('#app'),{onExit:()=>{},onFinish:()=>{}});}''');page.click('#capture');page.wait_for_timeout(100);assert page.evaluate("scene.state.ally.status==='active'")
 statuses=[]
 for _ in range(4):
  statuses.append(page.evaluate('scene.state.ally.status'))
  page.evaluate('scene.state.intermission=.01');page.wait_for_timeout(100)
 assert statuses==['active','gone','active','active'],statuses
 print('PASS ally varies per wave',statuses)
 assert not errs,errs
 b.close()
