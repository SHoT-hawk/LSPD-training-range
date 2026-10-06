from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/')
 g.evaluate("""async()=>{let m=await import('/range.js');window.r=m.mountRange(document.querySelector('#app'),{exercise:'circle',onExit:()=>{},onFinish:()=>{}});document.querySelector('#capture').click();r.state.raised=false;r.state.ally.status='gone';r.state.targets=[]} """)
 g.locator('#rangeCanvas').dispatch_event('mousedown',{'button':0});g.wait_for_timeout(100)
 assert 'Промах' in g.inner_text('#gunStatus'),'first/second shifts must explain a missed fired shot'
 print('PASS live miss feedback');b.close()
