from playwright.sync_api import sync_playwright
URL='http://localhost:8080/'
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page(viewport={'width':1440,'height':900})
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(URL);page.click('#create');page.fill('#name','QA');page.fill('#password','test123');page.fill('#password2','test123');page.click('button.primary');page.wait_for_selector('#start');page.click('#start');page.fill('#character','Tester');page.click('button.primary');page.select_option('#shiftSelect','third');assert page.inner_text('.intro-copy h1')=='Третья смена'
 page.click('#lightBinding');page.keyboard.press('t');assert page.evaluate("localStorage.getItem('lspd-flashlight-binding')")=='KeyT'
 page.click('#enterRange');page.wait_for_selector('#thirdCapture');page.click('#thirdCapture');page.wait_for_timeout(200)
 print('entered',page.locator('#thirdStats').inner_text(),page.locator('#thirdInstruction').inner_text())
 assert not errors,errors
 page.screenshot(path='D:/Работа/LSPD/tests/third-screen.png')
 print('layers',page.evaluate("""()=>{let b=document.querySelector('#thirdExit'),c=document.querySelector('#thirdCanvas'),r=b.getBoundingClientRect();return {button:getComputedStyle(b).zIndex,canvas:getComputedStyle(c).zIndex,under:document.elementFromPoint(r.left+r.width/2,r.top+r.height/2)?.id,rect:[r.left,r.top]}}"""))
 # Isolated playable scene exposes state to assert transitions and error branches.
 page.evaluate("document.querySelector('#thirdExit').click()")
 page.evaluate("""async()=>{const {mountThird}=await import('/third-day.js?v=test');window.third=mountThird(document.querySelector('#app'),{flashlightBinding:'KeyT',onExit:()=>{},onFinish:r=>window.thirdResult=r});}""")
 page.evaluate("document.querySelector('#thirdCapture').click()");page.wait_for_timeout(100)
 def stage():return page.evaluate('third.state.stage')
 def key(code):page.evaluate("code=>window.dispatchEvent(new KeyboardEvent('keydown',{code,bubbles:true}))",code)
 def mouse(button):page.evaluate("button=>document.querySelector('#thirdCanvas').dispatchEvent(new MouseEvent('mousedown',{button,bubbles:true}))",button)
 def point(side):
  page.evaluate("""side=>{const s=third.state,t=side===0?-2.5:2.5;const offset=s.lean==='left'?document.querySelector('#thirdCanvas').width*.06:-document.querySelector('#thirdCanvas').width*.06;s.yaw=Math.atan2(t,11)+Math.atan(offset/(document.querySelector('#thirdCanvas').height*.96));s.pitch=-.02;s.recoil=0;}""",side)
 key('KeyQ');assert stage()==1
 mouse(2);assert stage()==1 and page.evaluate('third.state.raised')
 key('Space');assert not page.evaluate('third.state.raised')
 mouse(2);assert stage()==2
 key('KeyT');assert stage()==3
 point(0);pitch_before=page.evaluate('third.state.pitch');mouse(0)
 assert page.evaluate('third.state.pitch')>pitch_before and page.evaluate('third.state.recoil')>.1
 for i in range(2):point(0);mouse(0)
 assert stage()==4,(stage(),page.inner_text('#thirdInstruction'))
 key('KeyT');key('KeyQ');key('Space');assert stage()==6
 page.evaluate("third.state.yaw=-.25;document.querySelector('#thirdCanvas').dispatchEvent(new MouseEvent('mousemove',{movementX:300,movementY:0}))")
 assert stage()==7,(stage(),page.inner_text('#thirdInstruction'))
 key('KeyE');key('Space');mouse(2);key('KeyT');assert stage()==10,(stage(),page.inner_text('#thirdInstruction'))
 for i in range(3):point(1);mouse(0)
 assert stage()==11,(stage(),page.inner_text('#thirdInstruction'))
 key('KeyT');key('KeyE');key('Space');assert page.evaluate('third.state.series')==1
 print('PASS full series',page.evaluate('({series:third.state.series,points:third.state.points,grouping:third.state.grouping})'))
 third_before=page.evaluate('third.state.points');key('KeyE');assert stage()==0 and page.evaluate('third.state.points')==third_before
 # Unsafe transfer has a real personnel consequence, simple aim does not.
 key('KeyQ');key('Space');mouse(2);key('KeyT');
 for i in range(3):point(0);mouse(0)
 key('KeyT');key('KeyQ');before=page.evaluate('third.state.resign')
 page.evaluate("third.state.yaw=-.25;document.querySelector('#thirdCanvas').dispatchEvent(new MouseEvent('mousemove',{movementX:300}))")
 assert stage()==0 and page.evaluate('third.state.resign')==before+1
 points=page.evaluate('third.state.points')
 page.evaluate('third.state.elapsed=89.99');page.wait_for_timeout(100)
 assert page.evaluate('thirdResult.series')==1 and page.evaluate('thirdResult.points')==points
 print('PASS unsafe transfer resignation; timeout retains points and series')
 assert not errors,errors
 browser.close()
