/* Keep the vendor module and replace only its /Launcher component. */
(function(root){'use strict';
 var original=root._V_M_&&root._V_M_.launcher;if(typeof original!=='function')return;
 var wrapped=null;
 root._V_M_.launcher=function(){
  if(wrapped)return wrapped;var stock=original.apply(this,arguments);
  try{
   if(!root._V_SDK_||!root._V_SDK_.vre||typeof root.AlvidaaFreeMyTV!=='function')return stock;
   var sdk=new root._V_SDK_.vre.SDK('launcher',{storagePrefix:'CleanHome'});
   if(!sdk.key||!sdk.key.KEYMAP||!sdk.me||!sdk.apc||!sdk.storage)return stock;
   var route=stock.route&&stock.route.filter(function(r){return r.path==='/Launcher';})[0];if(!route)return stock;
   var component=root.AlvidaaFreeMyTV(sdk);
   route.component=component;wrapped=stock;return stock;
  }catch(error){root.CleanHomeError=String(error);return stock;}
 };
})(self);
