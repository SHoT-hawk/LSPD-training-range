from playwright.sync_api import sync_playwright
import sys
url=sys.argv[1] if len(sys.argv)>1 else 'http://localhost:8080/'
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page(viewport={'width':1366,'height':768});errors=[];g.on('pageerror',lambda e:errors.append(str(e)));g.goto(url);g.click('#create');g.fill('#name','SevenReleaseQA');g.fill('#password','pass1234');g.fill('#password2','pass1234');g.click('button.primary');g.click('#start');g.fill('#character','QA');g.click('button.primary')
 for ex in ['circle','front','third','bandage','magazine','moving','judgement','attention','pace','memory']:
  g.select_option('#shiftSelect',ex);assert g.locator('#lightBinding').is_visible();g.click('#enterRange');assert g.locator('#fpsSensitivity').is_visible();g.click('#fpsStart');g.keyboard.down('w');g.wait_for_timeout(100);g.keyboard.up('w');g.keyboard.press('Space');
  if ex not in ['judgement','pace','memory']:g.locator('#fpsCanvas').dispatch_event('mousedown',{'button':0})
  g.wait_for_timeout(120);g.keyboard.press('Escape');g.click('#fpsMusic');assert g.locator('#fpsMusic').get_attribute('data-audio-state')=='running';g.click('#fpsExit');g.click('#start');print('PASS input audio menu',ex,flush=True)
 g.click('#back');g.click('#shared');assert g.locator('#boardShift option').count()==10
 for ex in ['circle','front','third','bandage','magazine','moving','judgement','attention','pace','memory']:g.select_option('#boardShift',ex);assert g.locator('#boardShift').input_value()==ex
 assert not errors,errors;print('PASS seven separate hall boards no JS errors');b.close()
