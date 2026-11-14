# Continue Watching: native preview research and implementation handoff

Status: **2026-11-14**. These are lessons from a private extension on the original
TV. **The public native build does not ship these provider adapters.**
Public documentation must not be mistaken for a working cross-provider installer.

## Acceptance status

| Provider | Original-unit evidence | Still unresolved |
| --- | --- | --- |
| Netflix | Personal resume item, title, artwork and native action confirmed | Reliable current season/episode and remaining time |
| Prime Video | Personal item, title, artwork, season/episode and native action confirmed | Remaining time |
| Disney+ | Artwork, current season/episode, remaining minutes, progress, correct episode and Home return confirmed; updates observed | Portability, other profiles and renewal cases require separate checks |
| Jellyfin | App tile/client and local server connection work | Empty library meant no real resume item was accepted |
| YouTube | Private history/thumbnail retrieval and token renewal responded successfully | Owner reported missing/wrong card; account matching, visible result and video-specific action not accepted |
| ARD, ZDF, RTL+, MagentaTV, HBO Max | Apps/inventory are separate from personal metadata | No accepted personal-resume integration |

Do not replace missing personal data with recommendations and call it
“Weiterschauen”. Do not describe the YouTube trial as working merely because
requests succeeded. Private viewing titles and content IDs are not test fixtures.

## Shared native card contract

Use a provider adapter returning a small normalized record:

- provider and actual installed app ID;
- opaque account/profile context used privately to invalidate cache;
- item ID, display title and artwork reference;
- current season/episode only when attached to that same playable item;
- position and duration with explicit units, or an actual remaining-time value;
- observation time, content expiry and source provenance;
- validated native launch action, including the provider's existing checks.

Catalog season/episode totals are not the user's current episode. Do not infer
remaining minutes from a decorative bar embedded in artwork. For reliable
position/duration, clamp the progress ratio and calculate remaining time using
consistent units; omit unavailable fields. Finished YouTube history belongs under
“Zuletzt angesehen”, not a fabricated “Noch 0 Min.” resume claim.

Keep the accepted card compact: **720×190 logical pixels**, artwork **288×162**
with contain sizing and about 14 pixels of padding. Use a two-line title and a
short metadata line rather than enlarging the card. Preserve artwork lettering.
A translucent surface with a supported blur/fallback can evoke glass; heavy
browser shaders and unsupported CSS must not hide content.

On the reference renderer, CSS background artwork worked where an image element
remained blank. Verify native rendering rather than assuming browser parity.
A missing image should retain readable text without becoming an accepted image
test.

Navigation: Up from the dock reaches the available card; OK opens its actual
native item action; Down/Back returns to the dock; further Up can reach the tabs.
Retain parental/rating checks. Opening the app alone is not proof of episode
deep linking.

## Delivery, cache and privacy

Use request generation IDs so a late response for the previously focused app
cannot appear under a new app. Cache results across focus changes and section
switches. Short positive/negative caches were useful; honor each provider's
longer minimum refresh and expiry rules. Avoid requests on every keypress.

Resolve current account/profile context before selecting an item. Invalidate on
account/profile change or expiry. Distinguish content expiry from the separate
maintenance-access deadline. An old diagnostic lease must not silently decide
whether valid content is rendered.

The reference native BaaS fetcher transport worked for a private host route where
ordinary browser-style fetching did not. Use only reviewed available transport
contracts. Reuse a restricted existing host listener when suitable; do not expose
an unauthenticated general-purpose proxy or open arbitrary ports.

Allowlist provider destinations, limit response size/type/time and sanitize image
handling. Keep authorization in private request state and out of URLs, console
logs and public bundles. Signed artwork/action URLs may contain private query
parameters. Store only necessary normalized data and expire it. A helper host
must be available for host-backed metadata; native Home should remain usable
when that optional service fails.

Do not send history, playback, impression or scrobbling updates just to obtain a
preview. Do not copy entire browser profiles/DRM stores or weaken app authentication.
Use synthetic fixtures for public tests.

## Netflix: use the native resume contract, respect its cache

The native Home's provider integration supplies a partner/DET context. Its token
context and request contract are not interchangeable with Netflix website
cookies or another client. Treat them as private owner-session state.

Select the explicit resume group and bind artwork/action to that item's identity.
Available catalog counts such as seasonsCount/episodesCount did not establish
the currently watched episode or play position. The displayed progress inside
returned artwork is not an exact minute value.

The native response includes refresh/expiry behavior. Retain the actual request
timestamp and honor minimum-refresh instructions. A crucial late finding:
restarting Home can itself trigger a fresh provider query, moving the next
allowed query time. Repeated reloads to investigate missing fields can therefore
keep postponing the useful probe and interrupt apps.

One bounded probe performed no additional request because cooldown was still
active; that is not a successful schema inspection. An isolated introspection
server error also does not prove every candidate field is unsupported.
Consolidate source questions, inspect the retained response and wait for the real
refresh window instead of guessing field combinations or bypassing cooldown.

The public [Universal Trakt Scrobbler Netflix implementation](https://github.com/trakt-tools/universal-trakt-scrobbler/blob/7ad00a272b2e890eaa4a176542f8858b26ea88d4/src/services/netflix/NetflixApi.ts)
is a useful comparison for website activity/bookmark semantics. It is a separate
website-authentication context, not evidence that its requests work with TV DET
credentials. No universal Netflix remaining-time solution was established here.

## Prime Video: exact item matching before enrichment

Select the personal continue-watching row from the native feed. Enrichment used
the same native-v2 item action and catalog decorations containing
`season_number` and `episode_number`. Match the exact item/deep-link identity,
not just a series title. Preserve the original native action.

That produced owner-confirmed season/episode text. Reviewed native configuration
and caches did not establish a reliable playback bookmark/remaining time.
Do not substitute a total series duration or an inferred progress estimate.

A TV ODE token was not accepted by a different mobile Switchblade startup route;
the observed 401 is specific to that client/authentication contract. Changing
device identity or using Kodi's local resume database would not establish the
TV app's progress.

The [amazon-vod-fireos API implementation](https://github.com/ScriptGod1337/amazon-vod-fireos/blob/01d93d5d63a8795814a77299890abb601b7c131a/app/src/main/java/com/scriptgod/fireos/avod/api/AmazonApiService.kt)
shows another client's watch-progress/runtime concepts. It is a source lead,
not a tested VIDAA adapter. Opaque caches remain unknown until actually decoded.

## Disney+: preserve the accepted integration

The original owner confirmed the card's artwork, episode metadata, remaining
minutes and native action, followed by physical Home return. Subsequent observed
updates demonstrate more than a one-time hardcoded title.

Preserve that accepted path while investigating another provider. Keep the
actual account/profile binding and valid item action, and omit unavailable data.
A successful private integration is not a portable unauthenticated Disney API.
Its credentials, raw responses and personal history must remain private.

The exact device-specific adapter is not included in this public kit. An agent
starting on a different device must inspect the available authorized native
provider contract, then validate the same acceptance criteria.

## Jellyfin: app registration and resume metadata are separate

Adding a Jellyfin app tile to the existing app inventory and favorites should
not replace Home or reset its configuration. Verify registration, cache refresh,
favorite membership, icon and actual launch independently. An “open Jellyfin”
link can work even when an installer did not register an app.

The [Jellyfin VIDAA installation project](https://github.com/theDavidCoen/jellyfin-vidaa-install)
documents a web-client installation approach. Its DNS setup is not a prerequisite
to adopt blindly on an already modified Home. Keep the owner's chosen server
and login private. Quick Connect codes belong to the current session only.

Jellyfin's server has an explicit [resume-items API](https://github.com/jellyfin/jellyfin/blob/2953ed632c9277351483eff04f87a8276390691c/Jellyfin.Api/Controllers/ItemsController.cs).
Use the chosen user's authenticated resume list and actual item playback data.
A zero-item/empty-library response is a valid empty state, not proof of a broken
TV connection. The original project's empty library did not provide a real
resume-item acceptance test. Test codec/audio/subtitle playback separately.

## YouTube: history retrieval is not visible acceptance

The official Data API does not expose the user's watch-history list; its
[revision history](https://developers.google.com/youtube/data/revision_history)
explicitly describes that limitation. Repeating official playlist calls with
different history IDs is not the appropriate next experiment.

The TV client's authenticated history route was investigated through existing
owner-session state. Public references include:

- [YouTube.js history implementation](https://github.com/LuanRT/YouTube.js/blob/d6bcf97531e638fbb2505e3dace83139f834468e/src/Innertube.ts), including FEhistory;
- [its OAuth implementation](https://github.com/LuanRT/YouTube.js/blob/d6bcf97531e638fbb2505e3dace83139f834468e/src/core/OAuth2.ts), a client-specific research reference;
- Google's [Cobalt storage schema](https://github.com/youtube/cobalt/blob/dd50bcd219df5870a032ad609b87e3b3cd0e5524/cobalt/shell/browser/migrate_storage_record/storage.proto), for structured migration/storage interpretation.

Private tests obtained a history response, thumbnail and renewed token. However,
the owner reported a missing or wrong card. Last stored identity is not proof
of the active TV profile. Account selection, the actual visible item and a
video-specific native action remain unresolved; the draft app-opening action
was insufficient. **This prototype is not an accepted feature.**

Additional research lessons: current TV bootstrap code may dynamically create
the base script, so a fixed old script-tag regex can fail. Derive parsing from
the actual source. Signed onSelectCommand/playback URLs can contain private
session/network values; do not log or replay them wholesale. Validate a video
identifier and the native app contract instead. No token or client secret belongs
in public examples.

## Provider acceptance checklist

1. Use synthetic fixtures for normalization, units, empty/error/expiry cases and
   account changes. Test response races after rapid focus switching.
2. Verify exactly which native module/candidate is running; stale compiled cache
   can hide a correct source change.
3. Verify the real account/profile and item without publishing their identities.
4. Confirm the whole image, current metadata and truthful progress on screen.
5. Confirm native item action and physical Home return.
6. Accept or roll back within the maintenance window; keep unrelated providers.
7. Record separate states: source inspected, response received, data normalized,
   card rendered, owner accepted, action accepted, cleanup verified.

A wrong/missing visible card remains a failed acceptance check even if every
backend request returned HTTP 200.
