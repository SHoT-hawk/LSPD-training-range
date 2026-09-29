// A short synthesized shot; no third-party recording or network dependency.
let context;
export function playShot(){
 try {
  context ||= new (window.AudioContext || window.webkitAudioContext)();
  if(context.state==='suspended') context.resume();
  const now=context.currentTime;
  const noise=context.createBuffer(1,Math.floor(context.sampleRate*.16),context.sampleRate);
  const samples=noise.getChannelData(0);
  for(let i=0;i<samples.length;i++) samples[i]=(Math.random()*2-1)*Math.exp(-i/(context.sampleRate*.032));
  const source=context.createBufferSource();source.buffer=noise;
  const lowpass=context.createBiquadFilter();lowpass.type='lowpass';lowpass.frequency.value=2600;
  const gain=context.createGain();gain.gain.setValueAtTime(.24,now);gain.gain.exponentialRampToValueAtTime(.001,now+.16);
  source.connect(lowpass).connect(gain).connect(context.destination);
  source.start(now);source.stop(now+.16);
  const thump=context.createOscillator(),body=context.createGain();thump.type='triangle';
  thump.frequency.setValueAtTime(145,now);thump.frequency.exponentialRampToValueAtTime(55,now+.11);
  body.gain.setValueAtTime(.25,now);body.gain.exponentialRampToValueAtTime(.001,now+.12);
  thump.connect(body).connect(context.destination);thump.start(now);thump.stop(now+.12);
 } catch(error) { console.warn('Звук выстрела недоступен:',error); }
}
