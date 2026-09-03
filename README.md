# Multi-Node Linux Home Lab (WSL2)

A small multi-distro Linux environment I built inside WSL2 to study for LPIC-1 hands-on, after two exam attempts made it clear I needed more practical repetition than reading alone was giving me. It runs three separate Linux servers plus a containerized web stack, all on a low-spec laptop.

## Why WSL2 instead of VirtualBox/VMware

My laptop has 4GB RAM (3.8GB usable) and a dual-core Celeron CPU — not enough headroom to run three full GUI-based VMs at once, since each one reserves a fixed chunk of RAM whether it's busy or not. WSL2 distros share a single Linux kernel and only use memory as they need it, so I could run three headless servers plus a Docker stack without the host slowing down noticeably in daily use.

> *I haven't formally benchmarked the RAM difference between this setup and full VMs — that's on my list. For now this is a practical description of why I chose this approach, not a measured comparison.*

**Host machine:**
- DESKTOP-HP3VGMTTG (Acer Aspire A315-34)
- Intel Celeron N4000C @ 1.10GHz, 2 cores / 2 threads
- 4.00 GB RAM (3.81 GB usable)
- Intel UHD Graphics 600 (512MB)
- ~480GB SSD

## Layout

```
        [ Windows 11 Host — WSL2, networkingMode=mirrored ]
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
[ Node 1: Ubuntu 22.04 ] [ Node 2: Ubuntu 24.04 ] [ Node 3: Fedora 44 ]
  jump box / supervisor      test environment       Red Hat–family sandbox
        │                         │                       │
        ├─ SSH (port 22)         └─ SSH (port 2223)       └─ SSH (port 2222)
        ├─ Nginx (Docker)
        ├─ PHP-FPM (Docker)
        └─ MariaDB (Docker)
```

| Node | User | OS | What it's for | Package tool |
|---|---|---|---|---|
| Node 1 | `lenamile_lpi` | Ubuntu 22.04 LTS | Main box, jump host to the others | apt |
| Node 2 | `lenamile23_server2` | Ubuntu 24.04 LTS | Separate test environment | apt |
| Node 3 | `sysadmin_modiri` | Fedora 44 | Red Hat–family practice (dnf/rpm instead of apt/dpkg) | dnf |
| Web stack | — | Alpine/Debian containers | Nginx + PHP-FPM + MariaDB | Docker Compose |

## What's in here

### 1. LEMP stack in Docker
Nginx reverse-proxies requests to PHP-FPM, which talks to a separate MariaDB container. Each service is its own container managed with Docker Compose, so I could break and rebuild individual pieces without taking down the whole stack — useful for practicing troubleshooting one layer at a time.

### 2. Mirrored networking
By default, WSL2 distros sit behind NAT and aren't reachable the way a real LAN device would be. I set `networkingMode=mirrored` in `%USERPROFILE%\.wslconfig` so each distro shares the host's actual network interface. That let me test reachability, firewall rules, and inter-node connectivity closer to how it would work on real separate machines.

```powershell
# %USERPROFILE%\.wslconfig
[wsl2]
networkingMode=mirrored
```

Verified connectivity between nodes with a basic ping test:

```
ping -c 4 172.19.136.65
# 4 packets transmitted, 4 received, 0% packet loss
```

### 3. SSH key-based access across nodes
Password auth is off; each node uses key-based SSH. Node 1 acts as the jump box I work from, connecting out to Nodes 2 and 3.

Since mirrored networking means all three distros share one IP space, I put each node's SSH daemon on its own port to avoid conflicts: Node 1 on the default port 22, Node 2 on 2223, Node 3 on 2222.

```bash
# generate a 4096-bit key pair on Node 1
ssh-keygen -t rsa -b 4096

# copy the public key to the other nodes
ssh-copy-id -p 2223 lenamile23_server2@localhost
ssh-copy-id -p 2222 sysadmin_modiri@localhost
```

### 4. Least-privilege access on Fedora
Rather than working as root on Node 3, I created a standard user (`sysadmin_modiri`) and granted sudo access through a dedicated file in `/etc/sudoers.d/` instead of editing `/etc/sudoers` directly — this keeps the change isolated and easy to remove without risking the main sudoers file.

```bash
echo "sysadmin_modiri ALL=(ALL) ALL" > /etc/sudoers.d/sysadmin_modiri
chmod 0440 /etc/sudoers.d/sysadmin_modiri
```

### 5. Building a WSL image from a Docker container
Wanted a Fedora WSL distro but there was no official WSL image, so I built one from the official Docker image instead: exported a running Fedora container's filesystem to a tarball, then imported that tarball as a new WSL distro.

```bash
docker run --rm fedora:latest tar --exclude='./sys' --exclude='./proc' \
  --exclude='./dev' --exclude='./run' -cf - . > fedora-rootfs.tar

wsl --import Fedora-Server C:\WSL\FedoraServer fedora-rootfs.tar
```

### 6. Memory usage script (Python)
A small script on Node 1 (`~/projects/lemp-stack/analytics/monitor.py`) that reads `/proc/meminfo` directly, parses total/available memory over a sampling window, and plots it with Pandas + Seaborn — mostly to have a real, working example of scripting against a live system file rather than a static dataset.

Output: `memory_utilization_DESKTOP-HP3VGMTTG.png`

## LPIC-1 coverage so far

This lab and the accompanying 16-week study log cover **Exam 101** material:

- Topic 101 — System Architecture
- Topic 102 — Linux Installation & Package Management
- Topic 103 — GNU & Unix Commands
- Topic 104 — Devices, Filesystems, FHS

**Exam 102** (105–110: shell scripting, user interfaces, admin tasks, essential services, networking fundamentals, security) is the next phase — the SSH and sudoers work above already touches Topics 109 and 110, so the next round of labs will build those out properly and document them the same way.

## What I'd still like to add

- Actual `free -h` / `htop` output comparing this setup to a baseline, instead of an estimated number
- A basic cron job + log rotation example (Topic 107/108)
- A simple shell script with error handling (Topic 105)
- A short write-up per lab: what broke, how I diagnosed it, how I fixed it
