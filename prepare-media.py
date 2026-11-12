#!/usr/bin/env python3
"""Prepare a local silent 1080p H.264 loop; no downloads and no TV access."""
import argparse,json,math,re,shutil,subprocess
from pathlib import Path
def graph(duration,speed,fade):
    if not all(math.isfinite(x) for x in (duration,speed,fade)) or not 0.5<=speed<=1.25 or not 0.2<=fade<=3:raise ValueError("Invalid speed/fade")
    total=math.floor(duration/speed*24)/24
    fade=round(fade*24)/24
    if total<2*fade+3:raise ValueError("Clip too short for crossfade and 2-second continuation")
    cycle=round((total-fade)*24)/24
    f=(f"[0:v]setpts=(PTS-STARTPTS)/{speed},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,fps=24,format=yuv420p,settb=AVTB,split=3[a][b][c];"
       f"[a]trim=start={fade}:end={total-fade},setpts=PTS-STARTPTS[main];"
       f"[b]trim=start={total-fade}:end={total},setpts=PTS-STARTPTS[tail];"
       f"[c]trim=start=0:end={fade},setpts=PTS-STARTPTS[head];"
       f"[tail][head]xfade=transition=fade:duration={fade}:offset=0[blend];"
       "[main][blend]concat=n=2:v=1:a=0,split=2[cycle][pad];"
       "[pad]trim=duration=2,setpts=PTS-STARTPTS[cont];"
       "[cycle][cont]concat=n=2:v=1:a=0[out]")
    return f,cycle
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("input",type=Path);p.add_argument("--id",required=True)
    p.add_argument("--label",required=True);p.add_argument("--speed",type=float,default=1.0)
    p.add_argument("--crossfade",type=float,default=1.0)
    p.add_argument("--out",type=Path,default=Path(".private/media"))
    p.add_argument("--dry-run",action="store_true");p.add_argument("--duration",type=float)
    a=p.parse_args()
    if not re.fullmatch("[a-z0-9_-]{1,40}",a.id):p.error("Use a simple media ID")
    if not a.label.strip() or len(a.label)>80:p.error("Invalid label")
    if not a.input.is_file():p.error("Input file missing")
    if a.duration is not None and not a.dry_run:p.error("--duration is only for offline planning; actual exports use ffprobe")
    if a.dry_run and a.duration is not None:duration=a.duration
    else:
        if not shutil.which("ffprobe"):p.error("ffprobe is required; nothing is installed automatically")
        probe=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","json",str(a.input)],capture_output=True,text=True,check=True)
        duration=float(json.loads(probe.stdout)["format"]["duration"])
    filt,cycle=graph(duration,a.speed,a.crossfade)
    video=a.out/(a.id+".mp4");poster=a.out/(a.id+".jpg");meta=a.out/(a.id+".json")
    for f in [video,poster,meta]:
        if f.exists():p.error("Refusing to overwrite "+str(f))
    cmd=["ffmpeg","-nostdin","-n","-i",str(a.input),"-filter_complex",filt,"-map","[out]","-an","-c:v","libx264","-preset","medium","-profile:v","high","-level","4.1","-pix_fmt","yuv420p","-b:v","6M","-maxrate","8M","-bufsize","12M","-g","24","-movflags","+faststart","-map_metadata","-1",str(video)]
    result={"id":a.id,"label":a.label,"video":video.name,"poster":poster.name,"cycle":cycle}
    if a.dry_run:print(json.dumps({"command":cmd,"catalogEntry":result,"tvContacted":False},indent=2));return
    if not shutil.which("ffmpeg"):p.error("ffmpeg is required; nothing is installed automatically")
    a.out.mkdir(parents=True,exist_ok=True,mode=0o700)
    subprocess.run(cmd,check=True)
    subprocess.run(["ffmpeg","-nostdin","-n","-i",str(video),"-frames:v","1","-q:v","2","-map_metadata","-1",str(poster)],check=True,capture_output=True)
    meta.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
