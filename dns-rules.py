#!/usr/bin/env python3
"""Generate AdGuard Home rules for exactly one TV; never deploy or change DNS."""
import argparse,ipaddress,json
from pathlib import Path
def render(ip,domains):
    target=ipaddress.ip_address(ip)
    if target.is_multicast or target.is_unspecified or target.is_loopback:raise ValueError("Not a TV client address")
    return "\n".join("||"+d+"^$client="+str(target) for d in domains)+"\n"
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--client",required=True)
    p.add_argument("--group",choices=["home","optional"],default="home")
    a=p.parse_args()
    data=json.loads(Path(__file__).with_name("dns-candidates.json").read_text())
    print("! Proposed rules for ONE client. Review DNS.md before applying.")
    print(render(a.client,[x["domain"] for x in data["groups"][a.group]]),end="")
if __name__=="__main__":main()
