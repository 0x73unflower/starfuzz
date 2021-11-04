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
* Linux / Unix
* Windows

# Usage
```
  -u URL | Specify URL (HTTP / HTTPS)
  -d DOMAIN | Scan for subdomains
  -v VERBOSE | Verbose mode
  -w WORDLIST | Specify a wordlist
```
Example:

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
