import requests
import argparse
import platform
import subprocess
import datetime
from requests import status_codes
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

# Colors
WARNING = f'{Style.BRIGHT}{Fore.RED}[{Fore.YELLOW}+{Fore.RED}]{Style.RESET_ALL}'
SUCCESS = f'{Style.BRIGHT}{Fore.GREEN}[{Fore.CYAN}+{Fore.GREEN}]{Style.RESET_ALL}'
UNKNOWN = f'{Style.BRIGHT}{Fore.MAGENTA}[{Fore.WHITE}~{Fore.MAGENTA}]{Style.RESET_ALL}'

class StarFuzz:
    def __init__(self):
        self.targetURL = ''
        self.cleanURL = ''
        self.reqURL = ''
        self.suppliedWordlist = ''
        self.saveOutput = False
        self.isVerbose = False
        self.word = ''
    
    def configTerminal(self):
        initialOS = platform.system()
        if initialOS == 'Windows':
            subprocess.call('cls', shell=True)
            # colorama for Windows
            init(autoreset=True)
        else:
            subprocess.call('clear', shell=True)
        print(LOGO)

    def parseArguments(self, *args):
        parser = argparse.ArgumentParser(add_help=True, description='starfuzz 1.0')
        parser.add_argument('-u', dest='url', help='Specify URL (HTTP / HTTPS)', required=True)
        parser.add_argument('-w', dest='wordlist', help='Specify a wordlist', required=True)
        parser.add_argument('-v', dest='verboseMode', help='Enable verbose mode', action='store_true', required=False)
        parser.add_argument('-s', dest='saveOutput', help='Saves output to a text file. ', action='store_true', required=False)
        args = parser.parse_args()
        
        self.targetURL = args.url
        self.suppliedWordlist = args.wordlist
        self.isVerbose = args.verboseMode
        self.saveOutput = args.saveOutput

    def openWordlist(self):
        try:
            with open(self.suppliedWordlist, 'r') as wordlistFile:
                for word in wordlistFile:
                    word = word.strip()
                    self.scanDomain(word)
        except FileNotFoundError:
            print(f'{WARNING} {self.suppliedWordlist} could NOT be found!')
    
    def scanDomain(self, word):
        foundDirectories = []
        try:
            self.cleanURL = self.targetURL + word
            self.reqURL = requests.get(self.cleanURL)
            if self.reqURL.status_code == 200:
                print(f'{SUCCESS} Found: {self.cleanURL}')
                foundDirectories.append(self.cleanURL)
            else:
                if self.isVerbose:
                    print(f'{UNKNOWN} Scanning: {self.cleanURL}')
                if self.reqURL.status_code == 200:
                    print(f'{SUCCESS} Found: {self.cleanURL}')
            if self.saveOutput:
                with open(f'starfuzz.txt', 'a+') as outputFile:
                    for directory in foundDirectories:
                        outputFile.write(directory)
                        outputFile.write('\n')
        except InvalidURL:
            print(f'{WARNING} {self.targetURL} does NOT exist.')
        except requests.exceptions.ConnectionError as connError:
            print(f'{WARNING} Connection Error! - {connError}')

if __name__ == '__main__':
    try:
        starfuzz = StarFuzz()
        starfuzz.configTerminal()
        starfuzz.parseArguments()
        starfuzz.openWordlist()
        starfuzz.scanDomain()
    except KeyboardInterrupt:
        print(f'{WARNING} [!] Exiting!')
