// Third shift is deliberately isolated from localStorage: the parent records the final result.
import {playShot} from './shot-sound.js';
export function mountThird(host,{officers=99,flashlightBinding='KeyF',onExit,onFinish}) {
 const root=document.createElement('section');root.className='training third';
 root.innerHTML=`<canvas id="thirdCanvas" tabindex="0"></canvas><div class="third-top" id="thirdStats"></div><button id="thirdExit">В меню</button><div class="third-brief"><img src="assets/alvarez-portrait.png" alt="Гало Альварес"><div><b>ТРЕТЬЯ СМЕНА · АЛЬВАРЕС</b><p id="thirdInstruction"></p></div></div><div class="third-bottom" id="thirdStatus"></div><button id="thirdCapture">Нажмите, чтобы начать · Esc — освободить мышь</button>`;
 host.replaceChildren(root);
 const canvas=root.querySelector('canvas'),ctx=canvas.getContext('2d'),instruction=root.querySelector('#thirdInstruction'),capture=root.querySelector('#thirdCapture');
 const lightKey=flashlightBinding,mouseLight=/^Mouse[0-4]$/.test(lightKey);
 const label=mouseLight?`кнопка мыши ${Number(lightKey.slice(5))+1}`:lightKey.replace(/^Key/,'');
 const s={stage:0,series:0,points:0,grouping:0,resign:0,killed:0,ammo:30,reserve:90,raised:true,lean:null,ads:false,light:false,yaw:-.25,pitch:0,recoil:0,reload:0,elapsed:0,active:false,done:false,transferCrossed:false,hits:[[],[]],error:'',flashlightBinding:lightKey};
 const abort=new AbortController(),opts={signal:abort.signal};let raf,last=performance.now(),transferStart=null;
 const targets=[{x:-2.5,z:11},{x:2.5,z:11}],ally={x:0,z:7};
 const earned=new Set();
 function award(name){if(!earned.has(name)){earned.add(name);s.points+=10;}}
 function hint(text=''){s.error=text;brief();}
 function brief(){
  const cue=s.hits[0].length<3 ?
   `ЛЕВАЯ ${s.hits[0].length}/3: Q — выглянуть, пробел — опустить ствол, ПКМ — прицел, свет — включить, затем стреляйте.`:
   s.hits[1].length<3 ?
   `ПРАВАЯ ${s.hits[1].length}/3: поднимите ствол пробелом, безопасно переведите его мимо напарника, E — выгляните (E сразу сменяет Q), опустите ствол, прицельтесь и стреляйте со светом.`:
   'Обе тройки готовы: выключите свет, выпрямитесь и поднимите ствол, чтобы завершить серию.';
  instruction.textContent=`${s.error?s.error+' ':''}${cue} Фонарик: ${label}. ${lightKey==='Mouse0'?'Стрельба — Enter. ':''}${lightKey==='Mouse2'?'Прицел — Shift. ':''}${['KeyQ','KeyE','Space','KeyR'].includes(lightKey)?'Основное действие на назначенной клавише — Ctrl+клавиша. ':''}Промах не обнуляет попадания; опасный перенос сбрасывает только текущую серию.`;
 }
 function status(){root.querySelector('#thirdStats').textContent=`${Math.max(0,90-s.elapsed).toFixed(1)} с · Полных серий ${s.series} · Очков ${s.points} · Сотрудников ${Math.max(0,officers-s.resign-s.killed)}`;root.querySelector('#thirdStatus').textContent=`${s.raised?'СТВОЛ ПОДНЯТ':'СТВОЛ ГОТОВ'} · ${s.lean==='left'?'ВЫГЛЯДЫВАЕТ ВЛЕВО':s.lean==='right'?'ВЫГЛЯДЫВАЕТ ВПРАВО':'ПРЯМО'} · ${s.ads?'ПРИЦЕЛ ВКЛ':'БЕЗ ПРИЦЕЛА'} · СВЕТ ${s.light?'ВКЛ':'ВЫКЛ'} (${label}) · ${s.reload?'ПЕРЕЗАРЯДКА '+s.reload.toFixed(1)+' с · ':''}В оружии ${s.ammo}/30 · Запас ${s.reserve}`;}
 function reset(why){s.stage=0;s.hits=[[],[]];s.lean=null;s.ads=false;s.light=false;s.raised=true;s.yaw=-.25;s.pitch=0;s.recoil=0;s.transferCrossed=false;transferStart=null;earned.clear();hint(why+' Текущая серия сначала, очки остаются.');}
 function complete(){s.points+=100;s.series++;s.stage=0;s.hits=[[],[]];s.lean=null;s.ads=false;s.light=false;s.raised=true;s.yaw=-.25;s.pitch=0;s.transferCrossed=false;transferStart=null;earned.clear();hint('Серия завершена!');}
 function maybeComplete(){if(s.hits[1].length===3&&!s.lean&&s.raised&&!s.light)complete();}
 function dispose(){s.done=true;abort.abort();cancelAnimationFrame(raf);if(document.pointerLockElement===canvas)document.exitPointerLock();}
 function finish(reason){if(s.done)return;dispose();onFinish({reason,duration:s.elapsed,destroyed:s.series*2,resign:s.resign,killed:s.killed,series:s.series,points:s.points,grouping:s.grouping});}
 root.querySelector('#thirdExit').onclick=()=>{dispose();onExit();};
 capture.onclick=()=>{s.active=true;last=performance.now();capture.hidden=true;canvas.focus();canvas.requestPointerLock?.().catch(()=>{});};
 document.addEventListener('pointerlockchange',()=>{if(document.pointerLockElement!==canvas&&!s.done){s.active=false;s.ads=false;capture.hidden=false;capture.textContent='Продолжить';}},opts);
 window.addEventListener('blur',()=>{s.active=false;s.ads=false;capture.hidden=false;},opts);
 function light(){s.light=!s.light;if(s.light)award(s.hits[0].length<3?'lightLeft':'lightRight');hint(s.light?'Свет включён.':'Свет выключен.');maybeComplete();}
 function action(code){
  if(code==='KeyR'){if(s.ammo<30&&s.reserve&&!s.reload){s.reload=1.6;s.ads=false;}return;}
  if(code==='KeyQ'||code==='KeyE'){
   const side=code==='KeyQ'?'left':'right',expected=s.hits[0].length<3?'left':'right';
   if(s.lean===side){s.lean=null;s.ads=false;award(side+'straight');hint('Выпрямились.');maybeComplete();return;}
   if(s.lean){s.lean=side;s.ads=false;if(side!==expected){hint('Переключились напрямую, но сейчас работаем с '+(expected==='left'?'левой':'правой')+' мишенью.');return;}if(side==='right'&&!s.transferCrossed){hint('Переключились вправо. Поднимите ствол и безопасно переведите его мимо напарника перед стрельбой.');return;}award(side+'lean');s.stage=side==='left'?1:8;hint();return;}
   if(side!==expected){hint('Сейчас работаем с '+(expected==='left'?'левой':'правой')+' мишенью.');return;}
   if(side==='right'&&!s.transferCrossed){hint('Сначала поднимите ствол и безопасно переведите его мимо напарника.');return;}
   s.lean=side;award(side+'lean');s.stage=side==='left'?1:8;hint();return;
  }
  if(code==='Space'){
   s.raised=!s.raised;s.ads=false;
   if(s.raised){if(s.hits[0].length===3&&s.hits[1].length<3){transferStart=Math.sign(angle(ally))||1;award('transferRaise');}else if(s.hits[1].length===3)award('finishRaise');hint('Ствол поднят.');}
   else{if(s.lean==='left')award('leftReady');if(s.lean==='right')award('rightReady');hint('Ствол готов.');}
   maybeComplete();return;
  }
 }
 window.addEventListener('keydown',e=>{if(!s.active||s.done||e.repeat)return;const isAction=['KeyQ','KeyE','Space','KeyR'].includes(e.code),reserved=e.code===lightKey;
  if(reserved||isAction||e.code==='Enter'||e.code==='ShiftLeft'||e.code==='ShiftRight')e.preventDefault();
  if(reserved&&!(isAction&&e.ctrlKey)){light();return;}
  if(isAction){action(e.code);return;}
  if(e.code==='Enter'&&lightKey==='Mouse0')fire();
  if((e.code==='ShiftLeft'||e.code==='ShiftRight')&&lightKey==='Mouse2')startAim();
 },opts);
 window.addEventListener('keyup',e=>{if(['ShiftLeft','ShiftRight'].includes(e.code)&&lightKey==='Mouse2')s.ads=false;},opts);
 function startAim(){if(s.raised){hint('Сначала пробел — опустить поднятый ствол; прицел сам этого не делает.');return;}if((s.lean==='left'&&s.hits[0].length<3)||(s.lean==='right'&&s.transferCrossed&&s.hits[0].length===3&&s.hits[1].length<3)){s.ads=true;award(s.lean+'aim');s.stage=s.lean==='left'?2:9;hint();}else hint('Выгляните в сторону текущей мишени.');}
 canvas.addEventListener('mousedown',e=>{if(!s.active)return;e.preventDefault();if(`Mouse${e.button}`===lightKey){light();return;}if(e.button===2){startAim();return;}if(e.button===0)fire();},opts);
 window.addEventListener('mouseup',e=>{if(e.button===2&&lightKey!=='Mouse2')s.ads=false;},opts);
 canvas.addEventListener('contextmenu',e=>e.preventDefault(),opts);
 function angle(o){return Math.atan2(o.x,o.z)-s.yaw;}
 function project(o){const a=angle(o),depth=Math.hypot(o.x,o.z)*Math.cos(a);if(depth<=.1)return null;const f=canvas.height*(s.ads?.96:.7),offset=s.lean==='left'?canvas.width*.06:s.lean==='right'?-canvas.width*.06:0;return {x:canvas.width/2+Math.tan(a)*f+offset,y:canvas.height*.52+s.pitch*f,k:f/depth};}
 function collision(o,w,h){const p=project(o);return !!p&&Math.abs(p.x-canvas.width/2)<w*p.k/2&&Math.abs(p.y-canvas.height/2)<h*p.k/2;}
 function fire(){if(s.raised||s.reload||!s.ammo){hint('Оружие не готово или магазин пуст.');return;}
  s.ammo--;playShot();const struckAlly=collision(ally,1.6,2.5),side=s.hits[0].length<3?0:1,valid=s.lean===(side===0?'left':'right')&&s.ads&&s.light&&(side===0||s.transferCrossed),struckTarget=valid&&collision(targets[side],.9,1.4),projected=struckTarget?project(targets[side]):null;
  s.recoil=Math.min(.32,s.recoil+.18);s.pitch=Math.min(.35,s.pitch+.035);
  if(struckAlly){s.killed++;s.resign+=Math.min(2,Math.max(0,officers-s.killed-s.resign));reset('Попали в напарника: один погиб, ещё двое увольняются.');return;}
  if(!valid){hint('Для зачёта выстрела: нужная сторона, опущенный ствол, прицел и включённый свет.');return;}
  if(!struckTarget){hint('Промах: патрон потрачен, попадания сохраняются.');return;}
  const hit={x:(projected.x-canvas.width/2)/(projected.k*.9),y:(projected.y-canvas.height/2)/(projected.k*1.4)};s.hits[side].push(hit);s.points+=15;s.stage=side===0?3:10;
  if(s.hits[side].length===3){const hits=s.hits[side],spread=Math.max(...hits.flatMap(a=>hits.map(b=>Math.hypot(a.x-b.x,a.y-b.y))));const bonus=Math.max(0,Math.round(40-80*spread));s.grouping+=bonus;s.points+=bonus;s.stage=side===0?6:13;hint(side===0?'Левая тройка готова. Поднимите ствол перед переводом.':'Правая тройка готова. Выпрямитесь, поднимите ствол и выключите свет.');maybeComplete();}
  else hint(`Попадание ${s.hits[side].length}/3. Верните прицел на мишень после отдачи.`);
 }
 canvas.addEventListener('mousemove',e=>{if(!s.active)return;const prior=angle(ally);s.yaw+=e.movementX*.002*(s.ads?.55:1);s.pitch=Math.max(-.35,Math.min(.35,s.pitch-e.movementY*.002));const next=angle(ally);
  if(s.hits[0].length===3&&s.hits[1].length<3&&!s.transferCrossed&&Math.sign(prior)!==Math.sign(next)){
   if(!s.raised){s.resign++;reset('Перенесли неподнятый ствол мимо напарника: он увольняется.');}
   else{s.transferCrossed=true;award('safeTransfer');s.stage=s.lean==='right'?8:7;hint('Безопасный перевод выполнен. Теперь правая мишень.');}
  }
 },opts);
 function render(){canvas.width=root.clientWidth;canvas.height=root.clientHeight;ctx.fillStyle='#141f28';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.fillStyle='#303838';ctx.fillRect(0,canvas.height*.55,canvas.width,canvas.height*.45);ctx.strokeStyle='#5c6866';for(let i=-10;i<=10;i+=2){ctx.beginPath();ctx.moveTo(canvas.width/2+i*canvas.width*.04,canvas.height*.55);ctx.lineTo(canvas.width/2+i*canvas.width*.15,canvas.height);ctx.stroke();}
  for(let i=0;i<2;i++){const p=project(targets[i]);if(!p)continue;const w=p.k*.9,h=p.k*1.4;ctx.fillStyle='#d8cdb8';ctx.fillRect(p.x-w/2,p.y-h/2,w,h);ctx.strokeStyle='#292b2b';ctx.strokeRect(p.x-w/2,p.y-h/2,w,h);ctx.fillStyle='#1b1f23';ctx.beginPath();ctx.ellipse(p.x,p.y,w*.17,h*.3,0,0,Math.PI*2);ctx.fill();ctx.fillStyle='#fff';ctx.font='16px sans-serif';ctx.fillText((i?'ПРАВАЯ ':'ЛЕВАЯ ')+s.hits[i].length+'/3',p.x-w/2,p.y-h/2-10);}
  const p=project(ally);if(p){const w=p.k*.85,h=p.k*1.7;ctx.fillStyle='#42627b';ctx.fillRect(p.x-w/2,p.y-h/2,w,h);ctx.fillStyle='#d2a98a';ctx.beginPath();ctx.arc(p.x,p.y-h*.52,w*.37,0,Math.PI*2);ctx.fill();ctx.fillStyle='white';ctx.font='16px sans-serif';ctx.fillText('НАПАРНИК',p.x-w/2,p.y+h/2+20);}
  if(s.light){const gradient=ctx.createRadialGradient(canvas.width/2,canvas.height/2,20,canvas.width/2,canvas.height/2,canvas.height*.65);gradient.addColorStop(0,'#fff8c350');gradient.addColorStop(1,'#fff8c300');ctx.fillStyle=gradient;ctx.fillRect(0,0,canvas.width,canvas.height);}
  ctx.save();ctx.translate(canvas.width*(s.ads?.5:s.raised?.77:.62),canvas.height*(s.raised?.64:.89)+s.recoil*190);ctx.rotate(-s.recoil*.35);ctx.fillStyle='#15191b';ctx.fillRect(-20,-170,40,270);ctx.fillStyle='#485259';ctx.fillRect(-34,-100,68,126);ctx.fillStyle='#12171a';ctx.fillRect(-8,-255,16,100);ctx.restore();if(s.ads&&!s.raised){ctx.strokeStyle='#fff';ctx.beginPath();ctx.moveTo(canvas.width/2-8,canvas.height/2);ctx.lineTo(canvas.width/2+8,canvas.height/2);ctx.moveTo(canvas.width/2,canvas.height/2-8);ctx.lineTo(canvas.width/2,canvas.height/2+8);ctx.stroke();}status();
 }
 function loop(now){if(s.done)return;const dt=Math.min((now-last)/1000,.05);last=now;if(s.active){s.elapsed+=dt;s.recoil*=Math.exp(-dt*8);if(s.reload){s.reload=Math.max(0,s.reload-dt);if(!s.reload){const count=Math.min(30-s.ammo,s.reserve);s.ammo+=count;s.reserve-=count;}}if(s.elapsed>=90||s.ammo+s.reserve===0||officers-s.resign-s.killed<=0){finish(s.elapsed>=90?'time_limit':s.ammo+s.reserve===0?'ammo_depleted':'no_officers');return;}}render();raf=requestAnimationFrame(loop);}
 brief();raf=requestAnimationFrame(loop);return {state:s,dispose};
}
