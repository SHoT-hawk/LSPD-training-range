# Current generator replaces the fixed map; exercise the new real-input route.
from pathlib import Path
exec(compile(Path(__file__).with_name('fps_generated_route_qa.py').read_text(encoding='utf8'),'generated-bandage-route','exec'))
