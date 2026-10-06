import asyncio,json
from pathlib import Path
import edge_tts
ROOT=Path('D:/Работа/LSPD/assets/voices')
LINES={
 'start':('alvarez','Начинаем. Следи за мишенями и за тем, кто рядом.'),
 'pair':('alvarez','Новая пара. Осмотрись, затем открывай огонь.'),
 'triple':('alvarez','Есть. Теперь спокойно перенеси оружие.'),
 'unsafe':('partner','Ствол убери! Я не могу так работать.'),
 'friendly':('partner','Прекратить огонь! Ты попал в своего!'),
 'wound':('partner','Ты ранен! Найди укрытие и перевяжись.'),
 'cover':('partner','Здесь тебя видно! Сначала уйди за укрытие.'),
 'heal':('partner','Перевязка закончена. Я прикрываю.'),
 'reload':('partner','Магазин установлен. Готова.'),
 'check':('alvarez','Вспомни, сколько патронов осталось в магазине.'),
 'decision':('alvarez','Верное решение. Мирные не пострадали.'),
 'room':('alvarez','Не спеши входить. Осмотри комнату из-за проёма.'),
 'light':('partner','Свет включён.'),
 'dark':('partner','Свет выключен.'),
}
async def main():
 ROOT.mkdir(parents=True,exist_ok=True)
 for key,(role,text) in LINES.items():
  path=ROOT/(key+'.mp3')
  if not path.exists():
   await edge_tts.Communicate(text,'ru-RU-DmitryNeural' if role=='alvarez' else 'ru-RU-SvetlanaNeural',rate='-8%' if role=='alvarez' else '+2%').save(str(path))
  print(key,path.stat().st_size,flush=True)
 (ROOT/'manifest.json').write_text(json.dumps({k:{'role':r,'text':t,'file':k+'.mp3'} for k,(r,t) in LINES.items()},ensure_ascii=False,indent=2),encoding='utf8')
asyncio.run(main())
