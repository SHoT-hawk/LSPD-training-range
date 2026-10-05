from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();errors=[];g.on('pageerror',lambda e:errors.append(str(e)))
 g.goto('http://localhost:8080/')
 g.evaluate("""async()=>{const {mountThird}=await import('/third-day.js?direct-lean');window.third=mountThird(document.querySelector('#app'),{onExit:()=>{},onFinish:()=>{}});document.querySelector('#thirdCapture').click();third.state.active=true}""")
 def key(code):g.evaluate("code=>window.dispatchEvent(new KeyboardEvent('keydown',{code,bubbles:true}))",code)
 def s():return g.evaluate('third.state')
 key('KeyQ');assert s()['lean']=='left'
 key('KeyE');assert s()['lean']=='right' and not s()['ads'],'E directly replaces Q lean'
 key('KeyQ');assert s()['lean']=='left','Q directly replaces E lean'
 key('KeyQ');assert s()['lean'] is None,'same side still straightens'
 # Completed left trio; safe translation still required before right can count.
 g.evaluate("third.state.hits[0]=[{x:0,y:0},{x:0,y:0},{x:0,y:0}];third.state.raised=true;third.state.yaw=-.25;third.state.lean='left'")
 key('KeyE');assert s()['lean']=='right' and not s()['transferCrossed'],'E alone must not count as a safe transfer'
 g.evaluate("document.querySelector('#thirdCanvas').dispatchEvent(new MouseEvent('mousemove',{movementX:300,bubbles:true}))")
 assert s()['transferCrossed'] and s()['resign']==0 and s()['lean']=='right','raised swept transfer while directly leaning right'
 key('Space');g.evaluate("document.querySelector('#thirdCanvas').dispatchEvent(new MouseEvent('mousedown',{button:2,bubbles:true}))")
 assert s()['ads'],'right-side ADS after safe crossing'
 # Switching lean alone does not bypass the unsafe swept transfer consequence.
 g.evaluate("third.state.hits[0]=[{x:0,y:0},{x:0,y:0},{x:0,y:0}];third.state.hits[1]=[];third.state.transferCrossed=false;third.state.lean='left';third.state.raised=false;third.state.ads=false;third.state.yaw=-.25")
 before=s()['resign'];key('KeyE');assert s()['lean']=='right' and s()['resign']==before
 g.evaluate("document.querySelector('#thirdCanvas').dispatchEvent(new MouseEvent('mousemove',{movementX:300,bubbles:true}))")
 assert s()['resign']==before+1 and s()['lean'] is None and s()['hits'][0]==[],'unsafe crossing still penalized'
 assert not errors,errors
 print('PASS direct Q/E lean replaces opposite; swept transfer and ADS still gated')
 b.close()
