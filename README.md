```
███████╗████████╗ █████╗ ██████╗ ███████╗██╗   ██╗███████╗███████╗
██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║   ██║╚══███╔╝╚══███╔╝
███████╗   ██║   ███████║██████╔╝█████╗  ██║   ██║  ███╔╝   ███╔╝ 
╚════██║   ██║   ██╔══██║██╔══██╗██╔══╝  ██║   ██║ ███╔╝   ███╔╝  
███████║   ██║   ██║  ██║██║  ██║██║     ╚██████╔╝███████╗███████╗
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝╚══════╝ 
                    A project by, sunflower 🌻
                       For legal use only!
```
# Starfuzz
Starfuzz is a tool for website directory scanning. Some websites may have hidden directories and
starfuzz makes it easier to find them. It's lightweight and made with Python.

# Technologies
Starfuzz currently works with:
* Linux
* Windows

# Usage
```
  -h, --help    show this help message and exit
  -u DIRECTORY  Specify URL (HTTP / HTTPS)
  -d SUBDOMAIN  Scan for Subdomains
  -w WORDLIST   Specify a Wordlist
  -v            Enable Verbose mode
  -s            Saves output to a given file.
```
Scan Directories:
-----------------
```
$ starfuzz.py -u https://www.example.com/ -w common-directories.txt
```
Scan Subdomains:
----------------
```
$ starfuzz.py -d https://example.com/ -w common-subdomains.txt
```
# Installation
```
git clone https://github.com/sunflower-exe/starfuzz
```
