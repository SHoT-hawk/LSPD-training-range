from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/');g.evaluate("""async()=>{let m=await import('/third-day.js');window.scene=m.mountThird(document.querySelector('#app'),{onExit:()=>{},onFinish:()=>{}});document.querySelector('#thirdCapture').click();scene.state.raised=false;scene.state.lean='left';scene.state.ads=true;scene.state.light=true;}""");before=g.evaluate('scene.state.ammo');g.locator('#thirdCanvas').dispatch_event('mousedown',{'button':0});assert g.evaluate('scene.state.ammo')==before-1
 assert 'Промах' in g.inner_text('#thirdInstruction'),'third shift must explain off-target miss'
 print('PASS third miss feedback');b.close()
