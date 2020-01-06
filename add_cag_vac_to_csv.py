import os, glob, csv, yaml

if __name__ == '__main__':
  with open('strains_list.csv') as f:
    reader = csv.reader(f)
    with open('output.csv', 'w', newline = '') as g:
      writer = csv.writer(g)
      for row in reader:
        if row[0] == 'Name':
          new_row = row + ['cagA', 'vacA']
        else:
          genome_id = row[1]
          with open(genome_id + '/CagVac/result.yaml') as f:
            result = yaml.full_load(f)
          
          EPIYA = ''
          if result['found_caga']:
            if result['caga_analysis']['EPIYA-A']: EPIYA += 'A'
            if result['caga_analysis']['EPIYA-B']: EPIYA += 'B'
            if result['caga_analysis']['EPIYA-C']: EPIYA += 'C'
            if result['caga_analysis']['EPIYA-CC']: EPIYA += 'C'
            if result['caga_analysis']['EPIYA-D']: EPIYA += 'D'
          
          new_row = row + [EPIYA, result['vaca_analysis']['s1s2'] + ' ' + result['vaca_analysis']['m1m2']]
        writer.writerow(new_row)