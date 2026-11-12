#!/usr/bin/env python3
"""Check the PUBLIC flat source kit. No network access; never prints matched secrets."""
from pathlib import Path
import re,ipaddress,subprocess,json
ALLOWED={
 '.gitignore','README.md','README.de.md','MASTERPROMPT.md','AGENTS.md','CLAUDE.md',
 'START-HERE.md','COMPATIBILITY.md','VIDAA-MODELS.md','NATIVE-ACCESS.md','RECOVERY.md','ANIMATED-WALLPAPERS.md',
 'DNS.md','PRIVACY.md','SECURITY.md','CREDITS.md','CONTRIBUTING.md','DISCOVERABILITY.md',
 'LICENSE','LICENSE.alvidaa.txt','LICENSE.free-my-tv.txt','LICENSE.metal-fx.txt',
 'native-platform.js','native-core.js','native-dock.js','native-actions.js','native-media.js',
 'native-video.js','native-saver.js','native-entry.js','build.mjs','prepare-media.py','dns-rules.py',
 'check.mjs','check.py','check-video.cjs','privacy-check.py','config.example.json',
 'compatibility.json','dns-candidates.json','preview.jpg','metal-icon-atlas.png','metal-tab-atlas.png',
 'agent.py','check-agent.py','check-bundle.mjs','device.example.json','AGENT-START.md',
 'SIMULATION.md','.github/workflows/offline-checks.yml',
 'model_tools.py','model-research.json','build-port.mjs','check-port.py',
 'PORTING.md','WORKED-EXAMPLE.md','LICENSE-SCOPE.md','ACCESS-RESEARCH.md'
}
def jpeg_private_metadata(data):
    if data[:2]!=b'\xff\xd8':return True
    pos=2
    while pos<len(data):
        if data[pos]!=255:return True
        while pos<len(data) and data[pos]==255:pos+=1
        marker=data[pos];pos+=1
        if marker in (0xda,0xd9):return False
        if marker in (0x01,0xd8) or 0xd0<=marker<=0xd7:continue
        size=int.from_bytes(data[pos:pos+2],'big')
        if size<2 or pos+size>len(data):return True
        if marker in (0xe1,0xed,0xfe):return True
        pos+=size
    return True
def issues(path):
    data=path.read_bytes();out=[]
    if path.name=='preview.jpg':
        return ['JPEG contains disallowed metadata or is invalid'] if jpeg_private_metadata(data) else []
    if path.suffix=='.png':
        return ['PNG contains textual/EXIF metadata'] if any(x in data for x in [b'tEXt',b'iTXt',b'zTXt',b'eXIf']) else []
    s=data.decode('utf-8')
    patterns={
      'private key':r'-----BEGIN (?:[A-Z]+ )*PRIVATE KEY-----',
      'GitHub token':r'\bgh[pousr]_[A-Za-z0-9]{20,}',
      'personal filesystem path':r'/(?:Users|home)/[A-Za-z0-9_.-]+/',
      'email address':r'\b[A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
      'MAC address':r'\b(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}\b'
    }
    for label,pattern in patterns.items():
        if re.search(pattern,s):out.append(label)
    for m in re.finditer(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])',s):
        try:ip=ipaddress.ip_address(m.group())
        except ValueError:continue
        allowed=any(ip in n for n in [ipaddress.ip_network('192.0.2.0/24'),ipaddress.ip_network('198.51.100.0/24'),ipaddress.ip_network('203.0.113.0/24')])
        if not allowed and m.group() not in ['0.0.0.0','127.0.0.1','224.0.0.1']:out.append('non-documentation network address')
    return out
def main():
    root=Path(__file__).resolve().parent;fail=[]
    def walk(directory):
        for p in directory.iterdir():
            name=p.relative_to(root).as_posix()
            if directory==root and name in {'.git','.private','__pycache__'}:continue
            if p.is_symlink():fail.append((name,'unexpected symlink'));continue
            if p.is_dir():
                if any(n.startswith(name+'/') for n in ALLOWED):walk(p)
                else:fail.append((name,'unexpected directory'))
                continue
            if not p.is_file() or name not in ALLOWED:fail.append((name,'unexpected file'));continue
            for issue in issues(p):fail.append((name,issue))
    walk(root)
    if (root/'.git').exists():
        tracked=subprocess.run(['git','ls-files'],cwd=root,capture_output=True,text=True,check=True).stdout.splitlines()
        for name in tracked:
            if name not in ALLOWED:fail.append((name,'private/unapproved tracked path'))
    missing={n for n in ALLOWED if not (root/n).is_file()}
    for n in sorted(missing):fail.append((n,'missing release file'))
    print(json.dumps({'ok':not fail,'findings':[{'file':f,'type':t} for f,t in fail],'networkUsed':False},indent=2))
    raise SystemExit(1 if fail else 0)
if __name__=='__main__':main()
