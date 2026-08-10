# Troubleshooting Documentation

## Issue 1: Port Conflict (8080 already in use)
**Date:** 08/04/2026
**Error:** `Bind for 0.0.0.0:8080 failed: port is already allocated`
**Solution:** Changed port mapping from 8080:80 to 8888:80 in docker-compose.yml
**Command:** `sed -i 's/8080:80/8888:80/g' docker-compose.yml`

## Issue 2: PHP MySQL Driver Missing
**Date:** 09/04/2026
**Error:** `Database Error: could not find driver`
**Solution:** Installed pdo_mysql and mysqli extensions in PHP container
**Commands:**
docker exec lemp-stack_php_1 docker-php-ext-install pdo_mysql mysqli
docker restart lemp-stack_php_1

## Issue 3: Container Name Confusion
Date: 08/04/2026
Issue: Couldn't access containers using lemp-stack-nginx-1
Root Cause: Docker Compose uses underscores (lemp-stack_nginx_1) not hyphens
Solution: Used correct naming convention with underscores

Lessons Learned
Always verify container names with docker ps
Check Docker Desktop WSL2 integration settings
PHP containers need explicit driver installation for database connectivity
Port conflicts are common - always check availability first

### 🔍 Scenario 4: Bypassing Missing Core Binary Blocks in Custom OS Tarballs
* **Symptom:** Executing `dnf check-update` inside a manually registered Fedora distribution threw critical configuration dependency path errors: `Unable to open /usr/lib/rpm/rpmrc: No such file or directory`.
* **Root Cause:** A selective include-based `tar` command string dropped secondary directory configurations during file streams, rendering the low-level RPM subsystem unreadable.
* **Resolution:** Switched deployment paradigms. Re-engineered the script to extract the *entire* operating system profile using strict global ignore parameters (`--exclude='./sys' --exclude='./proc'`) instead of hardcoding folders. This captured 100% of required library assets cleanly.

### 🔍 Scenario 5: Resolving Multi-Distribution Cached Sudoer Permission Drops
* **Symptom:** A newly provisioned server profile added to the administrative `wheel` group continually failed `sudo` authentication tests, outputting `user is not in the sudoers file`.
* **Root Cause:** Standard configurations are heavily stripped down in container distributions, leaving group trust properties unregistered within the security access layer.
* **Resolution:** Forced a root override prompt via `wsl -d Fedora-Server -u root`. Created an isolated configuration profile directly inside the `/etc/sudoers.d/` directory and applied a strict permission layer via `chmod 0440` to guarantee verification engine recognition.

### 🔍 Scenario 6: Cryptographic Key Drops and Service Port Collision Under Mirrored Networking
* **Symptom:** Starting the `sshd` daemon on Node 3 failed instantly with error flags: `Job for sshd.service failed because the control process exited with error code`.
* **Root Causes:** 
  1. The minimal container template structure lacked default host cryptographic certificates inside `/etc/ssh/`.
  2. Under global mirrored networking mode, Node 1 and Node 3 attempted to bind to Port 22 simultaneously, inducing a socket configuration lock.
* **Resolution:** Executed `sudo ssh-keygen -A` to force-generate host identities. Modified `/etc/ssh/sshd_config` to reassign Node 3's listening configuration to **Port 2222**, cleanly dividing network space lanes.

