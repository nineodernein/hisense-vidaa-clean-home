/* Owner's native VIDAA home. Source data and launch rules stay in the vendor SDK. */
(function(root){'use strict';
 var make=root.AlvidaaFreeMyTV;
 var asset=root.OwnerAssetBase||'file:///hisenseUI/static/vidaa-clean-home/';
 var preferred=[/netflix/i,/magenta/i,/prime|amazon/i,/disney/i,/youtube/i,/rtl|tvnow/i,/ard|das erste/i,/^zdf/i];
 function name(app){var n=app.appName||'';if(String(app.appId)===String((root.CleanHomeConfig||{}).storeAppId||'164'))return 'App Store';if(/rtl|tvnow/i.test(n))return 'RTL+';if(/ard|das erste/i.test(n))return 'ARD';if(/prime|amazon/i.test(n))return 'Prime Video';return n;}
 function icon(app){return (root.CleanHomeConfig&&root.CleanHomeConfig.icons||{})[String(app.appId)]||null;}
 function appColor(n){return /magenta/i.test(n)?'#dd007f':/zdf/i.test(n)?'#f16b00':/ard/i.test(n)?'#0646bf':'#191c22';}
 root.AlvidaaFreeMyTV=function(sdk){
  var c=make(sdk),originalStart=c.methods.start,originalStop=c.methods.stop,originalSave=c.methods.save;
  var originalData=c.data,k=sdk.key.KEYMAP;
  c.data=function(){var d=originalData.call(this),p={};try{p=sdk.storage.get('owner.nativeDesign')||{};}catch(_){}
   if(typeof p==='string')try{p=JSON.parse(p);}catch(_){p={};}
   d.motion=p.motion!==false;d.videoEnabled=p.video!==false;d.videoPlaying=false;d.videoError='';d.mediaRevision=0;d.metalFrame=0;d.appIndex=0;d.tabIndex=0;d.topIndex=0;d.status='';d.revision='owner-native-v2';return d;
  };
  c.methods.shelf=function(){
   if(this.favorites!==null)return this.favorites.map(function(id){return this.apps.filter(function(a){return String(a.appId)===id;})[0];},this).filter(Boolean);
   var apps=this.apps;return preferred.map(function(re){return apps.filter(function(a){return re.test(a.appName);})[0];}).filter(Boolean);
  };
  c.methods.save=function(){originalSave.call(this);sdk.storage.set('owner.nativeDesign',{motion:this.motion,video:this.videoEnabled});};
  c.methods.tab=function(){return this.view==='inputs'?1:['tv','prefs','about','backgrounds','savers'].indexOf(this.view)>=0?2:0;};
  c.methods.list=function(){
   if(this.view==='inputs')return this.sources;
   if(this.view==='apps'||this.view==='edit')return this.apps;
   if(this.view==='tv')return ['TV-Einstellungen','Alle Apps','Startseite anpassen','Bildschirmschoner','Hintergrundbild'];
   if(this.view==='backgrounds'||this.view==='savers'){
    var current=root.OwnerMedia.selected(this.view==='savers'?'saver':'home').id;
    var choices=root.OwnerMedia.list().map(function(item){return (item.id===current?'✓ ':'')+item.label;});
    return this.view==='savers'?['Jetzt starten'].concat(choices):choices;
   }
   if(this.view==='prefs')return ['Favoriten auswählen','Favoriten sortieren','Bewegung: '+(this.motion?'An':'Aus'),'Video-Hintergrund: '+(this.videoEnabled?'An':'Aus'),'Zurück'];
   if(this.view==='about')return ['Zurück'];
   return this.shelf();
  };
  c.methods.routeFocus=function(){
   var q=this.$route&&this.$route.query||{};
   if(q.focusArea==='input'||Number(q.value)===k.SOURCE||q.startLauncherFrom===sdk.apc.CMDMETHOD.KEY_INPUT_START)this.show('inputs');
   else{this.view='home';this.zone='shelf';this.index=this.appIndex||0;this.moving=false;this.clamp();}
  };
  c.methods.clamp=function(){this.index=Math.max(0,Math.min(this.index,(this.zone==='top'?3:this.list().length)-1));};
  c.methods.show=function(view){if(this.view==='home'&&this.zone==='shelf')this.appIndex=this.index;this.view=view;this.zone='shelf';this.index=view==='home'?this.appIndex:0;this.moving=false;this.clamp();};
  c.methods.armSaver=function(){
   if(!this._running||!sdk.router.isCurrentPathEqualTo('/Launcher'))return;
   var vm=this;try{sdk.message.emit('n2o://screen-saver/art-start-screensaver',{beforeStart:function(){return vm._running&&sdk.router.isCurrentPathEqualTo('/Launcher');}});}catch(_){}
  };
  c.methods.startVideo=function(){
   if(!this._running||!this.videoEnabled||!sdk.router.isCurrentPathEqualTo('/Launcher')||root.document.hidden)return;
   var vm=this;
   if(!this._video)this._video=root.OwnerVideo('home',function(s){vm.videoPlaying=s.playing;vm.videoError=s.error||'';});
   this._video.start();
  };
  c.methods.start=function(){
   if(this._running)return;originalStart.call(this);var vm=this;
   clearInterval(this._clock);this._clock=setInterval(function(){vm.now=new Date();},15000);
   this._videoVisibility=function(){if(root.document.hidden){if(vm._video)vm._video.stop();clearTimeout(vm._shineTimer);vm._shineTimer=null;}else{vm.startVideo();vm.shine();}};
   root.document.addEventListener('visibilitychange',this._videoVisibility);
   this.$nextTick(function(){vm.startVideo();vm.armSaver();vm.shine();});
   this._imageCache=this._imageCache||[];
   if(!this._imageCache.length){Object.keys((root.CleanHomeConfig||{}).icons||{}).map(function(k){return root.CleanHomeConfig.icons[k];}).concat(['metal-icon-atlas.png','metal-tab-atlas.png']).forEach(function(path){var image=new root.Image();image.src=asset+path;vm._imageCache.push(image);});}
  };
  c.methods.stop=function(){if(this._video)this._video.stop();clearTimeout(this._shineTimer);this._shineTimer=null;root.document.removeEventListener('visibilitychange',this._videoVisibility);originalStop.call(this);};
  c.methods.shine=function(){if(this._shineTimer)return;if(!this.motion){this.metalFrame=0;return;}var vm=this;function step(){vm._shineTimer=null;if(!vm._running||!vm.motion)return;vm._metalStep=((vm._metalStep||0)+1)%46;vm.metalFrame=vm._metalStep>23?46-vm._metalStep:vm._metalStep;vm._shineTimer=setTimeout(step,200);}this._shineTimer=setTimeout(step,200);};
  c.methods.select=function(){
   var vm=this;if(this.zone==='top'){this.show(['home','inputs','tv'][this.index]);return;}
   var item=this.list()[this.index];if(item==null)return;
   if(this.view==='tv'){
    if(this.index===0){if(this._video)this._video.stop();this.run(function(){return vm._platform.openSettings();});}
    else if(this.index===1)this.show('apps');else if(this.index===2)this.show('prefs');
    else this.show(this.index===3?'savers':'backgrounds');
   }else if(this.view==='backgrounds'||this.view==='savers'){
    if(this.view==='savers'&&this.index===0){if(!root.OwnerMedia.selected('saver').video){this.status='Bitte zuerst ein Video hinzufügen';return;}this.run(function(){if(vm._video)vm._video.stop();return sdk.me.req('screen-saver').open('screenMode',{from:'launcher'});});return;}
    var kind=this.view==='savers'?'saver':'home',media=root.OwnerMedia.list()[this.index-(kind==='saver'?1:0)];
    this.run(function(){root.OwnerMedia.select(kind,media.id);vm.mediaRevision++;if(kind==='home'){if(vm._video)vm._video.stop();vm._video=null;vm.startVideo();}});
   }else if(this.view==='prefs'){
    if(this.index===0)this.show('edit');else if(this.index===1)this.show('reorder');
    else if(this.index===2){this.motion=!this.motion;this.save();if(this.motion)this.shine();else{clearTimeout(this._shineTimer);this._shineTimer=null;this.metalFrame=0;}}
    else if(this.index===3){this.videoEnabled=!this.videoEnabled;this.save();if(this.videoEnabled)this.startVideo();else if(this._video)this._video.stop();}
    else this.show('tv');
   }else if(this.view==='inputs'){if(this._video)this._video.stop();this.run(function(){return vm._platform.changeSource(item.sourceId);});}
   else if(this.view==='edit'){var ids=this.shelf().map(function(a){return String(a.appId);}),at=ids.indexOf(String(item.appId));if(at<0)ids.push(String(item.appId));else ids.splice(at,1);this.favorites=ids;this.save();}
   else if(this.view==='reorder')this.moving=!this.moving;
   else if(this.view==='about')this.show('tv');
   else{this.appIndex=this.index;if(this._video)this._video.stop();this.run(function(){return vm._platform.launchApp(item.appId);});}
  };
  c.methods.handleKey=function(code){
   this.armSaver();
   if([k.LEFT,k.RIGHT,k.UP,k.DOWN,k.ENTER,k.BACK,k.RETURN].indexOf(code)<0)return false;
   if(code===k.BACK||code===k.RETURN){if(this.moving){this.moving=false;return true;}if(this.view==='backgrounds'||this.view==='savers'){var menuIndex=this.view==='savers'?3:4;this.show('tv');this.index=menuIndex;return true;}if(this.view!=='home'){this.show('home');return true;}this.zone='top';this.index=0;return true;}
   if(code===k.ENTER){this.select();return true;}
   if(this.moving){var ids=this.shelf().map(function(a){return String(a.appId);}),to=Math.max(0,Math.min(ids.length-1,this.index+(code===k.LEFT?-1:code===k.RIGHT?1:0)));if(to!==this.index){ids.splice(to,0,ids.splice(this.index,1)[0]);this.index=to;this.favorites=ids;this.save();}return true;}
   if(this.zone==='top'){
    if(code===k.DOWN){this.show(['home','inputs','tv'][this.index]);}
    else if(code===k.LEFT)this.index--;else if(code===k.RIGHT)this.index++;
   }else if(this.view==='inputs'){
    var columns=4,row=Math.floor(this.index/columns),count=this.list().length;
    if(code===k.UP){if(row>0)this.index-=columns;else{this.zone='top';this.index=this.tab();}}
    else if(code===k.DOWN){if((row+1)*columns<count)this.index=Math.min(count-1,this.index+columns);}
    else if(code===k.LEFT){if(this.index%columns>0)this.index--;}
    else if(code===k.RIGHT){if(this.index%columns<columns-1&&this.index+1<count)this.index++;}
   }else if(code===k.UP){if(['tv','prefs','backgrounds','savers'].indexOf(this.view)>=0&&this.index>0)this.index--;else{this.appIndex=this.view==='home'?this.index:this.appIndex;this.zone='top';this.index=this.tab();}}
   else if(code===k.DOWN){if(['tv','prefs','backgrounds','savers'].indexOf(this.view)>=0)this.index++;}
   else this.index+=code===k.LEFT?-1:1;
   this.clamp();this.shine();return true;
  };
  c.methods.announce=function(){if(!sdk.tts||!sdk.tts.isEnable())return;var a=this.zone==='top'?['Apps','Eingänge','Fernseher'][this.index]:this.list()[this.index];if(a)sdk.tts.speak(typeof a==='string'?a:a.appId!=null?name(a):this.sourceName(a));};
  c.render=function(h){
   var vm=this,s=(root.innerWidth||1920)/1920,ink='#f7f8fa',muted='#ced1d8',tab=this.tab();
   function px(n){return Math.round(n*s)+'px';}
   function box(x,y,w,ht,extra){return Object.assign({position:'absolute',left:px(x),top:px(y),width:px(w),height:px(ht),boxSizing:'border-box'},extra||{});}
   function text(key,x,y,w,ht,size,value,extra){return h('div',{key:key,style:box(x,y,w,ht,Object.assign({fontSize:px(size),lineHeight:px(ht),color:ink,fontWeight:'400',whiteSpace:'nowrap',overflow:'hidden'},extra||{}))},[value]);}
   function ring(key,x,y,w,ht,type){return h('div',{key:key,attrs:{'aria-hidden':'true'},style:box(x,y,w,ht,{pointerEvents:'none',backgroundImage:'url("'+asset+'metal-'+type+'-atlas.png")',backgroundRepeat:'no-repeat',backgroundSize:px(w*4)+' '+px(ht*6),backgroundPosition:px(-(vm.metalFrame%4)*w)+' '+px(-Math.floor(vm.metalFrame/4)*ht)})});}
   function button(key,label,x,y,w,ht,focused,action,children,extra){return h('div',{key:key,attrs:{role:'button','aria-label':label,tabindex:focused?'0':'-1'},style:box(x,y,w,ht,Object.assign({color:ink,fontSize:px(30),outline:'none'},extra||{})),on:{click:action}},children||[label]);}
   var nodes=[],mediaRevision=this.mediaRevision,poster=root.OwnerMedia?root.OwnerMedia.selected('home').poster:'midnight-loop.jpg';
   nodes.push(h('div',{key:'poster',style:box(0,0,1920,1080,{backgroundImage:poster?'url("'+asset+poster+'")':'linear-gradient(135deg,#090e19,#14233b)',backgroundSize:'cover',opacity:this.videoPlaying?'0':'1'})}));
   nodes.push(h('div',{key:'shade',style:box(0,0,1920,1080,{backgroundImage:'linear-gradient(180deg,rgba(0,0,0,.38) 0%,rgba(0,0,0,0) 28%,rgba(0,0,0,0) 46%,rgba(0,0,0,.48) 65%,rgba(0,0,0,.86) 86%,rgba(0,0,0,.96) 100%)'})}));
   var clock=('0'+this.now.getHours()).slice(-2)+':'+('0'+this.now.getMinutes()).slice(-2);
   nodes.push(text('clock',1580,56,244,58,46,clock,{textAlign:'right',fontVariantNumeric:'tabular-nums'}));
   var days=['So.','Mo.','Di.','Mi.','Do.','Fr.','Sa.'],months=['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'];
   nodes.push(text('date',1500,116,324,32,22,days[this.now.getDay()]+' '+this.now.getDate()+'. '+months[this.now.getMonth()],{textAlign:'right',color:muted}));
   ['Apps','Eingänge','Fernseher'].forEach(function(label,i){var focused=vm.zone==='top'&&vm.index===i,selected=vm.zone==='top'?focused:tab===i,x=624+i*226;var children=[text('label',0,0,220,64,focused?31:29,label,{textAlign:'center',color:selected?ink:'#c6c7cb',fontWeight:focused?'600':'400'})];nodes.push(button('nav-'+i,label,x,66,220,64,focused,function(){vm.zone='top';vm.index=i;vm.select();},children));});
   nodes.push(h('div',{key:'persistent-nav-rim',attrs:{'aria-hidden':'true'},style:box(621,63,226,70,{pointerEvents:'none',transform:'translateX('+px((this.zone==='top'?this.index:tab)*226)+')',transition:this.motion?'transform 220ms cubic-bezier(.2,.7,.2,1)':'none'})},[ring('rim',0,0,226,70,'tab')]));
   var appView=['home','apps','edit','reorder'].indexOf(this.view)>=0,appItems=appView?this.list():this.shelf(),appSelected=appView&&this.zone==='shelf'?this.index:this.appIndex;
   var appNodes=[],offset=Math.max(0,Math.min(Math.max(0,(appItems.length-6)*240),Math.max(0,(appSelected-3)*240)));
   var selectedApp=appItems[appSelected];
   if(this.view!=='home')appNodes.push(text('section',96,0,1000,36,22,this.view==='apps'?'Alle Apps':this.view==='edit'?'Favoriten auswählen':'Favoriten sortieren',{color:muted}));
   appNodes.push(text('selected',96,42,1500,76,56,(selectedApp?name(selectedApp):'Apps auswählen')+(this.moving?' verschieben':''),{fontWeight:'500'}));
   var tileNodes=[];
   appItems.forEach(function(app,i){var focused=appView&&vm.zone==='shelf'&&vm.index===i,x=i*240-offset,width=180,src=icon(app),label=name(app),uri=src?asset+src:vm.localIcon(app);var alpha=Math.max(0,Math.min(1,(x+220)/100,(1768-x)/100));
    var visual=box(20,16,width,width,{borderRadius:px(38),backgroundColor:uri?'transparent':appColor(label),backgroundImage:uri?'url("'+uri+'")':'none',backgroundSize:'contain',backgroundRepeat:'no-repeat',backgroundPosition:'center',transform:focused?'scale(1.09)':'scale(1)',transformOrigin:'50% 50%',transition:vm.motion?'transform 180ms ease-out':'none'});
    var content=[h('div',{key:'visual',style:visual},uri?[]:[text('wordmark',9,62,162,56,/Magenta/.test(label)?24:28,label,{textAlign:'center',fontWeight:'600'})]),text('label',-4,218,228,40,25,label,{textAlign:'center',color:focused?ink:muted})];
    if(vm.view==='edit'&&vm.shelf().some(function(a){return a.appId===app.appId;}))content.push(text('check',158,0,40,40,28,'✓',{textAlign:'center'}));
    tileNodes.push(button('app-'+app.appId,label,i*240,0,220,268,focused,function(){vm.zone='shelf';vm.index=i;vm.select();},content));
   });
   if(appItems.length)tileNodes.push(h('div',{key:'persistent-app-rim',attrs:{'aria-hidden':'true'},style:box(-1,-5,222,222,{pointerEvents:'none',visibility:appView&&this.zone==='shelf'?'visible':'hidden',transform:'translateX('+px(appSelected*240)+')',transition:this.motion?'transform 220ms cubic-bezier(.2,.7,.2,1)':'none'})},[ring('rim',0,0,222,222,'icon')]));
   appNodes.push(h('div',{key:'persistent-dock',style:box(0,130,1920,320,{overflow:'hidden'})},[h('div',{key:'dock-track',style:box(76,20,Math.max(1920,appItems.length*240),280,{transform:'translateX('+px(-offset)+')',transition:vm.motion?'transform 220ms cubic-bezier(.2,.7,.2,1)':'none'})},tileNodes)]));
   var pages=Math.max(1,Math.ceil(appItems.length/3)),page=Math.min(pages-1,Math.floor(appSelected/3));
   for(var i=0;i<pages;i++)appNodes.push(h('div',{key:'dot-'+i,attrs:{'aria-hidden':'true'},style:box(951+(i-(pages-1)/2)*25,455,i===page?18:8,8,{borderRadius:px(4),backgroundColor:i===page?'#f5f5f7':'#787b83'})}));
   nodes.push(h('div',{key:'apps-panel',attrs:{'aria-hidden':appView?'false':'true'},style:box(0,552,1920,480,{visibility:appView?'visible':'hidden'})},appNodes));
   nodes.push(h('div',{key:'left-edge',style:box(0,0,96,1080,{pointerEvents:'none',backgroundImage:'linear-gradient(90deg,rgba(0,0,0,1),rgba(0,0,0,0))'})}));
   nodes.push(h('div',{key:'right-edge',style:box(1824,0,96,1080,{pointerEvents:'none',backgroundImage:'linear-gradient(270deg,rgba(0,0,0,1),rgba(0,0,0,0))'})}));
   var utility=[];
   if(!appView){var items=this.list(),title={inputs:'Eingänge',tv:'Fernseher',prefs:'Deine Startseite',about:'Über diese Startseite',backgrounds:'Hintergrundbild',savers:'Bildschirmschoner'}[this.view]||'';utility.push(text('title',0,0,1500,80,56,title,{fontWeight:'500'}));
    items.forEach(function(item,i){var label=typeof item==='string'?item:vm.sourceName(item),focus=vm.zone==='shelf'&&vm.index===i;var row=vm.view==='inputs',x=row?(i%4)*420:0,y=row?120+Math.floor(i/4)*135:110+i*76,w=row?384:1050,ht=64;var children=[text('label',22,0,w-44,ht,29,label,{color:focus?ink:muted})];utility.push(button('utility-'+i,label,x,y,w,ht,focus,function(){vm.zone='shelf';vm.index=i;vm.select();},children,{borderRadius:px(24),backgroundColor:focus?'rgba(255,255,255,.16)':'rgba(8,10,15,.62)',border:focus?px(2)+' solid #d3d9e4':px(1)+' solid rgba(255,255,255,.10)'}));});}
   nodes.push(h('div',{key:'utility-panel',style:box(96,410,1728,600,{visibility:appView?'hidden':'visible'})},utility));
   if(this.status&&/failed|error|nicht/i.test(this.status))nodes.push(text('status',500,1000,1324,28,21,this.status,{textAlign:'right',color:'#ffd9b8'}));
   return h('div',{attrs:{id:'owner-native-home'},style:{position:'absolute',left:'0',top:'0',width:'100%',height:'100%',overflow:'hidden',backgroundColor:this.videoPlaying?'transparent':'#08090d',fontFamily:'Arial, sans-serif',color:ink}},nodes);
  };
  return c;
 };
})(self);
