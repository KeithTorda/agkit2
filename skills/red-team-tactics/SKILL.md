---
name: red-team-tactics
description: "Adversary-simulation reference for authorised security engagements - MITRE ATT&CK phases, reconnaissance, privilege escalation, lateral movement, Active Directory attack paths, and reporting with detection-gap analysis. Use only for penetration testing and red-team exercises the user is authorised to run; not loaded for application development. Triggers on: red team, adversary simulation, threat emulation, MITRE ATT&CK, pentest tactics, offensive security."
version: 2.0.0
---

# Red Team Tactics

> Scope: authorised engagements only, inside a signed rules-of-engagement document with defined targets, windows, and stop conditions. Every technique and tool below assumes that authorisation. The purpose is to find the detection and response gaps a checklist misses and improve defences — never unauthorised access. This skill is not loaded for application development.

Adversary-simulation reference organised on the MITRE ATT&CK framework. Emulate a real threat actor's tradecraft end to end; the deliverable is a defence that now sees the attack, not a foothold.

## 1. Attack lifecycle (MITRE ATT&CK)

```
RECON -> INITIAL ACCESS -> EXECUTION -> PERSISTENCE -> PRIVILEGE ESC
  -> DEFENSE EVASION -> CREDENTIAL ACCESS -> DISCOVERY -> LATERAL MOVEMENT
  -> COLLECTION -> C2 -> EXFILTRATION -> IMPACT
```

Map every action to its ATT&CK technique ID (Kerberoasting = T1558.003, and so on) so the blue team can check whether their telemetry covers it. The value of the exercise is the gap analysis, not the compromise.

## 2. Standard toolchain (Sept 2026)

Authorised use only — these are attack tools, and running them against a system outside your written scope is a crime, not a test.

| Stage | Tools |
|---|---|
| OS / attack host | Kali Linux 2024.x or Parrot; a Windows attack host (Commando VM) for native AD tradecraft |
| Recon | nmap 7.9x, subfinder, amass, ffuf, httpx; passive OSINT before any active scan |
| Web | Burp Suite 2025 (Pro for active scan), nuclei v3 (+ community templates), gobuster / feroxbuster, sqlmap |
| Exploitation | Metasploit 6.x, impacket (psexec/wmiexec/smbexec, secretsdump), searchsploit |
| Credential access | mimikatz, impacket-secretsdump, hashcat / john |
| AD / identity | BloodHound CE (SharpHound or bloodhound-python collector), Rubeus, Certipy / Certify, Kerbrute, NetExec (nxc) |
| C2 | Sliver or Havoc (modern, actively maintained), Mythic; Cobalt Strike (legacy commercial) |

Prefer the maintained tool over the well-known deprecated one: NetExec (nxc) replaced CrackMapExec; BloodHound CE replaced BloodHound Legacy.

## 3. Reconnaissance

Passive first — certificate transparency, DNS, OSINT, breach data send no packets to the target, stay invisible, and shape the active phase. Active recon (nmap, ffuf, subfinder resolution) is louder and detectable: scope it and pace it. What you are after: the technology stack (picks the exploit), identities and emails (phishing, password spraying), external ranges (scan scope), and third parties (the softer supply-chain path).

## 4. Initial access

| Vector | When it fits |
|---|---|
| Phishing / pretext | Human target reachable, email in scope |
| Public-facing exploit | An exposed service is actually vulnerable (validate, do not assume) |
| Valid credentials | Leaked, sprayed, or cracked — often the quietest way in |
| Supply chain | A trusted third party or dependency is the weaker target |

Password spraying (one password across many accounts, slow, under the lockout threshold) beats brute force (many passwords, one account, trips lockout). Kerbrute or NetExec, throttled to the domain's lockout policy.

## 5. Privilege escalation

Enumerate before you exploit — a scripted sweep finds the quick win faster than a kernel exploit that may crash the host.

- Windows: WinPEAS / PowerUp / SharpUp for the sweep. Look for unquoted service paths, weak service ACLs, abusable token privileges (`SeImpersonate` -> potato attacks), stored credentials, and AlwaysInstallElevated.
- Linux: LinPEAS for the sweep. Check `sudo -l`, SUID/SGID binaries (cross-reference GTFOBins), writable cron and `PATH`, Linux capabilities, and kernel version last — kernel exploits are the least reversible option.

## 6. Lateral movement

Move with credentials, not exploits, wherever possible — it is quieter and reads as legitimate admin activity.

| Credential | Technique | Tool |
|---|---|---|
| Password / NT hash | Pass-the-hash | impacket, NetExec |
| Kerberos ticket | Pass-the-ticket, overpass-the-hash | Rubeus, mimikatz |
| Certificate | PKINIT authentication (see ADCS below) | Rubeus, Certipy |

Paths: admin shares (SMB), WinRM, RDP, SSH. Blend with business hours and existing service accounts.

## 7. Active Directory attacks

AD is where most internal engagements are won. Run BloodHound CE first — it maps the shortest path from your foothold to Domain Admin and turns guesswork into a graph. The classic paths still work; the certificate and delegation paths below now dominate real engagements.

Classic:

| Attack | What it yields | Tool | ATT&CK |
|---|---|---|---|
| Kerberoasting | Service-account password, cracked offline | Rubeus, impacket-GetUserSPNs | T1558.003 |
| AS-REP roasting | Hash of accounts with pre-auth disabled | Rubeus, impacket-GetNPUsers | T1558.004 |
| DCSync | Any account's hash via replayed replication | mimikatz, secretsdump | T1003.006 |
| Golden / Silver ticket | Forged TGT / service ticket for persistence | mimikatz, Rubeus | T1558.001/.002 |

Modern dominant paths:

- **ADCS certificate abuse (ESC1-ESC8):** misconfigured certificate templates and CA settings let a low-privileged user enrol a certificate that authenticates as anyone — ESC1 (requester-supplied SAN), ESC6 (CA SAN flag), ESC8 (NTLM relay to the web-enrollment endpoint), and the rest. `certipy find -vulnerable` enumerates them; `certipy req` weaponises them. Certify is the Windows-native equivalent.
- **RBCD (resource-based constrained delegation):** with write access to a computer's `msDS-AllowedToActOnBehalfOfOtherIdentity` (for example GenericWrite), add a controlled computer account (default MachineAccountQuota is 10) and impersonate any user to that host via S4U. impacket `rbcd.py` + `addcomputer.py` + `getST.py`, or Powermad + Rubeus.
- **Shadow credentials:** with write access to a target's `msDS-KeyCredentialLink`, add your own key and authenticate via PKINIT to recover a TGT and the NT hash. pyWhisker / Whisker plants the key, then Rubeus or Certipy uses it (needs a DC that supports PKINIT).
- **Cross-forest trust abuse:** a trust is an attack path, not a boundary — enumerate foreign group memberships, inter-realm ticket abuse, and ACL or ADCS paths that cross the trust. BloodHound CE maps them; Rubeus abuses inter-realm tickets. (SID filtering blocks naive SID-history injection, but specific paths survive.)

## 8. Defense evasion and OPSEC

LOLBins (living off the land — `certutil`, `rundll32`, `wmic`) blend with normal activity; obfuscation, timestomping, and selective log handling reduce signal. But full stealth is rarely the point of an authorised test: coordinate with the blue team, use encrypted channels, and mimic legitimate traffic so you measure real detection instead of tripping every alarm at once.

## 9. Reporting and detection-gap analysis

The report is the product. Document the full attack chain — how initial access was gained, each technique (with its ATT&CK ID), what objective it achieved, and where detection should have fired but did not.

For every successful technique, answer three questions: what control should have detected or blocked it, why it did not, and the specific improvement (a detection rule, a hardened template, a removed privilege). A finding without a remediation is half a finding.

## 10. Ethical boundaries

Always: stay strictly within scope, minimise impact, take a proof of concept rather than the data, document every action with timestamps, and report a real active threat immediately if you find one.

Never: destroy or exfiltrate production data, cause denial of service unless it is explicitly scoped, move past the first proof of impact, or retain sensitive data after the engagement.

> Red team emulates attackers to improve defences. If an action would harm the client more than it teaches them, it is out of scope.
