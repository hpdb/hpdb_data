import os, zipfile

def zip(output):
    zipf = zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk('.'):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()

if __name__ == "__main__":
    dirs = [name for name in os.listdir('.') if os.path.isdir(name) and name != '.git']
    num = 0
    total = len(dirs)
    for name in dirs:
        num += 1
        print('[+] Zipping {} ({}/{})'.format(name, num, total))
        os.chdir(name + '/RAST')
        zip('../RAST.zip')
        os.chdir('../..')