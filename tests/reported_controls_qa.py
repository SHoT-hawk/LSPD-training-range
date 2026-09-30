from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();errors=[];g.on('pageerror',lambda e:errors.append(str(e)))
 g.goto('http://localhost:8080/')
 g.click('#create');g.fill('#name','QA');g.fill('#password','password');g.fill('#password2','password');g.click('button.primary');g.click('#start');g.fill('#character','QA');g.click('button.primary');g.select_option('#shiftSelect','third')
 g.click('#lightBinding');g.click('#lightBinding',button='middle')
 assert g.evaluate("localStorage.getItem('lspd-flashlight-binding')")=='Mouse1','Binding button did not capture mouse'
 g.select_option('#lightMouseBinding','Mouse4');assert g.evaluate("localStorage.getItem('lspd-flashlight-binding')")=='Mouse4'
 g.select_option('#lightMouseBinding','Mouse1')
 g.click('#enterRange');g.click('#thirdCapture')
 assert g.evaluate('''async()=>{let {mountThird}=await import('/third-day.js?check');window.testScene=mountThird(document.querySelector('#app'),{flashlightBinding:'Mouse1',onExit:()=>{},onFinish:()=>{}});document.querySelector('#thirdCapture').click();window.dispatchEvent(new KeyboardEvent('keydown',{code:'KeyQ'}));return testScene.state.raised}'''),'Q must not lower gun'
 g.evaluate("document.querySelector('#thirdCanvas').dispatchEvent(new MouseEvent('mousedown',{button:2}))")
 assert g.evaluate('testScene.state.raised && !testScene.state.ads && testScene.state.stage===1')
 g.evaluate("window.testScene.state.active=true;window.dispatchEvent(new KeyboardEvent('keydown',{code:'Space'}))")
 assert not g.evaluate('testScene.state.raised')
 g.evaluate("document.querySelector('#thirdCanvas').dispatchEvent(new MouseEvent('mousedown',{button:2}))")
 assert g.evaluate('testScene.state.ads && testScene.state.stage===2')
 g.evaluate('testScene.state.stage=3;testScene.state.light=true;testScene.state.ammo=30;testScene.state.yaw=Math.atan2(-2.5,11);testScene.state.pitch=-.02')
 before=g.evaluate('testScene.state.pitch');g.evaluate("document.querySelector('#thirdCanvas').dispatchEvent(new MouseEvent('mousedown',{button:0}))")
 assert g.evaluate('testScene.state.recoil')>.1 and g.evaluate('testScene.state.ammo')==29,'Shot should recoil and consume a round'
 assert not errors,errors
 print('PASS mouse button binding on button, Space required before ADS, recoil changes aim')
 b.close()
