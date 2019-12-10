import os, glob, csv, zipfile

def zip(output):
    zipf = zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk('.'):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()

def tsv2csv(input, output):
    with open(input, 'r') as fin:
        cr = csv.reader(fin, dialect = 'excel-tab')
        filecontents = [line for line in cr]
    
    # write comma-delimited file (comma is the default delimiter)
    with open(output, 'w', newline = '') as fou:
        cw = csv.writer(fou)
        cw.writerows(filecontents)

if __name__ == "__main__":
    dirs = [name for name in os.listdir('.') if os.path.isdir(name) and name != '.git']
    num = 0
    total = len(dirs)
    for name in dirs:
        os.chdir(name + '/RAST')
        num += 1
        genome_id = os.path.splitext(glob.glob("*.txt")[0])[0]
        print('[+] Converting {} - {} ({}/{})'.format(name, genome_id, num, total))
        tsv2csv(genome_id + '.txt', genome_id + '.csv')
        #zip('../RAST.zip')
        os.chdir('../..')