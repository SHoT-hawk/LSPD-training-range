from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page(viewport={'width':1280,'height':800});errors=[];g.on('pageerror',lambda e:errors.append(str(e)))
 g.goto('http://localhost:8080/');g.click('#create');g.fill('#name','QA');g.fill('#password','password');g.fill('#password2','password');g.click('button.primary');g.click('#start');g.fill('#character','Tester');g.click('button.primary')
 for mode,title in [('bandage','Четвёртая'),('magazine','Пятая')]:
  g.select_option('#shiftSelect',mode);assert title in g.inner_text('.intro-copy h1');g.click('#enterRange');assert g.locator('#habitStart').is_visible();g.click('#habitStart');assert g.locator('#habitCanvas').is_visible();assert ('04' if mode=='bandage' else '05') in g.inner_text('#habitTitle')
  assert 'WASD' in g.inner_text('#habitInstruction')
  g.click('#habitExit');assert g.locator('#start').is_visible();g.click('#start')
 assert not errors,errors
 print('PASS fourth/fifth selectable, playable map, exit/menu, no JS errors')
 b.close()
