# 3amowl

3amowl


# 🦉 3AMOWL 

[![License](https://img.shields.io/badge/license-Educational%20Purpose-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-green.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://docker.com)
[![GitLab CI](https://img.shields.io/badge/GitLab%20CI-pipeline-orange.svg)](.gitlab-ci.yml)

## ⚠️ WARNING - FOR AUTHORIZED TESTING ONLY

3AMOWL is an educational command and control (C2) framework designed for authorized penetration testing, red team exercises, and academic cybersecurity labs. It enables security students and professionals to issue commands through seven real-world messaging platforms—Telegram, Slack, iMessage, Discord, Signal, WhatsApp, and a unified web application—to simulate how modern adversaries use legitimate services for covert operations..

# Key educational capabilities:

* Remotely execute shell commands, upload/download files, capture screenshots, and manage keyloggers (within your own lab systems)

* Control multiple agents simultaneously from any supported chat interface

* Observe encrypted C2 traffic blending with normal messaging API calls

* Learn MITRE ATT&CK techniques (T1071.001, T1102, T1059) in a safe, logged environment

* Strict legal & ethical guardrails:

* ✅ Only for systems you own or have written permission to test

* ❌ Never for unauthorized access, surveillance, or malicious use

* Built-in killswitch, domain allow-listing, and educational watermarks

Typical use cases: University cyber ranges, CTF competitions, and internal red team training where Slack, Discord, or Telegram replace traditional HTTP/S listeners.


## 🎯 Features

### 🔍 Information Gathering
- **Shodan Integration** - Search internet-connected devices
- **WHOIS/DNS Lookups** - Domain intelligence
- **IP Geolocation** - Track IP locations
- **Nmap Scanning** - Port and service discovery

### 📡 Network Tools
- **Netcat Commands** - Bind shells, reverse shells, file transfer
- **SSH Command Execution** - Remote command execution
- **Port Scanning** - Comprehensive port discovery
- **Traceroute/Ping** - Network diagnostics

### 🚀 Traffic Generation
- **ICMP/TCP/UDP Packets** - Custom packet crafting
- **HTTP/HTTPS Requests** - Web traffic simulation
- **DNS/ARP Traffic** - Protocol-specific testing
- **Flood Generation** - DDoS simulation (controlled)

### 🎣 Social Engineering
- **Phishing Page Generation** - Facebook, Instagram, Twitter, Gmail, LinkedIn
- **Credential Capture** - Automatic credential logging
- **QR Code Generation** - For phishing links
- **URL Shortening** - Obfuscate malicious links

### 🤖 Multi-Platform Bots
- **Discord Bot** - Command execution via Discord
- **Telegram Bot** - Remote control via Telegram
- **WhatsApp Bot** - WhatsApp integration
- **Slack Bot** - Team collaboration
- **Signal Bot** - Encrypted messaging
- **iMessage Bot** - macOS integration

### 🛡️ Defense & Monitoring
- **Threat Detection** - Real-time attack detection
- **IP Management** - Block/Unblock IP addresses
- **Auto-blocking** - Automatic threat response
- **Session Tracking** - User activity logging

### 📊 Reporting
- **Command History** - Track all activities
- **Threat Reports** - Security incident logging
- **Performance Metrics** - System health monitoring
- **Export Capabilities** - JSON/CSV export

## 🚀 Quick Start

### Installation

#### Linux/macOS

# Clone repository
```bash
git clone https://github.com/Iankulani/3amowl.git
cd 3amowl
```

# Run installer
```bash
chmod +x install.sh
./install.sh
```
# Or run directly
python3 3amowl.py
