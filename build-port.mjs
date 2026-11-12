#!/usr/bin/env node
/* EXPERIMENTAL LOCAL ASSEMBLY, NOT AN INSTALLER OR SUPPORT PROFILE.
 * Called after agent.py prepare-port validates evidence and recovery records.
 * Neither this builder nor editable review records prove live hardware behavior.
 */
import fs from 'node:fs';
import path from 'node:path';
import {assemble, privateOutput, sha} from './build.mjs';
import {fileURLToPath} from 'node:url';

const root=path.dirname(fileURLToPath(import.meta.url));
function privateFile(name){
 const file=path.resolve(name),p=path.resolve('.private');
 privateOutput(path.dirname(file),p);
 if(!file.startsWith(p+path.sep)||fs.lstatSync(file).isSymbolicLink()||!fs.statSync(file).isFile())throw Error('Expected an ordinary private file');
 return file;
}
export function buildCandidate(requestPath,output){
 const request=JSON.parse(fs.readFileSync(privateFile(requestPath),'utf8'));
 if(request.schemaVersion!==1||request.kind!=='experimental_static_home_only')throw Error('Unknown experimental request');
 const home=fs.readFileSync(privateFile(request.home));
 if(sha(home)!==request.homeSha256)throw Error('Original changed after review');
 const config=request.config;
 if(!config||!Array.isArray(config.media)||config.media.length||Object.keys(config.icons||{}).length||Object.values(config.defaults||{}).some(Boolean))throw Error('First candidate must be static');
 const bundles=assemble(home,null,config,{homeOnly:true,adapter:request.adapter,
  assetBase:request.assetBase,excludedAppIds:request.excludedAppIds});
 const out=privateOutput(output);
 if(fs.existsSync(out))throw Error('Choose a fresh private output directory');
 fs.mkdirSync(out,{recursive:true,mode:0o700});fs.mkdirSync(path.join(out,'assets'),{mode:0o700});
 const manifest={schemaVersion:1,kind:'experimental_device_port',adapter:request.adapter,
  containsPrivateVendorCode:true,publicRelease:false,hardwareVerified:false,installationAuthorized:false,
  originalHomeSha256:sha(home),files:{}};
 for(const [name,data] of Object.entries(bundles)){
  fs.writeFileSync(path.join(out,name),data,{mode:0o600,flag:'wx'});manifest.files[name]=sha(data);
 }
 for(const name of ['metal-icon-atlas.png','metal-tab-atlas.png']){
  const data=fs.readFileSync(path.join(root,name));fs.writeFileSync(path.join(out,'assets',name),data,{mode:0o600,flag:'wx'});manifest.files['assets/'+name]=sha(data);
 }
 fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify(manifest,null,2)+'\n',{mode:0o600,flag:'wx'});
 return {status:'experimental_candidate_only',hardwareVerified:false,installationAuthorized:false,tvContacted:false};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 try{
  const args=process.argv.slice(2);
  if(args.length!==4||args[0]!=='--request'||args[2]!=='--out')throw Error('Use agent.py prepare-port --port <private port profile>');
  console.log(JSON.stringify(buildCandidate(args[1],args[3])));
 }catch(error){console.error(error.message);process.exitCode=1;}
}
