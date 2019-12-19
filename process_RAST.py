import os, glob, csv, zipfile

def parse_RAST(tsvfile):
  with open(tsvfile, 'r') as tsv:
    features = [line for line in csv.reader(tsv, dialect = 'excel-tab')][1:]
  
  peg    = list(filter(lambda f: f[2] == 'peg', features))
  repeat = list(filter(lambda f: f[2] == 'repeat', features))
  rna    = list(filter(lambda f: f[2] == 'rna', features))
  tRNA   = list(filter(lambda f: 'tRNA' in f[7], rna))
  rRNA   = list(filter(lambda f: 'rRNA' in f[7], rna))
  
  return peg, repeat, rna, tRNA, rRNA

if __name__ == '__main__':
  with open('strains_list.csv') as f:
    reader = csv.reader(f)
    with open('output.csv', 'w', newline = '') as g:
      writer = csv.writer(g)
      for row in reader:
        if row[0] == 'Name':
          new_row = row
        else:
          peg, repeat, rna, tRNA, rRNA = parse_RAST(glob.glob(row[1] + '/RAST/' + '*.txt')[0])
          new_row = row
          new_row[5] = len(peg)
          new_row[6] = len(repeat)
          new_row[7] = len(rna)
          new_row[8] = len(tRNA)
          new_row[9] = len(rRNA)
        writer.writerow(new_row)