@echo off
title 3AMOWL Installer
color 0B

echo.
echo ============================================================
echo               🦉 3AMOWL INSTALLER v1.0.0
echo ============================================================
echo.

:: Check Python
echo [*] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo [INFO] Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

:: Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo [OK] Python %PYTHON_VER% found

:: Check pip
echo.
echo [*] Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip not found
    echo [INFO] Installing pip...
    python -m ensurepip --upgrade
)
echo [OK] pip found

:: Upgrade pip
echo.
echo [*] Upgrading pip...
python -m pip install --upgrade pip

:: Install Python packages
echo.
echo [*] Installing Python packages...
python -m pip install requests psutil colorama cryptography
python -m pip install shodan paramiko
python -m pip install discord.py telethon
python -m pip install selenium webdriver-manager
python -m pip install slack-sdk
python -m pip install qrcode[pil] pyshorteners
python -m pip install python-nmap scapy
python -m pip install python-whois tqdm prompt-toolkit pyperclip dnspython

:: Check for nmap
echo.
echo [*] Checking for Nmap...
where nmap >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Nmap not found in PATH
    echo [INFO] Download Nmap from: https://nmap.org/download.html
) else (
    echo [OK] Nmap found
)

:: Check for netcat
echo.
echo [*] Checking for Netcat...
where nc >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Netcat not found in PATH
    echo [INFO] Download Netcat from: https://nmap.org/ncat/
) else (
    echo [OK] Netcat found
)

:: Create directories
echo.
echo [*] Creating directory structure...
if not exist ".3amowl" mkdir .3amowl
if not exist ".3amowl\payloads" mkdir .3amowl\payloads
if not exist ".3amowl\workspaces" mkdir .3amowl\workspaces
if not exist ".3amowl\scans" mkdir .3amowl\scans
if not exist ".3amowl\sessions" mkdir .3amowl\sessions
if not exist ".3amowl\nikto_results" mkdir .3amowl\nikto_results
if not exist ".3amowl\whatsapp_session" mkdir .3amowl\whatsapp_session
if not exist ".3amowl\phishing_pages" mkdir .3amowl\phishing_pages
if not exist ".3amowl\shodan_results" mkdir .3amowl\shodan_results
if not exist ".3amowl\reports" mkdir .3amowl\reports
if not exist ".3amowl\traffic_logs" mkdir .3amowl\traffic_logs
if not exist ".3amowl\phishing_templates" mkdir .3amowl\phishing_templates
if not exist ".3amowl\phishing_logs" mkdir .3amowl\phishing_logs
if not exist ".3amowl\captured_credentials" mkdir .3amowl\captured_credentials
if not exist ".3amowl\ssh_keys" mkdir .3amowl\ssh_keys
if not exist ".3amowl\ssh_logs" mkdir .3amowl\ssh_logs
if not exist ".3amowl\time_history" mkdir .3amowl\time_history
if not exist ".3amowl\netcat_listeners" mkdir .3amowl\netcat_listeners
if not exist ".3amowl\temp" mkdir .3amowl\temp
echo [OK] Directories created

:: Create launcher script
echo.
echo [*] Creating launcher script...
(
echo @echo off
echo python "%%~dp03amowl.py" %%*
) > 3amowl.bat
echo [OK] Created 3amowl.bat

:: Run requirements check
echo.
echo [*] Running requirements check...
if exist "requirements-check.py" (
    python requirements-check.py
) else (
    echo [WARNING] requirements-check.py not found
)

:: Final message
echo.
echo ============================================================
echo    ✅ 3AMOWL installation complete!
echo.
echo    🚀 Run: python 3amowl.py
echo    📖 Or use: 3amowl.bat
echo ============================================================
echo.

pause