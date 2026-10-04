from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page(viewport={'width':1440,'height':900});errors=[];g.on('pageerror',lambda e:errors.append(str(e)))
 g.goto('http://localhost:8080/')
 g.evaluate("""async()=>{let {mountThird}=await import('/third-day.js?flex-qa');window.third=mountThird(document.querySelector('#app'),{flashlightBinding:'KeyF',officers:20,onExit:()=>{},onFinish:r=>window.result=r});document.querySelector('#thirdCapture').click();third.state.active=true}""")
 def key(code):g.evaluate("code=>window.dispatchEvent(new KeyboardEvent('keydown',{code,bubbles:true}))",code)
 def mouse(button):g.evaluate("button=>document.querySelector('#thirdCanvas').dispatchEvent(new MouseEvent('mousedown',{button,bubbles:true}))",button)
 def point(side):g.evaluate("""side=>{const s=third.state,t=side===0?-2.5:2.5,w=document.querySelector('#thirdCanvas').width,h=document.querySelector('#thirdCanvas').height,offset=s.lean==='left'?w*.06:-w*.06;s.yaw=Math.atan2(t,11)+Math.atan(offset/(h*.96));s.pitch=-.02;s.recoil=0;}""",side)
 s=lambda:g.evaluate('third.state')
 key('KeyF');assert s()['light'] and s()['stage']==0,'early light is allowed'
 key('KeyQ');key('KeyQ');assert s()['lean'] is None and s()['stage']!=0,'second Q straightens without resetting progress'
 key('KeyQ');assert s()['lean']=='left'
 key('Space');mouse(2);assert s()['ads']
 before=s()['ammo'];mouse(0);assert s()['ammo']==before-1 and s()['stage']!=0 and s()['hits'][0]==[],'miss consumes ammo, not progress'
 point(0);mouse(0);assert len(s()['hits'][0])==1
 key('KeyF');mouse(0);assert len(s()['hits'][0])==1,'shot without light keeps previous hit'
 key('KeyF')
 for _ in range(2):point(0);mouse(0)
 assert len(s()['hits'][0])==3
 key('KeyF');key('Space');key('KeyQ');assert s()['raised'] and s()['lean'] is None and len(s()['hits'][0])==3,'safe post-left order preserves hits'
 g.evaluate("third.state.yaw=-.25;document.querySelector('#thirdCanvas').dispatchEvent(new MouseEvent('mousemove',{movementX:300}))")
 key('KeyE');key('Space');mouse(2);key('KeyF')
 for _ in range(3):point(1);mouse(0)
 key('KeyF');key('KeyE');key('Space')
 assert s()['series']==1,(s()['series'],s()['error'])
 earned=s()['points'];key('KeyE');assert s()['series']==1 and s()['points']==earned,'harmless mistake preserves score'
 # Unsafe transfer still has a personnel consequence and resets the current series.
 key('KeyQ');key('Space');mouse(2);key('KeyF')
 for _ in range(3):point(0);mouse(0)
 key('KeyF');key('KeyQ');before=s()['resign'];g.evaluate("third.state.yaw=-.25;document.querySelector('#thirdCanvas').dispatchEvent(new MouseEvent('mousemove',{movementX:300}))")
 assert s()['resign']==before+1 and s()['hits'][0]==[] and s()['series']==1
 assert not errors,errors
 print('PASS early light, miss and benign inputs preserve progress; flexible transfer; unsafe transfer penalized')
 b.close()
