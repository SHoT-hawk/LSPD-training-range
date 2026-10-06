from pathlib import Path
from playwright.sync_api import sync_playwright
# Reuse the real-input route pilot, with magazine decisions inserted before each sector/contact.
s=Path(__file__).with_name('fps_route_qa.py').read_text(encoding='utf8').replace("exercise:'bandage'","exercise:'magazine'")
s=s.replace("s=g.evaluate('game.state');\n  if s['raised']", "s=g.evaluate('game.state');\n  if not s['inspect']:\n   g.keyboard.down('r');g.wait_for_timeout(600);g.keyboard.up('r')\n  if s['ammo']<6 and s['sectorShots']==0 or s['ammo']<2:\n   g.keyboard.press('r');g.wait_for_timeout(1600);g.keyboard.down('r');g.wait_for_timeout(600);g.keyboard.up('r')\n  if s['raised']")
exec(compile(s,'magazine-real-route','exec'))
