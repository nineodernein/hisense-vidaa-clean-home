# Remove Hisense VIDAA home ads with TV-only DNS filtering

DNS filtering is independent of the custom dock. It can reduce home banners and
promotional surfaces without replacing firmware. It cannot promise complete
privacy or remove ads embedded in streaming content.

## Evidence and proposed rules

dns-candidates.json records each hostname, provider, observed evidence, inferred
purpose and breakage risk. The small home group includes:
- layout-ui-eu.vidaahub.com: a targeted reference trial plus cold start removed
  the large banner; app access was user-confirmed.
- crtv-mntz.vidaahub.com: a targeted trial was retained for intermediate promos.

Hostname purposes are partly inferred. These observations apply to one device,
not all regions/firmware. The optional reporting/resource group is separate.

Broader research:
[ipanalytics/Hisense-VIDAA-DNS-Clean-TV-Blocklist](https://github.com/ipanalytics/Hisense-VIDAA-DNS-Clean-TV-Blocklist).
Review its categories and compatibility warnings. This project does not silently
import that entire changing list.

## AdGuard Home: generate, review, then activate

1. Use a trusted DNS filter already under your control, or follow the official
   [AdGuard Home setup](https://github.com/AdguardTeam/AdGuardHome/wiki/Getting-Started).
2. Note the TV's current DNS/network settings and identify its stable client IP.
3. Generate proposed rules on your computer. This documentation address is an
   example only; replace it with your TV's actual address locally:

```sh
python3 dns-rules.py --client 192.0.2.10 --group home
```

4. Review the output. Add one rule to AdGuard Home's custom filtering rules.
   Each rule contains a client restriction. Never remove it to “make it work”.
5. Set only the TV's DNS to your resolver. Do not change router-wide DHCP/DNS.
   Preserve IP/gateway/netmask; DNS and default gateway are different settings.
   A public secondary DNS can bypass filtering; understand the device's fallback.
6. Test resolver reachability, cold-start behavior, apps, login, playback and
   firmware update checks. Add the next rule only after checking the first.
7. Roll back that one rule if a needed feature breaks. Restore previous TV DNS
   if the resolver will be unavailable.

Pi-hole needs an equivalent dedicated client/group configuration; AdGuard syntax
must not be pasted into a Pi-hole domain list. See the official
[Pi-hole group-management documentation](https://docs.pi-hole.net/group_management/).

A DNS log shows name lookups, not decrypted content. IPv6 DNS, cached IP addresses,
hardcoded DNS and encrypted DNS can affect coverage. Do not compensate with blind
network-wide firewall rules. No security-update or authentication endpoints are
included here.

ACR, microphone permissions, personalized advertising and account settings are
separate controls. ACR is not evidence of microphone recording.
