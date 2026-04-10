##  Project Overview
A fully functional LEMP stack (Linux, Nginx, MariaDB, PHP) running in Docker containers on my local machine.This lab demonstrates my system administration skills including container orchestration, service managemnt, and troubleshooting

## Curent Lab Architecture
**Web Server**: Nginx (port 8888)
**Application**: PHP 8.2-FPM
**Database**: MariaDB 10.11
**Orchestration**: Docker Compose
**Environment**: WSL2 Ubuntu on Windows 10

## What's working
Multi-container Docker environment
Nginx serving PHP files
Database with persistent storage
Container networking between services
Custom PHP application with database connectivity

## Skills Demonstrated 
Docker container management ('docker-compose', 'docker-exec', 'docker logs'
Service troubleshooting and log analysis
Database backup and restore procedures
PHP extension installation and configuration
Network configuration between containers

##Recent Troubleshooting Examples
**Resolved port conflict** - changed from port 8080 to 8888
**Fixed PHP MySQL driver** - installed pdo_mysql extension
**Debugged container connectivity** - Verified network isolation
