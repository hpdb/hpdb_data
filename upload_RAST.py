import RAST_sdk as rast
import requests, html, os, csv
from htmldom import htmldom
    
if __name__ == "__main__":
    username = ''
    password = ''
    with open('complete genome.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != 'Name':
                strain = row[0][20:] + ' [' + row[1] + ']'
                print('Uploading ' + strain + '...')
                os.chdir(row[1])
                rast.submit_RAST_job(username, password, 'genomic.fna', strain)
                os.chdir('..')