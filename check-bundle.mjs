/* Execute the actual assembled bundles against synthetic OEM modules and a fake SDK.
 * No network, browser, device, private backup, or privileged package is involved. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import vm from 'node:vm';
import {assemble,privateOutput,verifiedStock,sha} from './build.mjs';

const home=`self.fixtureHome={route:[{path:'/Launcher',component:{name:'StockHome'}},{path:'/Other',component:{name:'Other'}}]};self._V_M_={launcher:function(){return self.fixtureHome;}};`;
const saver=`self.fixtureSaver={route:[{path:'/ScreenSaver/ScreenMode',component:{name:'StockSaver'}}]};self._V_M_={'screen-saver':function(){return self.fixtureSaver;}};`;
const config={version:1,storeAppId:'164',icons:{},media:[],defaults:{home:null,saver:null}};
const bundles=assemble(Buffer.from(home),Buffer.from(saver),config);
assert.throws(()=>verifiedStock(Buffer.from(home),Buffer.from(saver),JSON.parse(fs.readFileSync(new URL('compatibility.json',import.meta.url)))));
assert.throws(()=>assemble(Buffer.from('broken {{{'),Buffer.from(saver),config));
assert.throws(()=>assemble(Buffer.from(home),Buffer.from(saver),{...config,icons:{x:'https://invalid.test/icon.png'}}));

function environment(apps=[{appId:'1',appName:'Netflix'},{appId:'2',appName:'YouTube'},{appId:'164',appName:'App Store'}],modern=false){
 const listeners=new Map(),messages=new Map(),saved=new Map(),launched=[],opened=[],timers=new Map();let timer=0,current='/Launcher';
 const K={LEFT:37,RIGHT:39,UP:38,DOWN:40,ENTER:13,BACK:8,RETURN:27,SOURCE:1000};
 const sources=Array.from({length:7},(_,i)=>({sourceId:'source-'+i,name:'Input '+i}));
 const sdk={key:{KEYMAP:K},storage:{get:k=>saved.get(k),set:(k,v)=>saved.set(k,v)},
  router:{isCurrentPathEqualTo:p=>current===p,back:()=>{current='/Launcher';}},
  message:{on:(name,fn)=>messages.set(name,fn),off:(name,fn)=>{if(messages.get(name)===fn)messages.delete(name);},emit:()=>{}},
  apc:{CMDMETHOD:modern?{LAUNCHER_RECOMMEND:52}:{REMOTECONTROL:1,KEY_INPUT_START:2},start:app=>{launched.push(app);current='/App';}},
  me:{req:module=>({getData:(key,arg)=>{
   if(key===(modern?'getAppList':'getCurrentShowApps')){
    if(modern)assert.equal(arg.sceneCode,'launcher');else assert.equal(arg,'Launcher');return {result:apps};
   }
   if(key==='getAllInputsData')return {result:sources};
   assert.equal(key,modern?'getAppInfo':'getAppInfoByAppId');assert.equal(arg.checkRange,1);
   return {result:apps.find(a=>a.appId===arg.appId)};
  },
   open:(...args)=>opened.push([module,...args]),invoke:()=>{}})}};
 const root={innerWidth:1920,Image:class{},addEventListener:()=>{},removeEventListener:()=>{},
  _V_SDK_:{vre:{SDK:function(){return sdk;}},biz:{file:{PATH:{UI:1},exists:k=>saved.has(k),readSync:k=>saved.get(k),writeSync:(k,v)=>saved.set(k,v)}}},
  document:{hidden:false,addEventListener:()=>{},removeEventListener:()=>{},body:{
   addEventListener:(name,fn)=>{if(!listeners.has(name))listeners.set(name,new Set());listeners.get(name).add(fn);},
   removeEventListener:(name,fn)=>listeners.get(name)?.delete(fn)}}};
 const context={self:root,console,Date,Array,setInterval:()=>++timer,clearInterval:()=>{},
  setTimeout:(fn,ms)=>{timers.set(++timer,{fn,ms});return timer;},clearTimeout:id=>timers.delete(id)};
 return {root,context,sdk,K,listeners,messages,saved,launched,opened,timers,setRoute:p=>current=p};
}
function instance(component){
 const result={...component.data(),$nextTick:f=>f()};
 for(const [name,method] of Object.entries(component.methods))result[name]=method.bind(result);
 return result;
}
const h=(tag,data,children)=>({tag,data,children:children||[]});
const e=environment();vm.runInNewContext(bundles['home.js'],e.context);
const registry=e.root._V_M_.launcher();
assert.equal(registry.route[1].component.name,'Other','Unrelated OEM routes must survive assembly');
const component=registry.route[0].component;assert.equal(component.name,'Launcher');
const ui=instance(component);component.mounted.call(ui);
assert.equal(component.render.call(ui,h).data.attrs.id,'owner-native-home');
assert.deepEqual(Array.from(ui.shelf(),a=>a.appId),['1','2','164']);
ui.select();assert.equal(e.launched.length,1);component.deactivated.call(ui);
e.setRoute('/Launcher');component.activated.call(ui);
assert.equal(ui.view,'home');assert.equal(ui._running,true);
ui.show('inputs');ui.index=1;ui.handleKey(e.K.DOWN);assert.equal(ui.index,5);ui.handleKey(e.K.UP);assert.equal(ui.index,1);
ui.show('home');ui.index=0;
for(const fn of e.listeners.get('key-down'))fn({keyCode:e.K.ENTER,stopPropagation(){}});
[...e.timers.values()].find(t=>t.ms===650).fn();
for(const fn of e.listeners.get('key-up'))fn({keyCode:e.K.ENTER,stopPropagation(){}});
assert.equal(ui.actionApp.appId,'1');assert.equal(e.launched.length,1,'Long OK does not launch');
ui.actionIndex=1;ui.select();assert.equal(ui.apps.length,3);assert.equal(ui.shelf().at(-1).appId,'164');
ui.show('savers');ui.index=0;ui.select();assert.equal(e.opened.length,0,'Empty media cannot launch a blank custom saver');
assert.match(ui.status,/Video/);component.beforeDestroy.call(ui);
assert.equal(e.listeners.get('key-down').size,0);assert.equal(e.listeners.get('key-up').size,0);
assert.equal(e.messages.size,0);

// A new user may have no Netflix or other preferred regional apps.
const local=environment([{appId:'30',appName:'Local Movies'},{appId:'164',appName:'App Store'}]);
vm.runInNewContext(bundles['home.js'],local.context);
const localComponent=local.root._V_M_.launcher().route[0].component,localUI=instance(localComponent);
localComponent.mounted.call(localUI);
assert.deepEqual(Array.from(localUI.shelf(),a=>a.appId),['30','164']);
localComponent.beforeDestroy.call(localUI);

// A different SDK is an explicit, reviewed port, not a model/chip heuristic.
const modernConfig={...config,storeAppId:null};
const modernBundle=assemble(Buffer.from(home),null,modernConfig,
 {homeOnly:true,adapter:'app-list-v1',assetBase:'file:///native/local/clean-home/',excludedAppIds:[]});
assert.deepEqual(Object.keys(modernBundle),['home.js'],'First port preserves the original saver');
assert.throws(()=>assemble(Buffer.from(home),null,modernConfig,{homeOnly:true,adapter:'guessed-chip'}));
assert.throws(()=>assemble(Buffer.from(home),null,modernConfig,{homeOnly:true,assetBase:'https://invalid.test/'}));
const modern=environment([{appId:'206',appName:'Local Library',openMode:4,skipCheck:true,skipPin:true}],true);
vm.runInNewContext(modernBundle['home.js'],modern.context);
const mc=modern.root._V_M_.launcher().route[0].component,mu=instance(mc);mc.mounted.call(mu);
assert.equal(mu.view,'home','Missing optional input-launch constant must not redirect ordinary Home');
assert.deepEqual(Array.from(mu.shelf(),a=>a.appId),['206'],'Do not inherit another owner\'s hidden ID or invent Store');
mu.select();assert.equal(modern.launched[0].startMethod,52);assert.equal(modern.launched[0].storeType,4);
assert.equal('skipPin' in modern.launched[0],false);assert.equal('skipCheck' in modern.launched[0],false);
modern.root.AlvidaaNativePlatform(modern.sdk,()=>{}).openSettings();
assert.equal(JSON.stringify(modern.opened.at(-1)),JSON.stringify(['setting','settings']));
assert.equal(modern.root.OwnerAssetBase,'file:///native/local/clean-home/');mc.beforeDestroy.call(mu);
const wrong=environment();vm.runInNewContext(modernBundle['home.js'],wrong.context);
assert.equal(wrong.root._V_M_.launcher().route[0].component.name,'StockHome','Missing reviewed SDK keeps OEM Home');
const mismatch=environment([{appId:'1',appName:'Example'}],true);vm.runInNewContext(modernBundle['home.js'],mismatch.context);
const platform=mismatch.root.AlvidaaNativePlatform(mismatch.sdk,()=>{});platform.start();
mismatch.sdk.me.req=()=>({getData:()=>({result:{appId:'different',appName:'Wrong'}})});
assert.throws(()=>platform.launchApp('1'));assert.throws(()=>platform.launchApp('999'));
assert.equal(mismatch.launched.length,0);platform.stop();

// Missing/throwing SDK retains the original vendor module rather than replacing it.
for(const makeBad of [r=>{delete r._V_SDK_;},r=>{r._V_SDK_.vre.SDK=function(){throw Error('unsupported SDK');};}]){
 const bad=environment();makeBad(bad.root);vm.runInNewContext(bundles['home.js'],bad.context);
 assert.equal(bad.root._V_M_.launcher().route[0].component.name,'StockHome');
}
const none=environment();vm.runInNewContext(bundles['saver.js'],none.context);
assert.equal(none.root._V_M_['screen-saver']().route[0].component.name,'StockSaver','No custom media preserves original saver');

const animated={...config,media:[{id:'one',label:'Example',video:'one.mp4',poster:'one.jpg',cycle:10}],defaults:{home:'one',saver:'one'}};
const animatedBundle=assemble(Buffer.from(home),Buffer.from(saver),animated)['saver.js'];
const se=environment();vm.runInNewContext(animatedBundle,se.context);
const sc=se.root._V_M_['screen-saver']().route[0].component;
const su=instance(sc);assert.equal(sc.render.call(su,h).data.attrs.id,'owner-native-saver');

const temp=fs.mkdtempSync(path.join(os.tmpdir(),'vidaa-path-test-'));
try{
 const p=path.join(temp,'.private');assert.equal(privateOutput(path.join(p,'build'),p),path.join(p,'build'));
 assert.throws(()=>privateOutput(path.join(temp,'public'),p));
 fs.mkdirSync(p);fs.symlinkSync(path.join(temp,'missing'),path.join(p,'linked'));
 assert.throws(()=>privateOutput(path.join(p,'linked','build'),p));
 fs.unlinkSync(path.join(p,'linked'));fs.rmdirSync(p);fs.symlinkSync(path.join(temp,'missing'),p);
 assert.throws(()=>privateOutput(path.join(p,'build'),p));
}finally{fs.rmSync(temp,{recursive:true,force:true});}
console.log('PASS: assembled Home/app/Home, grid, long OK, Store, empty media, nonpreferred apps, SDK failure fallback, saver assembly, private symlink rejection. Synthetic fixtures only.');
