/* Native VIDAA data adapter. No browser/bridge transport.
 * Derived from alvidaa; use only after profile and SDK validation.
 * Generalized community packaging requires its own hardware acceptance.
 */
(function (root) {
  "use strict";
  function createNativePlatform(sdk, onUpdate, adapter) {
    adapter = adapter || root.CleanHomeAdapter || "current-show-apps-v1";
    if (["current-show-apps-v1", "app-list-v1"].indexOf(adapter) < 0) throw new Error("Unknown native SDK adapter");
    // app-list-v1 follows alvidaa's source-reviewed 75U8QTUK contract.
    // Select it from per-device evidence, never a chip/model-name guess.
    var modern = adapter === "app-list-v1";
    var events = [
      "o2n://sdk/init-finished",
      "o2n://app-service/all-apps-changed",
      "o2n://all-inputs/inputs-data-changed",
      "o2n://sdk/str-resuming"
    ];
    var delays = [250, 500, 1000, 2000, 4000, 8000];
    var apps = [], sources = [], running = false, reading = false, timer = null, attempt = 0;

    function readList(module, key, argument) {
      var response = sdk.me.req(module).getData(key, argument);
      if (!response || !Array.isArray(response.result)) {
        throw new Error(module + "." + key + " did not return a list");
      }
      return response.result.slice();
    }
    function cancelTimer() {
      clearTimeout(timer);
      timer = null;
    }
    function refresh() {
      if (!running) return;
      cancelTimer();
      var errors = [];
      reading = true;
      // Keep the last good list on a failed read, but accept a successful empty
      // list (e.g. all apps removed). One failed service must not hide the other.
      try { apps = readList("app-service", modern ? "getAppList" : "getCurrentShowApps", modern ? {sceneCode:"launcher"} : "Launcher"); }
      catch (error) { errors.push("Apps: " + error.message); }
      try { sources = readList("all-inputs", "getAllInputsData"); }
      catch (error) { errors.push("Inputs: " + error.message); }
      reading = false;
      var waiting = errors.length > 0 || apps.length === 0 || sources.length === 0;
      var retrying = waiting && attempt < delays.length;
      if (retrying) timer = setTimeout(refresh, delays[attempt++]);
      onUpdate({ apps: apps.slice(), sources: sources.slice(), errors: errors,
        waiting: waiting, retrying: retrying });
    }
    function changed() {
      if (!running || reading) return;
      // Coalesce notifications. Ignore synchronous notifications caused by our
      // own reads: otherwise lazy initialization can reset the retry budget.
      attempt = 0;
      cancelTimer();
      timer = setTimeout(refresh, 0);
    }
    function stop() {
      if (!running) return;
      running = false;
      cancelTimer();
      events.forEach(function (event) { sdk.message.off(event, changed); });
    }
    return {
      start: function () {
        if (running) return;
        running = true;
        attempt = 0;
        try {
          events.forEach(function (event) { sdk.message.on(event, changed); });
          refresh();
        } catch (error) { stop(); throw error; }
      },
      stop: stop,
      refresh: changed,
      openSettings: function () {
        if (modern) return sdk.me.req("setting").open("settings");
        return sdk.me.req("setting").open("settings", { vk: "T" });
      },
      launchApp: function (appId) {
        if (!apps.some(function (app) { return app && String(app.appId) === String(appId); })) {
          throw new Error("App is not in the current native app list");
        }
        var response = sdk.me.req("app-service").getData(modern ? "getAppInfo" : "getAppInfoByAppId",
          { appId: String(appId), url: "", checkRange: 1 });
        var app = response && response.result;
        if (modern) {
          if (!app || typeof app !== "object" || Array.isArray(app) ||
              (app.appId != null && String(app.appId) !== String(appId))) throw new Error("App is unavailable or restricted");
          var item = apps.filter(function (a) { return a && String(a.appId) === String(appId); })[0];
          function value(key, fallback) { return app[key] != null ? app[key] : item[key] != null ? item[key] : fallback; }
          var method = sdk.apc.CMDMETHOD && sdk.apc.CMDMETHOD.LAUNCHER_RECOMMEND;
          if (method == null) throw new Error("Launcher command is not exposed by this SDK");
          return sdk.apc.start({name:String(value("appName", "")),appId:value("appId", String(appId)),
            url:String(value("url", "")),storeType:value("storeType", value("openMode", 0)),
            startMethod:method,typeCode:String(value("typeCode", "600002")),rateInfo:""});
        }
        if (!app || String(app.appId) !== String(appId)) throw new Error("App is unavailable or restricted");
        // APC owns parental PIN, EULA and hotel-mode checks. Never propagate
        // bypass flags from a UI record or invoke the lower-level app service.
        return sdk.apc.start({ name: app.appName || "", appId: app.appId,
          url: app.url || "", storeType: app.storeType,
          startMethod: sdk.apc.CMDMETHOD.REMOTECONTROL, typeCode: "600002" });
      },
      changeSource: function (sourceId) {
        var validId = (typeof sourceId === "string" && sourceId.trim() !== "") ||
          (typeof sourceId === "number" && isFinite(sourceId));
        if (!validId || !sources.some(function (source) { return source && source.sourceId === sourceId; })) {
          throw new Error("Input is not in the current native source list");
        }
        return sdk.me.req("all-inputs").invoke("changeSourceTo", sourceId, "launcher");
      }
    };
  }
  if (typeof module !== "undefined" && module.exports) module.exports = createNativePlatform;
  else root.AlvidaaNativePlatform = createNativePlatform;
}(typeof self !== "undefined" ? self : this));
