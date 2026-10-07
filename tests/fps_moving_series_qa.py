from pathlib import Path
s=Path('D:/Работа/LSPD/tests/fps_generated_route_qa.py').read_text(encoding='utf8').replace("exercise:'bandage'","exercise:'moving'")
exec(compile(s,'moving-maze-route','exec'))
