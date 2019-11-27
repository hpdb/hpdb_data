import requests, html, os, csv
from htmldom import htmldom

if __name__ == "__main__":
    dirs = [name for name in os.listdir('.') if os.path.isdir(name)]
    num = 0
    total = len(dirs)
    for name in dirs:
        num += 1
        print('[+] Checking {} ({}/{})'.format(name, num, total))
        files = os.listdir(name + '/' + 'RAST')
        files_len = len(files)
        print('[+] Found {} files'.format(files_len))
        if files_len == 17:
            print('[+] OK')
        else:
            print('[+] ERROR!!')
        print('')