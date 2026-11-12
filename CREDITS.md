# Credits and license boundaries

## alvidaa and Free My TV

- [carteakey/alvidaa](https://github.com/carteakey/alvidaa), research revision
  4bbf060aa7bc1532478517d5cd4d1484bd28ad97; MIT, Kartikey Chauhan.
  Native adapter/component integration and device research.
  License: LICENSE.alvidaa.txt.
- [felipericardo/tv-launcher](https://github.com/felipericardo/tv-launcher),
  Free My TV design lineage, revision f2d984c, MIT.
  The adapted native component retains its source notice.
  License: LICENSE.free-my-tv.txt.

## Libraries.dev

**[Libraries.dev](https://libraries.dev/)** provided the visual reference and
[Liquid Metal / metal-fx](https://libraries.dev/#components) renderer.
The included small ring atlases were rendered from metal-fx **2.0.11**.
They are used as local sprite images, not as a React/WebGL runtime on the TV.
MIT copyright 2026 Jakub Antalik: LICENSE.metal-fx.txt.
The initial design explored Border Beam; the final dock itself has no container
frame. Only the selected app/tab has a focus outline.

## DNS research and earlier exploration

- [ipanalytics/Hisense-VIDAA-DNS-Clean-TV-Blocklist](https://github.com/ipanalytics/Hisense-VIDAA-DNS-Clean-TV-Blocklist)
  for categorized VIDAA DNS research. Its complete list is not vendored here.
- [Zfinix/vidaa-launcher](https://github.com/Zfinix/vidaa-launcher)
  for the earlier browser-launcher approach and performance lessons.

## License scope

New original maintainer contributions are PolyForm Noncommercial 1.0.0;
see [LICENSE-SCOPE.md](LICENSE-SCOPE.md) and [LICENSE](LICENSE). Prior MIT grants
and the upstream MIT portions remain valid, with their notices retained.
TV firmware, vendor bundles, service branding,
app logos, the preview's third-party artwork and privately licensed media do not
become covered by the project's license merely by appearing in an illustration.
The approved preview is included as documentation; no source wallpaper/icon pack
is distributed. Bring your own media or assets you are entitled to use.

No affiliation or endorsement by Hisense, VIDAA, Libraries.dev or app providers
is implied.

## Example video source pages

- [Midnight Fuel Stop — MotionBGS](https://motionbgs.com/midnight-fuel-stop)
- [Rainy Night City View — MotionBGS](https://motionbgs.com/rainy-night-city-view)

Linked for users who want to find the reference clips. No original MP4, converted
copy or private icon pack is bundled. The links do not grant redistribution
rights or relicense third-party media. See [the media guide](ANIMATED-WALLPAPERS.md)
for downloading to a private folder and preparing your own clips.

## Additional native SDK research

The `app-list-v1` adapter follows alvidaa's
[75U8QTUK native adapter](https://github.com/carteakey/alvidaa/blob/7f9c9e9f91b5e9982f0af3d515f052b7499b29b4/tools/launcher-host/native-platform-75u8qtuk.js),
reviewed at revision `7f9c9e9f91b5e9982f0af3d515f052b7499b29b4`.
The model research catalog cites that same revision. These are upstream results,
not additional hardware validations of this repository's dock.
