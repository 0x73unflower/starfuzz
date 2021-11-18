import requests
import argparse
import platform
import subprocess
import datetime
from requests import status_codes
from requests import exceptions
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

class Main:
    def __init__(self):
        self.targetURL = ''
        self.targetSUB = ''
        self.wordlistFile = ''
        self.verboseMode = False
        self.saveOutput = False
        self.hostOS = ''
        self.words = []
        self.foundDirectories = []
        self.WARNING = f'{Style.BRIGHT}{Fore.RED}[{Fore.YELLOW}+{Fore.RED}]{Style.RESET_ALL}'
        self.SUCCESS = f'{Style.BRIGHT}{Fore.GREEN}[{Fore.CYAN}+{Fore.GREEN}]{Style.RESET_ALL}'
        self.UNKNOWN = f'{Style.BRIGHT}{Fore.MAGENTA}[{Fore.WHITE}~{Fore.MAGENTA}]{Style.RESET_ALL}'

    def parseArguments(self, *args):
        parser = argparse.ArgumentParser(add_help=True, description='starfuzz 1.0')
        parser.add_argument('-u', dest='directory', help='Specify URL (HTTP / HTTPS)')
        parser.add_argument('-d', dest='subdomain', help='Scan for Subdomains')
        parser.add_argument('-w', dest='wordlist', help='Specify a Wordlist' )
        parser.add_argument('-v', dest='verboseOn', help='Enable Verbose mode', action='store_true')
        parser.add_argument('-s', dest='saveResult', help='Saves output to a given file.', action='store_true')
        args = parser.parse_args()
        
        self.targetURL = args.directory
        self.targetSUB = args.subdomain
        self.wordlistFile = args.wordlist
        self.verboseMode = args.verboseOn
        self.saveOutput = args.saveResult

    def configTerminal(self):
        self.hostOS = platform.system()
        if self.hostOS == 'Windows':
            subprocess.call('cls', shell=True)
            init(autoreset=True)
        elif self.hostOS == 'Linux' or 'Darwin':
            subprocess.call('clear', shell=True)
        else:
            print(f'{self.WARNING} Unknown OS! Continuing...')
        print(LOGO)

    def openWordlist(self):
        try:
            with open(self.wordlistFile, 'r') as suppliedWordlist:
                for word in suppliedWordlist:
                    self.words.append(word.strip())
        except FileNotFoundError:
            print(f'{self.WARNING} \'{self.wordlistFile}\' could NOT be found!')
    
    def saveScan(self):
        with open('starfuzz.txt', 'a+') as outputFile:
            for directory in self.foundDirectories:
                outputFile.write(directory)
                outputFile.write('\n')
    
    def verboseScan(self):
        print(f'{self.UNKNOWN} Scanning: {self.cleanURL}')

    def scanDomain(self):
        try:
            for directory in self.words:
                self.cleanURL = self.targetURL + directory
                self.reqURL = requests.get(self.cleanURL)
                if self.reqURL.status_code == 200:
                    print(f'{self.SUCCESS} Found: {self.cleanURL}')
                else:
                    if self.reqURL.status_code != 200:
                        pass
                if self.verboseMode:
                    self.verboseScan()
        except InvalidURL:
                print(f'{self.WARNING} {self.targetURL} does NOT exist.')
    
    def scanSudomain(self):
        try:
            for directory in self.words:
                self.cleanURL = self.targetSUB[:8] + directory + '.' + self.targetSUB[8:]
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
        dScan = Main()
        dScan.configTerminal()
        dScan.parseArguments()
        dScan.openWordlist()
        if dScan.targetURL:
            dScan.scanDomain()
        if dScan.targetSUB:
            dScan.scanSudomain()
    except KeyboardInterrupt:
        print(f'Exiting!')
