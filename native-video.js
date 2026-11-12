/* Local, silent video using the firmware's native local-media playback contract.
 * No HTML/canvas video decoding. Each instance releases its own player only.
 * Verified against this TV's ads/js/969.js and launcher/js/123.js. No ad code,
 * advertising requests, browser redirect, canvas decoding, or global mute. */
(function(root){'use strict';
 if(typeof root.OwnerVideo==='function')return;
 var base='static/vidaa-clean-home/';
 root.OwnerVideo=function(kind,onChange){
  var b=root._V_SDK_.biz,media=null,active=false,started=false,ready=false,player=null,timer=null,loops=0,lastSource=null,lastError=null,events=[],rawStates=[],snapshot=null,wantedURL='',playRequested=false,session='',loadResult=null,monitor=null,restartTimer=null,lastPosition=-1,seekAt=0,loopRequests=0,lastReport=0;
  function source(value){try{return typeof value==='string'?JSON.parse(value):value||JSON.parse(b.source.getCurrentAppSource());}catch(_){return null;}}
  function own(value){var s=source(value);return s&&s.sessionId===session&&s.sourceName==='dmp';}
  function report(phase,error){
   if(error)lastError=error;
   events.push({phase:phase,time:Date.now()});if(events.length>16)events.shift();
   var value={version:'owner-native-v2',kind:kind,phase:phase,active:active,playing:ready,player:player,loops:loops,loopRequests:loopRequests,time:Date.now(),error:lastError,source:lastSource,events:events,rawStates:rawStates,snapshot:snapshot,loadResult:loadResult};
   try{if(root.OwnerDebug)b.file.writeSync('owner-video-'+kind+'.json',JSON.stringify(value),b.file.PATH.UI);}catch(_){}
   if(onChange)onChange(value);
  }
  function play(){
   if(!active||started||!own())return;
   started=true;
   var name=media.video;
   wantedURL='file://'+b.file.getUiHomePath().replace(/\/$/,'')+'/hisenseUI/'+base+name+'?video-play-mode=1';
   // Same local-media path as firmware ads/js/969.js, with the video-only
   // mode supported by the launcher's native video class (launcher/js/123.js).
   b.mpctrl.playMedia(wantedURL,4,'Media','null',JSON.stringify({ContentHttpHeader:[{userAgent:root.navigator&&root.navigator.userAgent||''}]}));
   report('loading');
  }
  function changedSource(value){lastSource=source(value);if(!active)return;if(own(value))play();else{ready=false;report('source-away');}}
  function state(e){
   if(active&&rawStates.length<8){rawStates.push({value:e,currentSource:source(),isArray:Array.isArray(e)});report('state-observed');}
   if(!active||!started||!own()||!Array.isArray(e))return;
   if(e[1]!==wantedURL)return;
   var value=Number(e[2]),defs=b.mpctrl.MODELJS_DEFINE;
   if(player!==null&&String(player)!==String(e[0]))return;
   player=e[0];
   if(!playRequested&&value===defs.ENUM_STATE_PREPARED){
    playRequested=true;
    b.mpctrl.setVideoZoom(0);
    b.mpctrl.setMediaPlayPause(defs.ACTION_STATE_PLAY);
    report('play-requested');
   }
   if(Number(e[5])===4){
    if(!restartTimer){ready=false;report('end-restart');restartTimer=setTimeout(function(){restartTimer=null;if(!active||!own())return;started=false;player=null;playRequested=false;lastPosition=-1;play();},400);}
    return;
   }
   if(value===defs.ENUM_STATE_PLAYING){player=e[0];var wasPlaying=ready;ready=true;clearTimeout(timer);if(!wasPlaying)report('playing');if(!monitor)monitor=setInterval(poll,250);}
   else if(value===defs.ENUM_STATE_PLAY_ERROR_UNKNOWN){ready=false;report('error','media-player-error');stop();}
  }
  function progress(value){
   if(!active||!ready||!own())return;
   var now=Date.now(),position=Number(value),cycle=media.cycle;
   if(lastPosition>position+2){loops++;seekAt=0;report('loop-verified');}
   lastPosition=position;
   // Exact cyclic boundary, followed by two seconds of repeated continuation.
   // The source therefore remains continuous while the hardware seeks to zero.
   if(position>=cycle&&now-seekAt>2000){seekAt=now;loopRequests++;b.mpctrl.setMpCtrlPlaytimeCurrent(0);report('loop-requested');}
   if(now-lastReport>15000){
    lastReport=now;snapshot={position:position,cycle:cycle,duration:Number(b.mpctrl.getMpCtrlPlaytimeTotal())};
    try{var node=root.document.getElementById(kind==='home'?'owner-native-home':'owner-native-saver'),parents=[];
     while(node&&parents.length<8){var style=root.getComputedStyle(node);parents.push({tag:node.tagName,id:node.id,cls:node.className,background:style.backgroundColor,image:style.backgroundImage,opacity:style.opacity});node=node.parentElement;}snapshot.layers=parents;
    }catch(_){}
    report('progress');
   }
  }
  function poll(){if(active&&ready&&own())progress(b.mpctrl.getMpCtrlPlaytimeCurrent());}
  function loaded(value){loadResult=value;report('load-result');}
  function stop(){
   if(!active)return;active=false;clearTimeout(timer);clearTimeout(restartTimer);restartTimer=null;clearInterval(monitor);monitor=null;
   b.model.off(b.model.MESSAGE_NAME.MPCTRL_CURRENT_SOURCE,changedSource);
   b.model.off(b.model.MESSAGE_NAME.MPCTRL_STATE_CHANGED,state);
   b.model.off(b.model.MESSAGE_NAME.MPCTRL_LOAD_STATE_CHANGED,loaded);
   b.model.off(b.model.MESSAGE_NAME.MPCTRL_CURRENT_TIME_CHANGED,progress);
   if(started&&player!==null&&own()){
    try{b.mpctrl.setMediaStop(b.mpctrl.MODELJS_DEFINE.ACTION_STATE_STOP,player);}catch(_){}
   }
   started=false;ready=false;report('stopped');
   if(root.OwnerVideoActive===api)root.OwnerVideoActive=null;
  }
  var api={start:function(){
   if(active)return;
   media=root.OwnerMedia?root.OwnerMedia.selected(kind):{video:null,cycle:0};
   if(root.OwnerVideoActive&&root.OwnerVideoActive!==api)root.OwnerVideoActive.stop();
   if(!media.video){ready=false;report('still');return;}
   root.OwnerVideoActive=api;active=true;started=false;player=null;lastError=null;loops=0;events=[];rawStates=[];snapshot=null;playRequested=false;loadResult=null;lastPosition=-1;loopRequests=0;seekAt=0;lastReport=0;session='owner_timercontrol_'+Date.now()+'_NotUpdateLastSource';
   b.model.on(b.model.MESSAGE_NAME.MPCTRL_CURRENT_SOURCE,changedSource);
   b.model.on(b.model.MESSAGE_NAME.MPCTRL_STATE_CHANGED,state);
   b.model.on(b.model.MESSAGE_NAME.MPCTRL_LOAD_STATE_CHANGED,loaded);
   b.model.on(b.model.MESSAGE_NAME.MPCTRL_CURRENT_TIME_CHANGED,progress);
   timer=setTimeout(function(){if(active&&!ready){try{snapshot={state:b.mpctrl.getMpCtrlStat(),source:source(),time:b.mpctrl.getMpCtrlPlaytimeCurrent(),duration:b.mpctrl.getMpCtrlPlaytimeTotal(),dmpFeature:b.mpctrl.checkFeature(61441),streamingFeature:b.mpctrl.checkFeature(61442),metadata:b.mpctrl.getMetadata()};}catch(e){snapshot={error:String(e)};}report('timeout','no-playback-confirmation');stop();}},20000);
   // Ownership contract used for native local ads, without analytics or network.
   b.source.sourceSwitch([session,b.source.MODELJS_DEFINE.SOURCE_SWITCH_REASON_SWITCH_SOURCE,'DMP']);
   if(own())play();
  },stop:stop};return api;
 };
})(self);
