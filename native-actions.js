/* Native key-down/key-up long press, verified against this firmware's SDK.
 * Favorites only: removing a tile never uninstalls an app. Store stays last. */
(function(root){'use strict';var factory=root.AlvidaaFreeMyTV;
 root.AlvidaaFreeMyTV=function(sdk){
  var c=factory(sdk),data=c.data,start=c.methods.start,stop=c.methods.stop,shelf=c.methods.shelf,list=c.methods.list,select=c.methods.select,key=c.methods.handleKey,render=c.render,announce=c.methods.announce,K=sdk.key.KEYMAP;
  c.data=function(){var d=data.call(this);d.actionApp=null;d.actionIndex=0;return d;};
  c.methods.favoriteApps=function(){return shelf.call(this).filter(function(a){return String(a.appId)!==String((root.CleanHomeConfig||{}).storeAppId||'');});};
  c.methods.shelf=function(){var result=this.favoriteApps(),store=this.apps.filter(function(a){return String(a.appId)===String((root.CleanHomeConfig||{}).storeAppId||'');})[0];if(store)result.push(store);return result;};
  c.methods.list=function(){if(this.view==='reorder')return this.favoriteApps();if(this.view==='edit')return this.apps.filter(function(a){return String(a.appId)!==String((root.CleanHomeConfig||{}).storeAppId||'');});return list.call(this);};
  c.methods.cancelHold=function(){clearTimeout(this._holdTimer);this._holdTimer=null;this._held=false;this._longHeld=false;};
  c.methods.beginMove=function(){this._beforeMove=this.favoriteApps().map(function(a){return String(a.appId);});this.moving=true;};
  c.methods.select=function(){
   if(this.moving){this.moving=false;this._beforeMove=null;this.save();return;}
   if(this.actionApp){var id=String(this.actionApp.appId),choice=this.actionIndex;this.actionApp=null;if(choice===0)this.beginMove();else{this.favorites=this.favoriteApps().map(function(a){return String(a.appId);}).filter(function(v){return v!==id;});this.clamp();this.appIndex=this.index;this.save();}return;}
   if(this.view==='reorder'&&this.zone==='shelf'){this.beginMove();return;}
   if(this.view==='edit'&&this.zone==='shelf'){var app=this.list()[this.index],ids=this.favoriteApps().map(function(a){return String(a.appId);}),at=ids.indexOf(String(app.appId));if(at<0)ids.push(String(app.appId));else ids.splice(at,1);this.favorites=ids;this.save();return;}
   return select.call(this);
  };
  c.methods.handleKey=function(code){
   if(this.actionApp){this.armSaver();if(code===K.BACK||code===K.RETURN){this.actionApp=null;return true;}if(code===K.ENTER){this.select();return true;}if([K.UP,K.DOWN,K.LEFT,K.RIGHT].indexOf(code)>=0){this.actionIndex=code===K.UP||code===K.LEFT?0:1;return true;}return false;}
   if(this.moving){this.armSaver();if(code===K.BACK||code===K.RETURN){if(this._beforeMove)this.favorites=this._beforeMove;this._beforeMove=null;this.moving=false;this.save();return true;}if(code===K.ENTER){this.select();return true;}if(code===K.LEFT||code===K.RIGHT){var ids=this.favoriteApps().map(function(a){return String(a.appId);}),to=Math.max(0,Math.min(ids.length-1,this.index+(code===K.LEFT?-1:1)));if(to!==this.index){ids.splice(to,0,ids.splice(this.index,1)[0]);this.favorites=ids;this.index=to;this.appIndex=to;}return true;}return [K.UP,K.DOWN].indexOf(code)>=0;}
   return key.call(this,code);
  };
  c.methods.start=function(){if(this._running)return;start.call(this);var vm=this;
   root.document.body.removeEventListener('key-down',this._keyDown);
   this._keyDown=function(event){
    if(!sdk.router.isCurrentPathEqualTo('/Launcher'))return;
    var code=event.keyCode;
    if(code===K.ENTER&&vm._held){event.stopPropagation();return;}
    if(code===K.ENTER&&vm.view==='home'&&vm.zone==='shelf'&&!vm.actionApp&&!vm.moving){
     event.stopPropagation();vm.armSaver();vm._held=true;vm._longHeld=false;vm._holdIndex=vm.index;
     vm._holdTimer=setTimeout(function(){vm._holdTimer=null;if(!vm._held||vm.index!==vm._holdIndex)return;var app=vm.shelf()[vm.index];if(app&&String(app.appId)!==String((root.CleanHomeConfig||{}).storeAppId||'')){vm._longHeld=true;vm.actionApp=app;vm.actionIndex=0;vm.announce();}},650);return;
    }
    if(code!==K.ENTER)vm.cancelHold();
    if(event.repeat&&code===K.ENTER){event.stopPropagation();return;}
    if(vm.handleKey(code)){event.stopPropagation();vm.announce();}
   };
   this._keyUp=function(event){if(event.keyCode!==K.ENTER||!vm._held)return;event.stopPropagation();var click=!vm._longHeld&&vm.index===vm._holdIndex;vm.cancelHold();if(click)vm.select();};
   root.document.body.addEventListener('key-down',this._keyDown);root.document.body.addEventListener('key-up',this._keyUp);
  };
  c.methods.stop=function(){this.cancelHold();this.actionApp=null;if(this.moving&&this._beforeMove)this.favorites=this._beforeMove;this.moving=false;root.document.body.removeEventListener('key-up',this._keyUp);stop.call(this);};
  c.methods.announce=function(){if(this.actionApp&&sdk.tts&&sdk.tts.isEnable())sdk.tts.speak(this.actionIndex===0?'Verschieben':'Vom Startbildschirm entfernen');else announce.call(this);};
  c.render=function(h){var result=render.call(this,h),vm=this;if(!this.actionApp)return result;var scale=(root.innerWidth||1920)/1920,p=function(n){return Math.round(n*scale)+'px';};
   var choices=['Verschieben','Vom Startbildschirm entfernen'];
   result.children.push(h('div',{key:'favorite-actions',attrs:{role:'dialog','aria-modal':'true','aria-label':this.actionApp.appName},style:{position:'absolute',left:'0',top:'0',width:'100%',height:'100%',backgroundColor:'rgba(0,0,0,.58)'}},[
    h('div',{style:{position:'absolute',left:p(600),top:p(350),width:p(720),padding:p(40),boxSizing:'border-box',backgroundColor:'#15171d',borderRadius:p(30),border:p(1)+' solid #6b707e'}},[
     h('div',{style:{fontSize:p(36),color:'#fff',marginBottom:p(30)}},[this.actionApp.appName])
    ].concat(choices.map(function(label,i){return h('div',{key:label,attrs:{role:'button',tabindex:vm.actionIndex===i?'0':'-1'},on:{click:function(){vm.actionIndex=i;vm.select();}},style:{height:p(76),lineHeight:p(76),paddingLeft:p(22),fontSize:p(27),marginTop:p(12),borderRadius:p(18),color:'#fff',backgroundColor:vm.actionIndex===i?'#404650':'#22252c',border:p(2)+' solid '+(vm.actionIndex===i?'#e4e9f0':'transparent')}},[label]);})))
   ]));return result;
  };return c;
 };
})(self);
