from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page(viewport={'width':1280,'height':800});errors=[];g.on('pageerror',lambda e:errors.append(str(e)))
 g.goto('http://localhost:8080/');g.click('#create');g.fill('#name','QA');g.fill('#password','password');g.fill('#password2','password');g.click('button.primary');g.click('#start');g.fill('#character','Tester');g.click('button.primary')
 for mode,title in [('bandage','Четвёртая'),('magazine','Пятая')]:
  g.select_option('#shiftSelect',mode);assert title in g.inner_text('.intro-copy h1');g.click('#enterRange');assert g.locator('#habitStart').is_visible();g.click('#habitStart');assert g.locator('#habitCanvas').is_visible();assert title.upper() in g.inner_text('#habitTitle')
  if mode=='bandage':
   g.evaluate('document.exitPointerLock()');g.wait_for_timeout(180);g.click('#habitExit');assert g.locator('#start').is_visible()
  else:
   for _ in range(8):g.keyboard.down('w');g.wait_for_timeout(55);g.keyboard.up('w');g.wait_for_timeout(25)
   g.wait_for_selector('#again',timeout=3000);assert title in g.inner_text('h2');assert 'Ошибок: 8' in g.inner_text('#app');g.click('#again')
  g.click('#start')
 assert not errors,errors
 print('PASS fourth/fifth shifts selectable, gameplay, fifth signed result and menu; no JS errors')
 b.close()
