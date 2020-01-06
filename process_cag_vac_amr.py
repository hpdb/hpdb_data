#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from Bio import SeqIO
from subprocess import call
from ref_AMR import AMR
import os, glob, zipfile
import time, jinja2, yaml, regex, utils

def analyzecagA(pro):
  res = {}
  
  fuzzyA = utils.fuzzyFind(pro, 'EPIYA[QK]VNKKK[AT]GQ')
  if fuzzyA[0] >= 0.85:
    res['EPIYA-A'] = True
    res['EPIYA-A_seq'] = fuzzyA[1][0]
  else:
    res['EPIYA-A'] = False
  
  fuzzyB = utils.fuzzyFind(pro, 'EPIY[AT]QVAKKVNAKID')
  if fuzzyB[0] >= 0.85:
    res['EPIYA-B'] = True
    res['EPIYA-B_seq'] = fuzzyB[1][0]
  else:
    res['EPIYA-B'] = False
  
  fuzzyC = utils.fuzzyFind(pro, 'EPIYATIDDLGQPFPLK')
  if fuzzyC[0] >= 0.85:
    res['EPIYA-C'] = True
    res['EPIYA-C_seq'] = fuzzyC[1][0]
    fuzzyCC = utils.fuzzyFind(pro, 'EPIYATIDDLGQPFPLK', fuzzyC[1].start() + len('EPIYATIDDLGQPFPLK'))
    if fuzzyCC[0] >= 0.85:
      res['EPIYA-CC'] = True
      res['EPIYA-CC_seq'] = fuzzyCC[1][0]
    else:
      res['EPIYA-CC'] = False
  else:
    res['EPIYA-C'] = False
    res['EPIYA-CC'] = False
  
  fuzzyD = utils.fuzzyFind(pro, 'EPIYATIDFDEANQAG')
  if fuzzyD[0] >= 0.85:
    res['EPIYA-D'] = True
    res['EPIYA-D_seq'] = fuzzyD[1][0]
  else:
    res['EPIYA-D'] = False
  
  if res['EPIYA-A'] and res['EPIYA-B'] and res['EPIYA-C']:
    res['Origin'] = 'Western'
  elif res['EPIYA-A'] and res['EPIYA-B'] and res['EPIYA-D']:
    res['Origin'] = 'East Asian'
  
  return res

def analyzevacA(pro):
  res = {}
  
  # s1/s2
  start = utils.fuzzyFind(pro, 'MEIQQTHRKINRP')
  if start[0] < 0.75:
    res['s1s2'] = 'Khong xac dinh duoc s1/s2'
  else:
    end = utils.fuzzyFind(pro, 'AFFTTVII', start[1].start())
    if end[0] < 0.75:
      res['s1s2'] = 'Khong xac dinh duoc s1/s2'
    else:
      slen = end[1].start() - start[1].start() - len('MEIQQTHRKINRP')
      res['s1s2'] = 's1' if slen <= 25 else 's2'
      res['s1s2_seq1'] = start[1][0]
      res['s1s2_seq2'] = end[1][0]
  
  # m1/m2
  matched = regex.search('LGKAVNL(?:R){s<=1}VDAHT(A[YN]FNGNIYLG){s<=10}', pro)
  if not matched:
    res['m1m2'] = 'm1'
  else:
    percent = 1 - matched.fuzzy_counts[0] / len(matched[0])
    res['m1m2'] = 'm2' if percent >= 0.85 else 'Lai m1/m2'
    res['m1m2_seq'] = matched[0]
  
  return res

def analyze_cag_vac(genome_id):
  start_time = time.time()
  
  os.chdir(genome_id)
  utils.mkdir('CagVac')
  os.chdir('CagVac')
  
  result = {}
  result['jobtype'] = 'caga/vaca'
  result['daysubmit'] = time.strftime("%d-%m-%Y")
  result['found_caga'] = False
  result['found_vaca'] = False
  result['mutant_caga'] = False
  result['mutant_vaca'] = False
  result['caga_nu'] = {}
  result['caga_prot'] = {}
  result['vaca_nu'] = {}
  result['vaca_prot'] = {}
  result['caga_analysis'] = {'EPIYA-A': False, 'EPIYA-B': False, 'EPIYA-C': False, 'EPIYA-D': False}
  result['vaca_analysis'] = {'s1s2': '', 'm1m2': ''}
  
  # ----- Run tools -----
  utils.runprodigal('../genomic.fna', 'prot.fasta', 'nu.fasta')
  caga_ids = utils.runblast('blastp', os.environ['HPDB_BASE'] + '/genome/j99_caga.fasta', 'prot.fasta', '0.0001', '10 sseqid').splitlines()
  vaca_ids = utils.runblast('blastp', os.environ['HPDB_BASE'] + '/genome/j99_vaca.fasta', 'prot.fasta', '0.0001', '10 sseqid').splitlines()
  
  # ----- Find virulence factors -----
  prot_dict = SeqIO.index('prot.fasta', 'fasta')
  nu_dict = SeqIO.index('nu.fasta', 'fasta')
  
  for id in caga_ids:
    caga_prot = str(prot_dict[id].seq).rstrip('*')
    caga_pos = prot_dict[id].description.split('#')
    caga_nu = str(nu_dict[id].seq).strip('*')
    if 'EPIYA' in caga_prot or 'EPIYT' in caga_prot:
      if len(caga_prot) > 800: result['found_caga'] = True
      else: result['mutant_caga'] = True
      break
  
  for id in vaca_ids:
    vaca_prot = str(prot_dict[id].seq).rstrip('*')
    vaca_pos = prot_dict[id].description.split('#')
    vaca_nu = str(nu_dict[id].seq).strip('*')
    if utils.fuzzyFind(vaca_prot, 'MELQQTHRKINRPLVSLALVG')[0] >= 0.8:
      if len(vaca_prot) > 800: result['found_vaca'] = True
      else: result['mutant_vaca'] = True
      break
  
  prot_dict.close()
  nu_dict.close()
  
  # ----- Analyze data -----
  # cagA
  if result['found_caga']:
    result['caga_analysis'] = analyzecagA(caga_prot)
    result['caga_nu'] = {'name': 'cagA DNA', \
            'raw': caga_nu, \
            'len': len(caga_nu), \
            'start_pos': caga_pos[1].strip(), \
            'end_pos': caga_pos[2].strip()}    
    result['caga_prot'] = {'name': 'cagA Protein', \
            'raw': caga_prot, \
            'len': len(caga_prot), \
            'start_pos': caga_pos[1].strip(), \
            'end_pos': caga_pos[2].strip()}
    
  # vacA
  if result['found_vaca']:
    result['vaca_analysis'] = analyzevacA(vaca_prot)
    result['vaca_nu'] = {'name': 'vacA DNA', \
            'raw': vaca_nu, \
            'len': len(vaca_nu), \
            'start_pos': vaca_pos[1].strip(), \
            'end_pos': vaca_pos[2].strip()}    
    result['vaca_prot'] = {'name': 'vacA Protein', \
            'raw': vaca_prot, \
            'len': len(vaca_prot), \
            'start_pos': vaca_pos[1].strip(), \
            'end_pos': vaca_pos[2].strip()}
  
  result['exec_time'] = '%.2f' % (time.time() - start_time)
  with open('result.yaml', 'w') as f:
    yaml.dump(result, f)
  
  os.chdir('../..')

def checkMutant(inp):
  for x in inp:
    if x[0] != x[-1]:
      return True
  
  return False

def analyze_amr(genome_id):
  start_time = time.time()
  
  os.chdir(genome_id)
  utils.mkdir('AMR')
  os.chdir('AMR')
  
  result = {}
  result['jobtype'] = 'amr detection'
  result['daysubmit'] = time.strftime("%d-%m-%Y")
  result['amr_analysis'] = []
  
  # ----- Run tools -----
  utils.runsnippy(os.environ['HPDB_BASE'] + '/genome/26695.A23S.fasta',
                  '../genomic.fna',
                  'snippy_A23S')
  utils.runsnippy(os.environ['HPDB_BASE'] + '/genome/GCA_000008525.1_ASM852v1_genomic.gbff',
                  '../genomic.fna',
                  'snippy_whole_genome')
  utils.runprodigal('snippy_whole_genome/snps.consensus.subs.fa',
                    'snippy_whole_genome/snp_prot.fasta',
                    'snippy_whole_genome/snp_nu.fasta')
  
  # AMR
  genome = str(SeqIO.read('snippy_A23S/snps.consensus.subs.fa', 'fasta').seq)
  record = list(SeqIO.parse('snippy_whole_genome/snp_prot.fasta', 'fasta'))
  protein_seqs = [str(x.seq) for x in record]
  for x in AMR:
    if x['type'] == 'nu':
      part = genome[x['start'] : x['end']]
    elif x['type'] == 'prot':
      part = utils.fuzzyFindInList(protein_seqs, x['ref'])
    
    tmp = {}
    tmp['antibiotic'] = x['antibiotic']
    tmp['typing method'] = x['typing method']
    tmp['resistance gene'] = x['resistance gene']
    tmp['mutations'] = []
    
    for y in x['subs']:
      tmp['mutations'].append(y['orig'] + str(y['pos'] + 1) + part[y['pos']])
    
    tmp['mutations'] = ' '.join(tmp['mutations'])
    
    if checkMutant(tmp['mutations']):
      tmp['resistant phenotype'] = 'Resistant'
    else:
      tmp['resistant phenotype'] = 'Susceptible'
    
    result['amr_analysis'].append(tmp)
  
  result['exec_time'] = '%.2f' % (time.time() - start_time)
  with open('result.yaml', 'w') as f:
    yaml.dump(result, f)
  
  os.chdir('../..')

if __name__ == '__main__':
  dirs = [name for name in os.listdir('.') if os.path.isdir(name) and name != '.git']
  num = 0
  total = len(dirs)
  for name in dirs:
    num += 1
    print('[+] Processing {} ({}/{})'.format(name, num, total))
    analyze_cag_vac(name)