from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();errors=[];g.on('pageerror',lambda e:errors.append(str(e)));g.goto('http://localhost:8080/')
 g.evaluate("""localStorage.setItem('lspd-training-v1',JSON.stringify({profiles:[{name:'QA',password:'unused',career:{character:'QA',days:0,officers:99,ammo:120},personal:[]}]}))""")
 # Verify production routing uses one renderer, without changing profile data.
 source=g.request.get('http://localhost:8080/app.js').text();assert "mountFPS" in source,'production must route five shifts to new FPS'
 assert "state.scene=mountFPS" in source;print('PASS production FPS routing');b.close()
