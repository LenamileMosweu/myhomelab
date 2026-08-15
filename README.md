# 🖥️ Multi-Node Hybrid DevOps & System Administration HomeLab

A production-grade, multi-distribution Linux server infrastructure lab built natively on top of the Windows Subsystem for Linux (WSL2) hypervisor layer. This project showcases container orchestration alongside deep Linux engineering, cross-platform networking, privilege isolation models, and automated resource observability.

---

## 💻 Bare-Metal Host Hardware Optimization Profile

To showcase production-grade optimization and resource profiling across severe hardware limitations, this entire multi-distribution enterprise architecture lab was explicitly engineered to maintain stability under the following strict physical machine parameters:

* **Host Machine Identity:** DESKTOP-HP3VGMTTG (Aspire A315-34)
* **Processor Engine:** Intel(R) Celeron(R) N4000C CPU @ 1.10GHz (2 Cores / 2 Logical Threads)
* **Physical Installed Memory Volatile Pool:** 4.00 GB Total System RAM (3.81 GB usable)
* **Graphics Infrastructure Layer:** Intel(R) UHD Graphics 600 (512 MB allocated)
* **Storage Array Subsystem:** 480 GB Solid-State Drive (SSD) Partition Matrix

### 🔋 Resource Management Strategy Overview:
By replacing heavy standard GUI virtual machines (VirtualBox/VMware) with lightweight, head-less command-line distributions sharing a unified, compressed WSL2 kernel space, the memory footprint required for running 3 independent Linux servers plus an active Docker web container stack dropped from a projected **12.5GB RAM** down to an active operational footprint of under **1.8GB RAM**. This allowed for robust systems engineering testing with 0% host system slowdown or thermal degradation.

---

## 🏗️ Integrated Cluster Architecture Design

The environment bridges containerized application components (LEMP Stack) and distinct standalone enterprise Linux nodes communicating on a shared subsystem space.

```text
       [ Windows 11 Physical Host (Mirrored Network Space Pool) ]
                                   │
         ┌─────────────────────────┼────────────────────────┐
         ▼                         ▼                        ▼
 [ Node 1: Ubuntu 22.04 ]   [ Node 2: Ubuntu 24.04 ]  [ Node 3: Fedora 44 ]
   (Supervisor / Jump Box)     (Isolated Infrastructure)  (Red Hat Sandbox)
         │                                 │                    │
         ├─► SSH Service (Port 22)         └─► SSH Service      └─► SSHD Daemon
         ├─► Nginx Container (Port 80)         (Port 2223)          (Port 2222)
         ├─► PHP-FPM Container
         └─► MariaDB Container
```

| Server Node / Service | Profile Identity | Operating System | Primary Core Function | Infrastructure Management |
| :--- | :--- | :--- | :--- | :--- |
| **Nginx / PHP / MariaDB** | Containerized | Alpine / Debian | Core Microservices Web Application Stack | Docker Compose Layer |
| **Node 1 (Host Base)** | `lenamile_lpi` | Ubuntu 22.04 LTS | Virtualization Supervisor / Administrative Jump Box | `apt` / SSH Port 22 Control |
| **Node 2 (Isolated)**| `lenamile23_server2` | Ubuntu 24.04 LTS | Secondary Infrastructure Test Environment Node | `apt` / SSH Port 2223 (`systemd`) |
| **Node 3 (Fedora)** | `sysadmin_modiri` | Fedora 44 (Raw) | Independent Red Hat Ecosystem Cluster Node | `dnf` / SSH Port 2222 (`systemd`) |

---

## 🛠️ Core Sysadmin Engineering Implementations

### 1. 🐳 Containerized Web Application Stack (LEMP Engine)
* **Orchestration:** Implemented a microservices architecture using Docker Compose managing isolated runtimes.
* **Stack Layout:** Reverse-proxy routing handles external transactions via **Nginx**, parsing programmatic operations execution flags cleanly down through independent **PHP-FPM** containers while preserving data frames within segregated stateful **MariaDB** engine layers.

### 2. 🌐 Advanced Subsystem Networking (Mirrored Mode)
By default, WSL distribution nodes sit behind an isolated internal virtual switch using Network Address Translation (NAT). To establish a realistic local environment, the default hypervisor architecture was completely overridden at the host layer:
* **Implementation:** Configured a global configuration utility at `%USERPROFILE%\.wslconfig` enforcing `networkingMode=mirrored`.
* **Result:** All standalone Linux instances mirror the host's physical hardware network interfaces, enabling integrated DNS tunneling and native firewall packet filtering.

### 📡 3. Network Connectivity & Latency Metrics (`ping`)
Inter-node network paths and loopback routing accuracy were audited from the supervisor control center.
```bash
# Auditing the network response path from Node 1 to Node 2 & 3
ping -c 4 172.19.136.65
```
* **Performance Metrics:** 0% packet loss verified across transmissions with sub-millisecond response delay (`~0.132ms` average), confirming stable intra-subsystem capability.

### 🔑 4. Secure Cryptographic Access Layer & Socket Isolation (SSH Mesh Architecture)
To eliminate insecure password vectors, the cluster was engineered using RSA key-pair authentication, designating Node 1 as an administrative Jump Box.
* **Key Generation:** Generated a 4096-bit RSA asymmetric key pair on the supervisor node (`~/.ssh/id_rsa`).
* **Socket Collision Prevention:** Under global mirrored networking mode, all distributions share the host network space pool. To prevent socket configuration deadlocks on default **Port 22**, the daemons were isolated onto unique channel lanes. Node 1 retains standard Port 22, while Node 2 was re-routed to **Port 2223** and Node 3 to **Port 2222**.
```bash
# Secure token exchange protocols used across custom lanes:
ssh-copy-id -p 2223 lenamile23_server2@localhost
ssh-copy-id -p 2222 sysadmin_modiri@localhost
```

### 🛡️ 5. Privilege Model Hardening & Group Access Isolation (`sudoers.d`)
Operating out of an unmitigated `root` terminal profile poses a severe vulnerability. The minimal Fedora deployment was hardened using robust access control patterns:
* Provisioned an unprivileged workspace identity (`sysadmin_modiri`) containing individual home file spaces.
* Patched the administrative permission pool without breaking the main server settings file by injecting a locked file configuration directly into the isolated `sudoers.d` framework:
```bash
echo "sysadmin_modiri ALL=(ALL) ALL" > /etc/sudoers.d/sysadmin_modiri
chmod 0440 /etc/sudoers.d/sysadmin_modiri
```

### 💾 6. OS Image Stripping, Extraction, and Registration
Bypassed standard app stores and operating system catalog installers by stripping an active container down to its core file system structure and manually registering it:
```powershell
# Stripping live runtime memory layers and streaming an OS root footprint directly to disk
docker run --rm fedora:latest tar --exclude='./sys' --exclude='./proc' --exclude='./dev' --exclude='./run' -cf - . > C:\Users\USER\fedora-rootfs.tar

# Low-level manual registration of the extracted image asset into the WSL cluster
wsl --import Fedora-Server C:\WSL\FedoraServer C:\Users\USER\fedora-rootfs.tar
```

### 🐍 7. Infrastructure Observability Automation (Python Performance Diagnostics)
To audit the infrastructure state without running heavy tracking applications, a lightweight Python analytics workspace was successfully deployed and verified.
* **Location:** Deployed on **Node 1 (Ubuntu 22.04 Base)** under the `~/projects/lemp-stack/analytics/` directory path, containing `monitor.py`.
* **Mechanism:** The engine interfaces directly with low-level kernel streams (`/proc/meminfo`) via Regex pattern matching to parse total and available memory limits across short operational windows.
* **Output Artifact:** Automatically processes statistical inputs into a Pandas DataFrame and streams them into a custom-styled Seaborn visualization trace graphic (`memory_utilization_DESKTOP-HP3VGMTTG.png`), validating active metric-gathering capability.

