import requests
import argparse
import platform
import subprocess
from requests.models import InvalidURL, Response

if platform.system() == 'Windows':
    subprocess.call('cls', shell=True)
else:
    subprocess.call('clear', shell=True)

print('''
███████╗████████╗ █████╗ ██████╗ ███████╗██╗   ██╗███████╗███████╗
██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║   ██║╚══███╔╝╚══███╔╝
███████╗   ██║   ███████║██████╔╝█████╗  ██║   ██║  ███╔╝   ███╔╝ 
╚════██║   ██║   ██╔══██║██╔══██╗██╔══╝  ██║   ██║ ███╔╝   ███╔╝  
███████║   ██║   ██║  ██║██║  ██║██║     ╚██████╔╝███████╗███████╗
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝╚══════╝                                                            
''')

parser = argparse.ArgumentParser(add_help=True, description='dirscan 0.1')
parser.add_argument('-u', '--url', dest='url', help='Specify URL (HTTP / HTTPS)', required=True)
parser.add_argument('-w', '--wordlist', dest='wordlist', help='Specify a wordlist', required=True)
args = parser.parse_args()

url = args.url
wordlist = args.wordlist

def main():
    try:
        with open(wordlist,'r') as file:
            for word in (file):
                domain = url + word.lower().strip()
                r = requests.get(domain)
                if (r.status_code == 200):
                    print('[+] Found: ' + domain)
                else:
                    pass            
    except InvalidURL:
        print('[!] Invalid URL')
    except requests.exceptions.ConnectionError:
        print('[!] Connection Error!')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n[!] Exiting...')
