from pathlib import Path
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();g=b.new_page();g.goto('http://localhost:8080/');s=g.request.get('http://localhost:8080/styles.css').text();assert "ready-or-not-background.jpg" not in s,'restricted Steam background must not be active in distributed redesign';print('PASS original public backdrop');b.close()
