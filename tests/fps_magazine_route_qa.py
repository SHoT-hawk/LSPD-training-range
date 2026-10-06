from pathlib import Path
s=Path(__file__).with_name('fps_generated_route_qa.py').read_text(encoding='utf8').replace("exercise:'bandage'","exercise:'magazine'")
exec(compile(s,'generated-magazine-route','exec'))
