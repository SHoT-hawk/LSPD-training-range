from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch()
 page=b.new_page()
 errors=[]
 page.on('pageerror',lambda err:errors.append(str(err)))
 page.goto('http://localhost:8080/')
 page.click('#create');page.fill('#name','audio-QA');page.fill('#password','password');page.fill('#password2','password');page.click('button.primary')
 page.click('#start');page.fill('#character','Tester');page.click('button.primary')
 page.select_option('#shiftSelect','third')
 assert page.locator('#lightBinding').is_visible()
 page.click('#lightBinding');page.keyboard.press('t')
 assert page.evaluate("localStorage.getItem('lspd-flashlight-binding')")=='KeyT'
 assert 'T · изменить' in page.inner_text('#lightBinding')
 page.click('#lightBinding')
 page.evaluate("document.querySelector('#shiftStory').dispatchEvent(new MouseEvent('mousedown',{button:3,bubbles:true}))")
 assert page.evaluate("localStorage.getItem('lspd-flashlight-binding')")=='Mouse3'
 assert 'кнопка мыши 4' in page.inner_text('#lightBinding')
 page.click('#enterRange');page.click('#thirdCapture')
 page.keyboard.press('q');page.mouse.click(720,450,button='right')
 page.evaluate("document.querySelector('#thirdCanvas').dispatchEvent(new MouseEvent('mousedown',{button:3}))")
 page.wait_for_timeout(80)
 assert 'СВЕТ ВКЛ (кнопка мыши 4)' in page.inner_text('#thirdStatus')
 page.evaluate("document.querySelector('#thirdExit').click()")
 page.click('#start');page.select_option('#shiftSelect','third')
 page.click('#lightBinding');page.keyboard.press('g')
 page.click('#enterRange');page.click('#thirdCapture')
 assert 'СВЕТ ВЫКЛ (G)' in page.inner_text('#thirdStatus')
 page.keyboard.press('q');page.mouse.click(720,450,button='right');page.keyboard.press('g');page.wait_for_timeout(80)
 assert 'СВЕТ ВКЛ (G)' in page.inner_text('#thirdStatus')
 before=page.evaluate("async()=>{const {playShot}=await import('/shot-sound.js');return !!playShot}")
 assert before
 page.evaluate("document.querySelector('#thirdCanvas').dispatchEvent(new MouseEvent('mousedown',{button:0}))")
 assert page.evaluate("document.querySelector('#thirdStatus').textContent.includes('29/30')")
 assert errors==[],errors
 print('PASS key and mouse rebinding, actual G flashlight, fired shot, audio module, no page errors')
 b.close()
