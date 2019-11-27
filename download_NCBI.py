import os, errno, gzip, shutil, csv, urllib.request

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def download(name, genomeid, refseq, genbank):
    print('Downloading {} - {}...'.format(name, genomeid))
    dir = str(genomeid)
    base = os.path.basename(refseq)
    mkdir_p(dir)
    os.chdir(dir)
    urllib.request.urlretrieve(refseq + '/' + base + '_genomic.fna.gz', 'genomic.fna.gz')
    with gzip.open('genomic.fna.gz', 'rb') as f_in:
        with open('genomic.fna', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.chdir('..')

if __name__ == "__main__":
    with open('complete genome.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != 'Name':
                download(row[0], row[1], row[2], row[3])