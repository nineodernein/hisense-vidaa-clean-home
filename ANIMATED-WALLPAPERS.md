# Animated VIDAA wallpapers and video screensavers

Yes: the reference TV played a local animated background through its native
media player. The original upload was 4K, but the prepared playback copy was a
silent 1080p24 H.264 MP4. Native text remains separate from video.

No private video or paid icon pack is included. Use media you own or may use.
Do not use the README preview as a wallpaper source; it is only a screenshot.

## Prepare a clip on your computer

Use an existing FFmpeg/ffprobe installation from a trusted source. Nothing in
this repo downloads or installs it automatically. The included Python exporter
is a portable reimplementation; its filter-plan tests are offline. Unlike the
original macOS exporter, this specific exporter still needs a real FFmpeg export
and visual loop check before using its output on a TV.

```sh
python3 prepare-media.py /path/to/your-video.mp4 --id night --label "Night"
```

Optional slower playback:

```sh
python3 prepare-media.py /path/to/your-video.mp4 --id night-slow --label "Night slow" --speed 0.9 --crossfade 1
```

Output: .private/media/night.mp4, night.jpg and night.json.
The original is not overwritten. Sound and metadata are removed. A short
tail/head crossfade is followed by two seconds of cyclic continuation so the
native player can seek to zero before EOF. Some scenes still reveal a transition;
inspect the actual video rather than promising a mathematically invisible loop.

For a command-only offline plan, use --dry-run --duration with the known source
duration. Actual exports obtain duration through ffprobe.

## Add it to the catalog

Copy config.example.json to .private/ui.json. Add the object printed by the exporter
to media, set defaults.home/defaults.saver to its id, and rebuild to a new private
output directory. Example:

```json
{
  "version": 1,
  "storeAppId": "164",
  "icons": {},
  "media": [
    {"id":"night","label":"Night","video":"night.mp4","poster":"night.jpg","cycle":14}
  ],
  "defaults": {"home":"night","saver":"night"}
}
```

The cycle above is illustrative: use the actual exported metadata, not 14 for
every clip. File names must be local basenames. URLs, parent paths and symlink
assets are rejected. Copy new files to the profile's static asset directory only
during an authorized deployment. The videos run locally; no Mac video server
is needed for normal playback.

The packaged chooser offers TV → Background and TV → Screensaver, with independent
choices from the same catalog. This chooser has offline tests; hardware validation
is still required. Keep its status separate from the already verified local player.

## Resource use and space

Start with one short clip. 6 Mbit/s is roughly 0.75 MB per second before overhead,
so one minute is about 45 MB. Multiple 4K files can exhaust the TV's writable
partition. Keep at least 64 MiB reserve plus backup/cache space; measure actual
free space and file sizes before transfer. Reuse a single file for Home and saver.

Stop the owned video player when leaving Home. Never stop another app's player.
No GIF or canvas-decoding fallback is supplied; a static poster is safer.

## Automatic screensaver limits

Manual video saver and Back from Home were confirmed. The real ten-minute Home
idle test and a custom saver during paused Netflix were not completed.
Do not activate a global “no keys for ten minutes” timer: it can cover a playing
movie, and switching to DMP can disrupt a streaming session.
