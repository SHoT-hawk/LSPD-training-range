from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/');g.evaluate("async()=>{let m=await import('/fps-game.js');window.game=m.mountFPS(document.querySelector('#app'),{exercise:'front'})}");g.click('#fpsStart');g.wait_for_timeout(70)
 def lum():return g.evaluate("()=>{let d=document.querySelector('#fpsCanvas').getContext('2d').getImageData(270,80,100,160).data,n=0;for(let i=0;i<d.length;i+=4)n+=d[i]+d[i+1]+d[i+2];return n/d.length}")
 before=lum();g.keyboard.press('f');g.wait_for_timeout(70);after=lum();assert after>before*1.2,(before,after);print('PASS flashlight visible pixel brightness',before,after);b.close()
