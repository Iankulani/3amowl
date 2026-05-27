#!/bin/bash
# 3AMOWL Bash Installation Script
# Supports: Ubuntu/Debian, CentOS/RHEL, Fedora, Arch Linux, macOS

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                         🦉 3AMOWL INSTALLER v1.0.0                            ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [[ -f /etc/os-release ]]; then
            . /etc/os-release
            OS=$ID
            VER=$VERSION_ID
        else
            OS="linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        OS="unknown"
    fi
    echo -e "${GREEN}✓ Detected OS: ${OS}${NC}"
}

# Check root/sudo
check_privileges() {
    if [[ $EUID -ne 0 ]]; then
        echo -e "${YELLOW}⚠️  Some features require root privileges (firewall, raw packets)${NC}"
        echo -e "${YELLOW}   Run with sudo for full functionality${NC}"
        USE_SUDO="sudo"
    else
        USE_SUDO=""
    fi
}

# Install system dependencies
install_system_deps() {
    echo -e "\n${BLUE}📦 Installing system dependencies...${NC}"
    
    case $OS in
        ubuntu|debian)
            $USE_SUDO apt-get update
            $USE_SUDO apt-get install -y \
                python3 python3-pip python3-dev \
                nmap netcat-openbsd openssh-client \
                curl dnsutils traceroute iputils-ping \
                whois tcpdump build-essential \
                libssl-dev libffi-dev
            ;;
        centos|rhel|fedora)
            if [[ "$OS" == "fedora" ]]; then
                $USE_SUDO dnf install -y \
                    python3 python3-pip python3-devel \
                    nmap nc openssh-clients \
                    curl bind-utils traceroute iputils \
                    whois tcpdump gcc \
                    openssl-devel libffi-devel
            else
                $USE_SUDO yum install -y epel-release
                $USE_SUDO yum install -y \
                    python3 python3-pip python3-devel \
                    nmap nc openssh-clients \
                    curl bind-utils traceroute iputils \
                    whois tcpdump gcc \
                    openssl-devel libffi-devel
            fi
            ;;
        arch)
            $USE_SUDO pacman -S --noconfirm \
                python python-pip \
                nmap netcat openssh \
                curl bind-tools traceroute iputils \
                whois tcpdump gcc \
                openssl libffi
            ;;
        macos)
            if ! command -v brew &> /dev/null; then
                echo -e "${YELLOW}⚠️  Homebrew not found. Installing...${NC}"
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            brew install python3 nmap netcat openssh curl bind traceroute whois tcpdump
            ;;
        *)
            echo -e "${RED}❌ Unsupported OS: $OS${NC}"
            exit 1
            ;;
    esac
    
    echo -e "${GREEN}✓ System dependencies installed${NC}"
}

# Install Python packages
install_python_packages() {
    echo -e "\n${BLUE}📦 Installing Python packages...${NC}"
    
    # Upgrade pip
    python3 -m pip install --upgrade pip
    
    # Install from requirements.txt if exists
    if [[ -f "requirements.txt" ]]; then
        python3 -m pip install -r requirements.txt
    else
        python3 -m pip install \
            requests psutil colorama cryptography \
            shodan paramiko discord.py telethon \
            selenium webdriver-manager slack-sdk \
            qrcode[pil] pyshorteners python-nmap \
            scapy python-whois tqdm prompt-toolkit \
            pyperclip ipaddress dnspython
    fi
    
    echo -e "${GREEN}✓ Python packages installed${NC}"
}

# Check and install optional tools
install_optional_tools() {
    echo -e "\n${BLUE}🎯 Installing optional tools...${NC}"
    
    # ChromeDriver for WhatsApp
    if [[ "$OS" != "macos" ]]; then
        if ! command -v chromedriver &> /dev/null; then
            echo -e "${YELLOW}⚠️  ChromeDriver not found (optional for WhatsApp)${NC}"
            echo -e "${YELLOW}   Install with: pip install webdriver-manager${NC}"
        fi
    fi
    
    # signal-cli for Signal
    if ! command -v signal-cli &> /dev/null && [[ "$OS" != "macos" ]]; then
        echo -e "${YELLOW}⚠️  signal-cli not found (optional for Signal)${NC}"
        echo -e "${YELLOW}   Install from: https://github.com/AsamK/signal-cli${NC}"
    fi
    
    echo -e "${GREEN}✓ Optional tools check complete${NC}"
}

# Create directory structure
create_directories() {
    echo -e "\n${BLUE}📁 Creating directory structure...${NC}"
    
    mkdir -p .3amowl
    mkdir -p .3amowl/payloads
    mkdir -p .3amowl/workspaces
    mkdir -p .3amowl/scans
    mkdir -p .3amowl/sessions
    mkdir -p .3amowl/nikto_results
    mkdir -p .3amowl/whatsapp_session
    mkdir -p .3amowl/phishing_pages
    mkdir -p .3amowl/shodan_results
    mkdir -p .3amowl/reports
    mkdir -p .3amowl/traffic_logs
    mkdir -p .3amowl/phishing_templates
    mkdir -p .3amowl/phishing_logs
    mkdir -p .3amowl/captured_credentials
    mkdir -p .3amowl/ssh_keys
    mkdir -p .3amowl/ssh_logs
    mkdir -p .3amowl/time_history
    mkdir -p .3amowl/netcat_listeners
    mkdir -p .3amowl/temp
    
    echo -e "${GREEN}✓ Directory structure created${NC}"
}

# Run requirements check
run_requirements_check() {
    echo -e "\n${BLUE}🔍 Running requirements check...${NC}"
    
    if [[ -f "requirements-check.py" ]]; then
        python3 requirements-check.py
    else
        echo -e "${YELLOW}⚠️  requirements-check.py not found${NC}"
    fi
}

# Set up shell alias
setup_alias() {
    echo -e "\n${BLUE}🔧 Setting up shell alias...${NC}"
    
    SCRIPT_DIR=$(pwd)
    ALIAS_CMD="alias 3amowl='python3 $SCRIPT_DIR/3amowl.py'"
    
    if [[ -f ~/.bashrc ]]; then
        if ! grep -q "alias 3amowl=" ~/.bashrc; then
            echo "$ALIAS_CMD" >> ~/.bashrc
            echo -e "${GREEN}✓ Added to ~/.bashrc${NC}"
        fi
    fi
    
    if [[ -f ~/.zshrc ]]; then
        if ! grep -q "alias 3amowl=" ~/.zshrc; then
            echo "$ALIAS_CMD" >> ~/.zshrc
            echo -e "${GREEN}✓ Added to ~/.zshrc${NC}"
        fi
    fi
    
    echo -e "${YELLOW}💡 Run 'source ~/.bashrc' or 'source ~/.zshrc' to use '3amowl' command${NC}"
}

# Main installation
main() {
    detect_os
    check_privileges
    install_system_deps
    install_python_packages
    install_optional_tools
    create_directories
    run_requirements_check
    setup_alias
    
    echo -e "\n${PURPLE}════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ 3AMOWL installation complete!${NC}"
    echo -e "${CYAN}🚀 Run: python3 3amowl.py${NC}"
    echo -e "${CYAN}📖 Or use '3amowl' alias after reloading your shell${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════════════${NC}"
}

# Run main
main