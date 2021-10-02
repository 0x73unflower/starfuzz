import requests
import argparse
import platform
import subprocess
from requests import status_codes
from requests.models import InvalidURL

LOGO = '''
███████╗████████╗ █████╗ ██████╗ ███████╗██╗   ██╗███████╗███████╗
██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║   ██║╚══███╔╝╚══███╔╝
███████╗   ██║   ███████║██████╔╝█████╗  ██║   ██║  ███╔╝   ███╔╝ 
╚════██║   ██║   ██╔══██║██╔══██╗██╔══╝  ██║   ██║ ███╔╝   ███╔╝  
███████║   ██║   ██║  ██║██║  ██║██║     ╚██████╔╝███████╗███████╗
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝╚══════╝
'''

class StarFuzz:
    def __init__(self):
        self.targetURL = ''
        self.cleanURL = ''
        self.reqURL = ''
        self.suppliedWordlist = ''
        self.isVerbose = False
        self.word = ''
    
    def clearTerminal(self):
        initialOS = platform.system()
        if initialOS == 'Windows':
            subprocess.call('cls', shell=True)
        else:
            subprocess.call('clear', shell=True)
        print(LOGO)

    def parseArguments(self, *args):
        parser = argparse.ArgumentParser(add_help=True, description='starfuzz 1.0')
        parser.add_argument('-u', dest='url', help='Specify URL (HTTP / HTTPS)', required=True)
        parser.add_argument('-w', dest='wordlist', help='Specify a wordlist', required=True)
        parser.add_argument('-v', dest='verboseMode', help='Enable verbose mode', action='store_true', required=False)
        args = parser.parse_args()
        
        self.targetURL = args.url
        self.suppliedWordlist = args.wordlist
        self.isVerbose = args.verboseMode

    def openWordlist(self):
        try:
            with open(self.suppliedWordlist, 'r') as wordlistFile:
                for word in wordlistFile:
                    word = word.strip()
                    self.startScan(word)
        except FileNotFoundError:
            print(f'[!] {self.suppliedWordlist} could NOT be found!')
    
    def startScan(self, word):
        try:
            self.cleanURL = self.targetURL + word
            self.reqURL = requests.get(self.cleanURL)
            if self.reqURL.status_code == 200:
                print(f'[+] Found: {self.cleanURL}')
            else:
                if self.isVerbose:
                    print(f'[!] Scanning: {self.cleanURL}')
                if self.reqURL.status_code == 200:
                    print(f'[+] Found: {self.cleanURL}')
        except InvalidURL:
            print(f'[!] {self.targetURL} does NOT exist.')
        except requests.exceptions.ConnectionError as connError:
            print(f'[!] Connection Error! - {connError}')

if __name__ == '__main__':
    try:
        starfuzz = StarFuzz()
        starfuzz.clearTerminal()
        starfuzz.parseArguments()
        starfuzz.openWordlist()
        starfuzz.startScan()
    except KeyboardInterrupt:
        print('[!] Exiting!')
