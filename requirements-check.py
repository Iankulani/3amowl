#!/usr/bin/env python3
"""
3AMOWL Requirements Checker
Checks if all required dependencies and tools are installed
"""

import sys
import subprocess
import shutil
import importlib
import platform
from typing import Dict, List, Tuple

class RequirementsChecker:
    def __init__(self):
        self.python_version = sys.version_info
        self.os_type = platform.system().lower()
        self.results = {
            'python': {'passed': False, 'message': ''},
            'pip': {'passed': False, 'message': ''},
            'packages': {},
            'system_tools': {},
            'optional': {}
        }
    
    def check_python(self) -> bool:
        """Check Python version"""
        if self.python_version.major >= 3 and self.python_version.minor >= 7:
            self.results['python']['passed'] = True
            self.results['python']['message'] = f"Python {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}"
        else:
            self.results['python']['message'] = f"Python 3.7+ required (found {self.python_version.major}.{self.python_version.minor})"
        return self.results['python']['passed']
    
    def check_pip(self) -> bool:
        """Check if pip is available"""
        pip_path = shutil.which('pip') or shutil.which('pip3')
        if pip_path:
            self.results['pip']['passed'] = True
            self.results['pip']['message'] = f"pip found at {pip_path}"
            return True
        self.results['pip']['message'] = "pip not found in PATH"
        return False
    
    def check_package(self, package_name: str, import_name: str = None) -> bool:
        """Check if a Python package is installed"""
        import_name = import_name or package_name.replace('-', '_')
        try:
            module = importlib.import_module(import_name)
            version = getattr(module, '__version__', 'unknown')
            self.results['packages'][package_name] = {'passed': True, 'version': version}
            return True
        except ImportError:
            self.results['packages'][package_name] = {'passed': False, 'error': 'not installed'}
            return False
    
    def check_system_tool(self, tool_name: str, check_cmd: List[str] = None) -> bool:
        """Check if a system tool is installed"""
        tool_path = shutil.which(tool_name)
        if tool_path:
            version = "unknown"
            if check_cmd:
                try:
                    result = subprocess.run(check_cmd, capture_output=True, text=True, timeout=5)
                    version = result.stdout.strip().split('\n')[0][:50]
                except:
                    pass
            self.results['system_tools'][tool_name] = {'passed': True, 'path': tool_path, 'version': version}
            return True
        self.results['system_tools'][tool_name] = {'passed': False, 'error': 'not found'}
        return False
    
    def check_optional(self, name: str, check_func) -> bool:
        """Check optional dependency"""
        try:
            result = check_func()
            self.results['optional'][name] = {'passed': result}
            return result
        except Exception as e:
            self.results['optional'][name] = {'passed': False, 'error': str(e)}
            return False
    
    def run_all_checks(self):
        """Run all requirement checks"""
        print("=" * 60)
        print("🦉 3AMOWL Requirements Checker")
        print("=" * 60)
        
        # Python check
        print("\n📌 Python Environment:")
        self.check_python()
        status = "✅" if self.results['python']['passed'] else "❌"
        print(f"  {status} {self.results['python']['message']}")
        
        # Pip check
        self.check_pip()
        status = "✅" if self.results['pip']['passed'] else "❌"
        print(f"  {status} {self.results['pip']['message']}")
        
        # Core packages
        print("\n📦 Python Packages:")
        core_packages = [
            ('requests', 'requests'),
            ('psutil', 'psutil'),
            ('colorama', 'colorama'),
            ('cryptography', 'cryptography'),
        ]
        
        for pkg, imp in core_packages:
            self.check_package(pkg, imp)
            status = "✅" if self.results['packages'][pkg]['passed'] else "❌"
            version = self.results['packages'][pkg].get('version', '')
            print(f"  {status} {pkg:<20} {version}")
        
        # Optional packages
        print("\n📦 Optional Python Packages:")
        optional_packages = [
            ('shodan', 'shodan'),
            ('paramiko', 'paramiko'),
            ('discord.py', 'discord'),
            ('telethon', 'telethon'),
            ('selenium', 'selenium'),
            ('slack-sdk', 'slack_sdk'),
            ('qrcode', 'qrcode'),
            ('scapy', 'scapy'),
            ('python-whois', 'whois'),
        ]
        
        for pkg, imp in optional_packages:
            self.check_package(pkg, imp)
            status = "✅" if self.results['packages'][pkg]['passed'] else "⚠️"
            version = self.results['packages'][pkg].get('version', '')
            print(f"  {status} {pkg:<20} {version}")
        
        # System tools
        print("\n🔧 System Tools:")
        tools = [
            ('ping', ['ping', '-c', '1', '127.0.0.1']),
            ('nmap', ['nmap', '--version']),
            ('nc', ['nc', '-h']),
            ('ssh', ['ssh', '-V']),
            ('curl', ['curl', '--version']),
            ('dig', ['dig', '-v']),
            ('traceroute', ['traceroute', '--version']),
        ]
        
        for tool, check_cmd in tools:
            self.check_system_tool(tool, check_cmd)
            status = "✅" if self.results['system_tools'][tool]['passed'] else "❌"
            version = self.results['system_tools'][tool].get('version', '')
            print(f"  {status} {tool:<15} {version[:40]}")
        
        # Optional capabilities
        print("\n🎯 Optional Capabilities:")
        
        def check_root():
            if self.os_type == 'linux':
                return os.geteuid() == 0
            return False
        
        self.check_optional('Root/Admin Access', check_root)
        status = "✅" if self.results['optional']['Root/Admin Access']['passed'] else "⚠️"
        print(f"  {status} Root/Admin Access - Required for raw packets and firewall")
        
        def check_signal_cli():
            return shutil.which('signal-cli') is not None
        
        self.check_optional('signal-cli', check_signal_cli)
        status = "✅" if self.results['optional']['signal-cli']['passed'] else "⚠️"
        print(f"  {status} signal-cli - For Signal integration")
        
        def check_chromedriver():
            return shutil.which('chromedriver') is not None
        
        self.check_optional('ChromeDriver', check_chromedriver)
        status = "✅" if self.results['optional']['ChromeDriver']['passed'] else "⚠️"
        print(f"  {status} ChromeDriver - For WhatsApp automation")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Summary")
        print("=" * 60)
        
        passed_packages = sum(1 for v in self.results['packages'].values() if v['passed'])
        total_packages = len(self.results['packages'])
        passed_tools = sum(1 for v in self.results['system_tools'].values() if v['passed'])
        total_tools = len(self.results['system_tools'])
        
        print(f"  Python Packages: {passed_packages}/{total_packages} installed")
        print(f"  System Tools:    {passed_tools}/{total_tools} available")
        
        if self.results['python']['passed'] and self.results['pip']['passed']:
            print("\n✅ Base requirements satisfied!")
        else:
            print("\n❌ Base requirements not satisfied. Please fix issues above.")
        
        if passed_packages < len(core_packages):
            print(f"\n💡 Run: pip install -r requirements.txt")
        
        return self.results['python']['passed'] and self.results['pip']['passed']

def main():
    import os
    
    checker = RequirementsChecker()
    success = checker.run_all_checks()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 3AMOWL is ready to run!")
        print("   Run: python3 3amowl.py")
    else:
        print("❌ Please resolve the issues above before running 3AMOWL")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()