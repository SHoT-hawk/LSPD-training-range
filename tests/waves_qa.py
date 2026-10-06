from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path('D:/Работа/LSPD')
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':1280,'height':800});page.goto('http://localhost:8080/')
 result=page.evaluate('''async()=>{const {chooseWave,wrap}=await import('/waves.js');let history=[],seen=new Set(),prev=[];const player={x:0,z:0,yaw:0};for(let n=0;n<1000;n++){player.yaw=n*.37;const ally=n%2?{x:0,z:7,status:'active'}:null;const pair=chooseWave(player,history,ally);for(const t of pair){const a=Math.atan2(t.x,t.z);if(Math.abs(wrap(a-player.yaw))<.3)throw Error('under crosshair');for(const old of history)if(Math.abs(wrap(a-Math.atan2(old.x,old.z)))<.25)throw Error('repeat');if(ally&&Math.abs(wrap(a))<.2)throw Error('behind ally');seen.add(Math.floor((a+Math.PI)/(Math.PI/2)));}history=[...history,...pair].slice(-4);}return {waves:1000,sectors:[...seen]};}''')
 print('PASS wave placement',result)
 src=(R/'app.js').read_text(encoding='utf-8')+'\nwindow.debug={state};'
 page.route('**/app.js*',lambda r:r.fulfill(body=src,content_type='application/javascript'));page.reload();page.click('#create');page.fill('#name','Visual QA');page.fill('#password','test123');page.fill('#password2','test123');page.click('button.primary');page.wait_for_selector('#trainingButton');page.click('#trainingButton');page.click('#capture');page.wait_for_timeout(200)
 page.screenshot(path=str(R/'tests/raised.png'))
 page.evaluate("debug.state.scene.state.ally.status='gone'");page.keyboard.press('Space');page.dispatch_event('#rangeCanvas','mousedown',{'button':2});page.wait_for_timeout(100);page.screenshot(path=str(R/'tests/ads.png'));page.dispatch_event('#rangeCanvas','mouseup',{'button':2})
 page.dispatch_event('#rangeCanvas','mousedown',{'button':0});page.keyboard.press('r');page.wait_for_timeout(450);assert 'ПЕРЕЗАРЯДКА' in page.inner_text('#gunStatus');ammo=page.evaluate('debug.state.scene.state.ammo');page.dispatch_event('#rangeCanvas','mousedown',{'button':0});assert page.evaluate('debug.state.scene.state.ammo')==ammo;page.screenshot(path=str(R/'tests/reload.png'));page.wait_for_timeout(1500);assert page.evaluate('debug.state.scene.state.ammo')==30
 print('PASS reload visible, blocks firing, completes and updates ammo');b.close()
