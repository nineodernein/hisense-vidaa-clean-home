import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {validateConfig,verifiedStock,sha} from './build.mjs';
const sources=['native-platform.js','native-core.js','native-dock.js','native-actions.js','native-media.js','native-video.js','native-saver.js','native-entry.js'];
for(const name of sources)new vm.Script(fs.readFileSync(new URL(name,import.meta.url),'utf8'),{filename:name});
const good={version:1,storeAppId:'164',icons:{},media:[],defaults:{home:null,saver:null}};
assert.deepEqual(validateConfig({...good,privateField:'must not export'}),good);
for(const config of [
 {...good,icons:{'1':'https://invalid.test/x.png'}},
 {...good,icons:{'1':'../outside.png'}},
 {...good,media:[{id:'a',label:'A',video:'a.mp4',poster:'a.jpg',cycle:0}]},
 {...good,defaults:{home:'missing',saver:null}}
])assert.throws(()=>validateConfig(config));
assert.throws(()=>verifiedStock(Buffer.from('unknown'),Buffer.from('unknown'),JSON.parse(fs.readFileSync(new URL('compatibility.json',import.meta.url)))));
verifiedStock(Buffer.from('fixture-home'),Buffer.from('fixture-saver'),{stock:{home:sha('fixture-home'),saver:sha('fixture-saver')}});

// Private-media choices remain independent; malformed persisted data falls back.
let persisted=null;const cfg={...good,media:[{id:'one',label:'One',video:'one.mp4',poster:'one.jpg',cycle:11},{id:'two',label:'Two',video:'two.mp4',poster:'two.jpg',cycle:14}],defaults:{home:'one',saver:'two'}};
const root={CleanHomeConfig:cfg,_V_SDK_:{biz:{file:{PATH:{UI:1},exists:()=>persisted!==null,readSync:()=>persisted,writeSync:(n,v)=>{persisted=v;}}}}};
const mediaCode=fs.readFileSync(new URL('native-media.js',import.meta.url),'utf8');
vm.runInNewContext(mediaCode,{self:root});root.OwnerMedia.select('home','two');root.OwnerMedia.select('saver','one');
assert.equal(root.OwnerMedia.selected('home').id,'two');assert.equal(root.OwnerMedia.selected('saver').id,'one');
assert.throws(()=>root.OwnerMedia.select('home','../../outside'));
delete root.OwnerMedia;vm.runInNewContext(mediaCode,{self:root});assert.equal(root.OwnerMedia.selected('saver').id,'one');

// Native dock keyboard/favorites using a fake vendor SDK; no TV or browser.
const listeners={};const timers=new Map();let tid=0;const launched=[];const saved=new Map();
const apps=[{appId:'1',appName:'Netflix'},{appId:'2',appName:'YouTube'},{appId:'164',appName:'App Store'}];
const inputs=Array.from({length:7},(_,i)=>({sourceId:'input-'+i,name:'Input '+i}));
const K={LEFT:37,RIGHT:39,UP:38,DOWN:40,ENTER:13,BACK:8,RETURN:27,SOURCE:1000};
const sdk={key:{KEYMAP:K},storage:{get:k=>saved.get(k),set:(k,v)=>saved.set(k,v)},router:{isCurrentPathEqualTo:()=>true},
 message:{on:()=>{},off:()=>{},emit:()=>{}},
 apc:{CMDMETHOD:{REMOTECONTROL:1,KEY_INPUT_START:2},start:a=>launched.push(a)},
 me:{req:module=>({getData:(key,arg)=>({result:key==='getCurrentShowApps'?apps:key==='getAllInputsData'?inputs:apps.find(a=>a.appId===arg.appId)}),open:()=>{},invoke:()=>{}})}};
root.innerWidth=1920;root.Image=class{};root.OwnerVideo=()=>({start:()=>{},stop:()=>{}});
root.addEventListener=()=>{};root.removeEventListener=()=>{};
root.document={hidden:false,addEventListener:()=>{},removeEventListener:()=>{},body:{
 addEventListener:(name,fn)=>{(listeners[name]||=new Set()).add(fn);},
 removeEventListener:(name,fn)=>listeners[name]?.delete(fn)
}};
const context={self:root,setTimeout:(fn,ms)=>{timers.set(++tid,{fn,ms});return tid;},clearTimeout:id=>timers.delete(id),setInterval:()=>++tid,clearInterval:()=>{},Date,Array,console};
for(const name of ['native-platform.js','native-core.js','native-dock.js','native-actions.js'])vm.runInNewContext(fs.readFileSync(new URL(name,import.meta.url),'utf8'),context);
const component=root.AlvidaaFreeMyTV(sdk),instance={...component.data(),$nextTick:f=>f()};
for(const [k,v] of Object.entries(component.methods))instance[k]=v.bind(instance);
instance.start();assert.equal(instance.shelf().at(-1).appId,'164');
instance.show('inputs');instance.index=1;instance.handleKey(K.DOWN);assert.equal(instance.index,5);instance.handleKey(K.UP);assert.equal(instance.index,1);
instance.index=3;instance.handleKey(K.DOWN);assert.equal(instance.index,6,'Last incomplete row clamps');
instance.show('home');instance.index=0;
const event=code=>({keyCode:code,stopPropagation(){}});
for(const fn of listeners['key-down'])fn(event(K.ENTER));
const hold=[...timers.values()].find(t=>t.ms===650);assert(hold);hold.fn();
for(const fn of listeners['key-up'])fn(event(K.ENTER));
assert.equal(instance.actionApp.appId,'1');assert.equal(launched.length,0,'Holding OK must not also launch');
instance.actionIndex=1;instance.select();assert.equal(instance.apps.length,3,'Only favorite removed, not installed app');
assert(!instance.shelf().some(a=>a.appId==='1'));assert.equal(instance.shelf().at(-1).appId,'164');
instance.favorites=['1','2'];instance.index=0;instance.beginMove();instance.handleKey(K.RIGHT);
assert.equal(instance.favoriteApps()[0].appId,'2');instance.handleKey(K.BACK);assert.equal(instance.favoriteApps()[0].appId,'1');
instance.stop();assert.equal(listeners['key-up'].size,0);

// Stock factory fallback: unsupported/missing SDK retains original component.
const stock={route:[{path:'/Launcher',component:{name:'Stock'}}]};
const fallback={_V_M_:{launcher:()=>stock}};
vm.runInNewContext(fs.readFileSync(new URL('native-entry.js',import.meta.url),'utf8'),{self:fallback});
assert.equal(fallback._V_M_.launcher().route[0].component.name,'Stock');
console.log('PASS: syntax, hash/config rejection, private-field exclusion, media persistence, dock grid, long OK, favorites, cancellation, Store, stock fallback.');

await import('./check-video.cjs');
