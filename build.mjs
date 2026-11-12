#!/usr/bin/env node
/* Offline only. OEM bytes enter a private build, never the public source tree. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
export const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const fileName=/^[a-z0-9][a-z0-9._-]{0,100}\.(?:mp4|png|jpg|jpeg|webp)$/i;
export function validateConfig(c){
 if(!c||c.version!==1||!Array.isArray(c.media)||typeof c.icons!=='object'||!c.icons)throw Error('Invalid config schema');
 if(!/^[0-9]{1,8}$/.test(c.storeAppId))throw Error('Invalid storeAppId');
 const result={version:1,storeAppId:c.storeAppId,icons:{},media:[],defaults:{home:null,saver:null}};
 const ids=new Set();
 for(const [id,name] of Object.entries(c.icons)){
  if(!/^[a-zA-Z0-9_-]{1,80}$/.test(id)||typeof name!=='string'||!fileName.test(name)||/\.mp4$/i.test(name))throw Error('Invalid local icon');
  result.icons[id]=name;
 }
 for(const m of c.media){
  if(!m||!/^[a-z0-9_-]{1,40}$/.test(m.id)||ids.has(m.id)||typeof m.label!=='string'||!m.label.trim()||m.label.length>80)throw Error('Invalid media identity');
  if(!fileName.test(m.video)||!m.video.toLowerCase().endsWith('.mp4')||!fileName.test(m.poster)||/\.mp4$/i.test(m.poster))throw Error('Only local MP4 + raster poster allowed');
  if(!Number.isFinite(m.cycle)||m.cycle<2||m.cycle>1800)throw Error('Invalid loop cycle');
  ids.add(m.id);result.media.push({id:m.id,label:m.label,video:m.video,poster:m.poster,cycle:m.cycle});
 }
 for(const k of ['home','saver']){
  const id=c.defaults&&c.defaults[k];
  if(id!=null&&!ids.has(id))throw Error('Unknown default '+k);
  result.defaults[k]=id||null;
 }
 return result;
}
export function verifiedStock(home,saver,profile){
 for(const [name,data] of Object.entries({home,saver}))if(sha(data)!==profile.stock[name])throw Error('Unsupported '+name+' hash. Stop; do not change the profile to force installation.');
}
function main(){
 const args=process.argv.slice(2),opt={};
 for(let i=0;i<args.length;i+=2){
  if(!['--stock-home','--stock-saver','--config','--media-dir','--out'].includes(args[i])||!args[i+1])throw Error('Unknown or incomplete argument');
  opt[args[i]]=args[i+1];
 }
 const home=fs.readFileSync(opt['--stock-home']||'.private/stock/home.js');
 const saver=fs.readFileSync(opt['--stock-saver']||'.private/stock/saver.js');
 const profile=JSON.parse(fs.readFileSync(path.join(root,'compatibility.json'),'utf8'));
 verifiedStock(home,saver,profile);
 const config=validateConfig(JSON.parse(fs.readFileSync(opt['--config']||path.join(root,'config.example.json'),'utf8')));
 const out=path.resolve(opt['--out']||'.private/build');
 const privateRoot=path.resolve('.private');
 if(out===privateRoot||!out.startsWith(privateRoot+path.sep))throw Error('Build output must be below .private/ to avoid publishing OEM code');
 if(fs.existsSync(out))throw Error('Output already exists; choose a new .private/build-... directory');
 const assets=new Map(['metal-icon-atlas.png','metal-tab-atlas.png'].map(n=>[n,fs.readFileSync(path.join(root,n))]));
 const mediaDir=path.resolve(opt['--media-dir']||'.private/media');
 const names=[...Object.values(config.icons),...config.media.flatMap(m=>[m.video,m.poster])];
 for(const n of names){
  const f=path.join(mediaDir,n);
  if(fs.lstatSync(f).isSymbolicLink()||!fs.statSync(f).isFile()||!fs.realpathSync(f).startsWith(fs.realpathSync(mediaDir)+path.sep))throw Error('Asset must be an ordinary file inside media directory');
  assets.set(n,fs.readFileSync(f));
 }
 const generated='self.CleanHomeConfig='+JSON.stringify(config)+';\nself.OwnerDebug=false;\n';
 const src=n=>fs.readFileSync(path.join(root,n),'utf8');
 const license=['LICENSE','LICENSE.alvidaa.txt','LICENSE.free-my-tv.txt','LICENSE.metal-fx.txt'].map(src).join('\n');
 const common=generated+src('native-media.js')+'\n;\n'+src('native-video.js');
 const homeParts=['native-platform.js','native-core.js','native-dock.js','native-actions.js','native-entry.js'];
 const bundles={
  'home.js':'/*\n'+license+'\n*/\n'+home.toString()+'\n;\n'+common+'\n;\n'+homeParts.map(src).join('\n;\n'),
  'saver.js':saver.toString()+'\n;\n'+common+'\n;\n'+src('native-saver.js')
 };
 for(const [name,data] of Object.entries(bundles))new vm.Script(data,{filename:name});
 fs.mkdirSync(out,{recursive:true,mode:0o700});fs.mkdirSync(path.join(out,'assets'),{mode:0o700});
 const manifest={profile:profile.id,stock:profile.stock,containsPrivateVendorCode:true,publicRelease:false,files:{},assetsBytes:0};
 for(const [name,data] of Object.entries(bundles)){fs.writeFileSync(path.join(out,name),data,{mode:0o600});manifest.files[name]=sha(data);}
 for(const [name,data] of assets){fs.writeFileSync(path.join(out,'assets',name),data,{mode:0o600});manifest.files['assets/'+name]=sha(data);manifest.assetsBytes+=data.length;}
 fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify(manifest,null,2)+'\n',{mode:0o600});
 console.log(JSON.stringify({built:out,profile:profile.id,assetsBytes:manifest.assetsBytes,tvContacted:false,publicRelease:false}));
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 try{main();}catch(e){console.error(e.message);process.exitCode=1;}
}
