from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page(viewport={'width':1280,'height':800});err=[];g.on('pageerror',lambda e:err.append(str(e)));g.goto('http://localhost:8080/')
 g.click('#create');g.fill('#name','BandageQA');g.fill('#password','password');g.fill('#password2','password');g.click('button.primary');g.click('#start');g.fill('#character','Tester');g.click('button.primary');g.select_option('#shiftSelect','bandage');g.click('#enterRange');g.click('#habitStart')
 # End-to-end: visible menu route, eight real cover decisions and 3.2-second animations.
 for i in range(8):
  expected_cover=0 if (i+1)%4==0 else (2.2 if (i+1)%2==1 else -2.2)
  direction='d' if expected_cover>0 else 'a'
  if expected_cover:g.keyboard.down(direction);g.wait_for_timeout(610);g.keyboard.up(direction)
  status=g.inner_text('#habitStatus');assert 'ЗА УКРЫТИЕМ' in status,(i,status,g.inner_text('#habitStats'))
  g.keyboard.press('f');g.wait_for_timeout(3300)
 g.wait_for_selector('#again',timeout=5000)
 assert 'Четвёртая смена' in g.inner_text('h2');assert 'Верных решений: 8' in g.inner_text('#app'),g.inner_text('#app');assert not err,err
 print('PASS eight human-timed cover-bandage decisions, signed result, no JS errors')
 b.close()
