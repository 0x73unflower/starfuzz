import requests
import argparse
import platform
import subprocess
from requests.models import InvalidURL
from colorama import init, Fore, Style

LOGO = '''
███████╗████████╗ █████╗ ██████╗ ███████╗██╗   ██╗███████╗███████╗
██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║   ██║╚══███╔╝╚══███╔╝
███████╗   ██║   ███████║██████╔╝█████╗  ██║   ██║  ███╔╝   ███╔╝ 
╚════██║   ██║   ██╔══██║██╔══██╗██╔══╝  ██║   ██║ ███╔╝   ███╔╝  
███████║   ██║   ██║  ██║██║  ██║██║     ╚██████╔╝███████╗███████╗
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝╚══════╝
'''

class Options:
    def __init__(self):
        self.targetURL = False
        self.wordlistFile = ''
        self.verboseMode = False
        self.hostOS = ''
        self.foundDirectories = []
        self.WARNING = f'{Style.BRIGHT}{Fore.RED}[{Fore.YELLOW}+{Fore.RED}]{Style.RESET_ALL}'
        self.SUCCESS = f'{Style.BRIGHT}{Fore.GREEN}[{Fore.CYAN}+{Fore.GREEN}]{Style.RESET_ALL}'
        self.UNKNOWN = f'{Style.BRIGHT}{Fore.MAGENTA}[{Fore.WHITE}~{Fore.MAGENTA}]{Style.RESET_ALL}'

    def parseArguments(self, *args):
        parser = argparse.ArgumentParser(add_help=True, description='starfuzz 1.0')
        parser.add_argument('-u', dest='URL', help='Specify URL (HTTP / HTTPS)')
        parser.add_argument('-d', dest='subdomain', help='Scan for Subdomains')
        parser.add_argument('-w', dest='wordlist', help='Specify a Wordlist' )
        parser.add_argument('-v', dest='verboseOn', help='Enable Verbose mode', action='store_true')
        args = parser.parse_args()
        
        self.targetURL = args.URL
        self.targetSUB = args.subdomain
        self.wordlistFile = args.wordlist
        self.verboseMode = args.verboseOn

    def configTerminal(self):
        self.hostOS = platform.system()
        if self.hostOS == 'Windows':
            subprocess.call('cls', shell=True)
            init(autoreset=True)
        elif self.hostOS == 'Linux' or 'Darwin':
            subprocess.call('clear', shell=True)
        else:
            print(f'{self.WARNING} Unknown OS! Continuing...')

    def openWordlist(self):
        try:
            with open(self.wordlistFile, 'r') as suppliedWordlist:
                for word in suppliedWordlist:
                    if self.targetURL:
                        self.scanDomain(word.strip())
                    if self.targetSUB:
                        self.scanSubdomain(word.strip())
        except FileNotFoundError:
            print(f'{self.WARNING} \'{self.wordlistFile}\' could NOT be found!')
    
    def verboseScan(self):
        print(f'{self.UNKNOWN} Scanning: {self.cleanURL}')

class DirectoryScan(Options):
    def scanDomain(self, word):
        try:
            self.cleanURL = self.targetURL + word 
            self.reqURL = requests.get(self.cleanURL)
            if self.reqURL.status_code == 200:
                self.foundDirectories.append(self.cleanURL)
                print(f'{self.SUCCESS} Found: {self.cleanURL}')
            else:
                pass
            if self.verboseMode:
                self.verboseScan()
        except InvalidURL:
                print(f'{self.WARNING} {self.cleanURL} does NOT exist.')

    def scanSubdomain(self, word):
        try:
            self.cleanURL = self.targetSUB[:8] + word + '.' + self.targetSUB[8:]
            self.reqURL = requests.get(self.cleanURL)
            if self.reqURL.status_code == 200:
                print(f'{self.SUCCESS} Found: {self.cleanURL}')
                self.foundDirectories.append(self.cleanURL)
            else:
                pass
            if self.verboseMode:
                self.verboseScan()
        except InvalidURL:
            print(f'{self.WARNING} {self.cleanURL} does NOT exist.')
        except requests.ConnectionError:
            pass

if __name__ == '__main__':
    try:
        dScan = DirectoryScan()
        dScan.configTerminal()
        dScan.parseArguments()
        dScan.openWordlist()
        if dScan.targetURL:
            dScan.scanDomain()
        if dScan.targetSUB:
            dScan.scanSubdomain()
    except KeyboardInterrupt:
        print(f'Exiting!')
