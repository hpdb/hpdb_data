import csv
with open('data.csv') as f:
  reader = csv.reader(f)
  full = [row for row in reader]

with open('strains_list.csv') as f:
  reader = csv.reader(f)
  with open('output.csv', 'w', newline = '') as g:
    writer = csv.writer(g)
    for row in reader:
      new_row = row 
      if row[0] != 'Name':
        matched = [x for x in full if x[1] == row[1]]
        new_row[13] = matched[0][19]
      writer.writerow(new_row)