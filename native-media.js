/* Local media catalog. No network requests, installation or external URLs. */
(function(root){'use strict';
 if(root.OwnerMedia)return;
 var cfg=root.CleanHomeConfig||{},empty={id:'off',label:'Kein Video',video:null,poster:null,cycle:0};
 var catalog=(cfg.media||[]).slice();if(!catalog.length)catalog=[empty];
 var cache=null,filename='clean-home-media-selection.json';
 function find(id){return catalog.filter(function(m){return m.id===id;})[0];}
 function file(){return root._V_SDK_&&root._V_SDK_.biz&&root._V_SDK_.biz.file;}
 function load(){
  if(cache)return cache;var value={},defaults=cfg.defaults||{};
  try{var f=file();if(f&&f.exists(filename,f.PATH.UI))value=JSON.parse(f.readSync(filename,f.PATH.UI))||{};}catch(_){}
  cache={version:1,home:find(value.home)?value.home:find(defaults.home)?defaults.home:catalog[0].id,
   saver:find(value.saver)?value.saver:find(defaults.saver)?defaults.saver:catalog[0].id};return cache;
 }
 root.OwnerMedia={
  list:function(){return catalog.slice();},
  selected:function(kind){return find(load()[kind==='saver'?'saver':'home'])||empty;},
  select:function(kind,id){
   if(['home','saver'].indexOf(kind)<0||!find(id))throw new Error('Unbekanntes Motiv');
   var previous=load(),next={version:1,home:previous.home,saver:previous.saver};next[kind]=id;
   if(!root.OwnerMediaPreview){var f=file();if(!f)throw new Error('Auswahl konnte nicht gespeichert werden');
    f.writeSync(filename,JSON.stringify(next),f.PATH.UI);var saved=JSON.parse(f.readSync(filename,f.PATH.UI));
    if(saved.home!==next.home||saved.saver!==next.saver)throw new Error('Auswahl konnte nicht gespeichert werden');}
   cache=next;return find(id);
  }
 };
})(self);
