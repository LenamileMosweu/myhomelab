# Troubleshooting Documentation

## Issue 1: Port Conflict (8080 already in use)
**Date:** 2026-04-08
**Error:** `Bind for 0.0.0.0:8080 failed: port is already allocated`
**Solution:** Changed port mapping from 8080:80 to 8888:80 in docker-compose.yml
**Command:** `sed -i 's/8080:80/8888:80/g' docker-compose.yml`

## Issue 2: PHP MySQL Driver Missing
**Date:** 2026-04-09
**Error:** `Database Error: could not find driver`
**Solution:** Installed pdo_mysql and mysqli extensions in PHP container
**Commands:**
docker exec lemp-stack_php_1 docker-php-ext-install pdo_mysql mysqli
docker restart lemp-stack_php_1

## Issue 3: Container Name Confusion
Date: 2026-04-08
Issue: Couldn't access containers using lemp-stack-nginx-1
Root Cause: Docker Compose uses underscores (lemp-stack_nginx_1) not hyphens
Solution: Used correct naming convention with underscores

Lessons Learned
Always verify container names with docker ps
Check Docker Desktop WSL2 integration settings
PHP containers need explicit driver installation for database connectivity
Port conflicts are common - always check availability first
