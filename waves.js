export const wrap=a=>Math.atan2(Math.sin(a),Math.cos(a));
export function chooseWave(player,history=[],ally=null,rng=Math.random){
 const candidates=[];
 for(let i=0;i<36;i++){
  const a=i*Math.PI/18, p={x:Math.sin(a)*12,y:1.5,z:Math.cos(a)*12,hits:0};
  const bearing=Math.atan2(p.x-player.x,p.z-player.z);
  if(Math.abs(wrap(bearing-player.yaw))<.3)continue;
  if(history.some(o=>Math.hypot(p.x-o.x,p.z-o.z)<3||Math.abs(wrap(bearing-Math.atan2(o.x-player.x,o.z-player.z)))<.25))continue;
  if(ally&&ally.status==='active'&&Math.abs(wrap(bearing-Math.atan2(ally.x-player.x,ally.z-player.z)))<.2)continue;
  candidates.push(p);
 }
 if(candidates.length<2)throw new Error('Нет безопасной схемы');
 const first=candidates.splice(Math.floor(rng()*candidates.length),1)[0];
 const separated=candidates.filter(p=>Math.abs(wrap(Math.atan2(p.x-player.x,p.z-player.z)-Math.atan2(first.x-player.x,first.z-player.z)))>=.55);
 const close=separated.filter(p=>Math.hypot(p.x-first.x,p.z-first.z)<9);
 const pool=rng()<.5&&close.length?close:separated;
 return [first,pool[Math.floor(rng()*pool.length)]];
}
