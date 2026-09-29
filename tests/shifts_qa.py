from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path('D:/Работа/LSPD')
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://localhost:8080/')
 page.evaluate('''async()=>{const {mountRange}=await import('/range.js?qa');window.scene=mountRange(document.querySelector('#app'),{exercise:'front',onExit:()=>{},onFinish:()=>{}});}''');page.click('#capture');page.wait_for_timeout(100)
 def shoot_at(i):
  page.evaluate('''i=>{const s=scene.state,t=s.targets[i];s.raised=false;s.aimed=true;s.recoil=0;s.yaw=Math.atan2(t.x-s.x,t.z-s.z);s.pitch=Math.atan2(t.y-1.65,Math.hypot(t.x-s.x,t.z-s.z));document.querySelector('canvas').dispatchEvent(new MouseEvent('mousedown',{button:0}));}''',i)
 shoot_at(1);assert page.evaluate('scene.state.targets[1].hits===0&&scene.state.orderErrors===1')
 for _ in range(3):shoot_at(0)
 assert page.evaluate("scene.state.expectedSide==='right' && scene.state.destroyed===1")
 for _ in range(3):shoot_at(1)
 page.wait_for_timeout(1400);assert page.evaluate("scene.state.wave===2&&scene.state.expectedSide==='left'&&scene.state.ally.status==='gone'")
 print('PASS right first rejected, three left then three right, next pair starts left, absent ally')
 page.evaluate('scene.dispose()')
 src=(R/'app.js').read_text(encoding='utf-8')+'\nwindow.debug={state,renderIntro};'
 page.route('**/app.js*',lambda r:r.fulfill(body=src,content_type='application/javascript'));page.reload();page.click('#create');page.fill('#name','QA');page.fill('#password','test123');page.fill('#password2','test123');page.click('button.primary');page.wait_for_selector('#start');page.click('#start');page.fill('#character','Reaper');page.click('button.primary');page.select_option('#shiftSelect','front');assert page.inner_text('.intro-copy h1')=='Вторая смена'
 page.evaluate('''()=>{const RealDate=Date;window.Date=class extends RealDate{constructor(...a){super(...(a.length?a:[2026,8,29,12]));}};debug.renderIntro();}''');assert page.locator('.birthday').count()==1
 page.evaluate("debug.state.profiles[0].career.character='Other';debug.renderIntro()");assert page.locator('.birthday').count()==0
 assert not errors,errors
 print('PASS shift menu, dated Reaper greeting, other name excluded; no JS errors');b.close()
