# 🖥️ Multi-Node Hybrid DevOps & System Administration HomeLab

A production-grade, multi-distribution Linux server infrastructure lab built natively on top of the Windows Subsystem for Linux (WSL2) hypervisor layer. This project showcases container orchestration alongside deep Linux engineering, cross-platform networking, privilege isolation models, and automated observability.

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
         │                                                      │
         ├─► Nginx Container (Port 80)                          └─► SSHD Daemon
         ├─► PHP-FPM Container                                      (Port 2222)
         └─► MariaDB Container
```

| Server Node | Profile Identity | Operating System | Primary Core Function | Infrastructure Management |
| :--- | :--- | :--- | :--- | :--- |
| **Node 1 (Host)** | `lenamile_lpi` | Ubuntu 22.04 LTS | Virtualization Supervisor & Container Engine Platform | `apt` / Docker Compose Layer |
| **Node 2 (Isolated)**| `lenamile23_server2` | Ubuntu 24.04 LTS | Secondary Infrastructure Test Environment Node | `apt` / `systemd` Integration |
| **Node 3 (Fedora)** | `sysadmin_modiri` | Fedora 44 (Raw) | Independent Red Hat Ecosystem Cluster Node | `dnf` / `rpm` Core Subsystem |

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

### 🔑 4. Secure Cryptographic Access Layer (SSH Mesh Architecture)
To eliminate insecure password vectors, the cluster was engineered using RSA key-pair authentication, designating Node 1 as an administrative Jump Box.
* **Key Generation:** Generated a 4096-bit RSA asymmetric key pair on the supervisor node (`~/.ssh/id_rsa`).
* **Boundary Traversal:** Distributed public identity signatures across nodes. Because of the mirrored network adapter mode, Node 3 (Fedora) was hardened to run on a dedicated channel (**Port 2222**) to bypass port collisions with the core host system.
```bash
# Secure token exchange protocols used:
ssh-copy-id lenamile23_server2@localhost
ssh-copy-id -p 2222 sysadmin_modiri@localhost
```
* **Result:** Achieved secure, passwordless, token-based boundary traversal between distinct distributions.

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

### 🐍 7. Infrastructure Observability (Cross-Node Python Analytics)
*(We will insert the Python monitor script details and your generated graph analysis notes right here in the next step!)*

