/* Replaces only VIDAA's ScreenMode view; existing idle decisions remain in charge. */
(function(root){'use strict';
 var original=root._V_M_&&root._V_M_['screen-saver'];if(typeof original!=='function')return;
 var wrapped=null,base='file:///hisenseUI/static/vidaa-clean-home/';
 function record(phase,error){try{if(!root.OwnerDebug)return;var b=root._V_SDK_.biz;b.file.writeSync('owner-saver-route.json',JSON.stringify({phase:phase,time:Date.now(),error:error?String(error):null}),b.file.PATH.UI);}catch(_){}}
 root._V_M_['screen-saver']=function(){
  if(wrapped)return wrapped;var stock=original.apply(this,arguments);
  try{
   var selected=root.OwnerMedia&&root.OwnerMedia.selected('saver');
   if(!selected||(!selected.video&&!selected.poster))return stock;
   var route=stock.route.filter(function(r){return r.path==='/ScreenSaver/ScreenMode';})[0];if(!route||typeof root.OwnerVideo!=='function')return stock;
   var sdk=new root._V_SDK_.vre.SDK('screen-saver'),keys=sdk.key.KEYMAP;
   route.component={name:'ScreenMode',data:function(){return{playing:false};},mounted:function(){this.start();},activated:function(){this.start();},deactivated:function(){this.stop();},beforeDestroy:function(){this.stop();},methods:{
    start:function(){if(this._active)return;this._active=true;var vm=this;
     record('mounted');this._video=root.OwnerVideo('saver',function(s){vm.playing=s.playing;});this._video.start();
     this._key=function(event){if(!sdk.router.isCurrentPathEqualTo('/ScreenSaver/ScreenMode'))return;
      if([keys.LEFT,keys.RIGHT,keys.UP,keys.DOWN,keys.ENTER,keys.BACK,keys.RETURN].indexOf(event.keyCode)>=0){event.stopPropagation();vm.close();}
     };root.document.body.addEventListener('key-down',this._key);
     this._exist=function(message){if(message&&['DLNA','LiveTV'].indexOf(message.source)>=0)vm.close();};sdk.message.on('n2o://screen-saver/exist-screen-saver',this._exist);
    },
    stop:function(){if(!this._active)return;this._active=false;if(this._video)this._video.stop();root.document.body.removeEventListener('key-down',this._key);sdk.message.off('n2o://screen-saver/exist-screen-saver',this._exist);},
    close:function(){this.stop();sdk.router.back();}
   },render:function(h){var media=root.OwnerMedia.selected('saver');return h('div',{attrs:{id:'owner-native-saver','aria-label':media.label+' Bildschirmschoner'},style:{position:'absolute',left:'0',top:'0',width:'100%',height:'100%',backgroundColor:this.playing?'transparent':'#080b11',backgroundImage:this.playing||!media.poster?'none':'url("'+base+media.poster+'")',backgroundSize:'cover'}});}};
   wrapped=stock;record('installed');return stock;
  }catch(error){record('install-error',error);return stock;}
 };
})(self);
