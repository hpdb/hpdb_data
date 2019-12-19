import requests, HTMLParser, os, csv
import urllib, yaml
from htmldom import htmldom

try:
  import urlparse
except ImportError:
  import urllib.parse as urlparse

def htmlunescape(str):
  return HTMLParser.HTMLParser().unescape(str)

class MyDumper(yaml.Dumper):
  def increase_indent(self, flow = False, indentless = False):
    return super(MyDumper, self).increase_indent(flow, False)

def parse_url():
  return dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))

def run_query(function, username, password, args):
  server = 'http://pubseed.theseed.org/rast/server.cgi'
  param = {'function': function,
           'username': username,
           'password': password,
           'args': yaml.dump(args, Dumper = MyDumper, default_flow_style = False)}
  return requests.post(server, data = param)

'''
status_of_RAST_job(username, password, *jobid);

where *jobid is a list of job ids.

The return value is a hash keyed by Jobid of
      {status} = Job Stage
      {error_msg} = message
      {verbose-status} = RAST Metadata
'''
def status_of_RAST_job(username, password, *jobids):
  return run_query('status_of_RAST_job', username, password, {'-job': jobids})

'''
retrieve_RAST_job(username, password, jobid, format)

where jobid is the RAST id of the job and

format is one of:
    genbank 		    (Genbank format)
    genbank_stripped 	(Genbank with EC numbers removed)
    embl 			    (EMBL format)
    embl_stripped 		(EMBL with EC numbers stripped)
    gff3 			    (GFF3 format)
    gff3_stripped 		(GFF3 with EC numbers stripped)
    gtf 			    (GTF format)
    gtf_stripped 		(GTF with EC numbers stripped)
    rast_tarball 		(gzipped tar file of the entire job)

The return is a hash of
    {status} = ok|error
    {file} = the downloaded file name
    {error_msg} = The error message
'''
def retrieve_RAST_job(username, password, *jobids):
  # WIP
  return

'''
kill_RAST_job(username, password, *jobids);

where *jobids is a list job ids to kill.

Return is a hash keyed by Job ID of
      {status} = ok|error
      {messages} = Messages
'''
def kill_RAST_job(username, password, *jobids):
  return run_query('kill_RAST_job', username, password, {'-job': jobids})

'''
delete_RAST_job(username, password, *jobids);

where *jobids is a list job ids to delete.

Return is a hash keyed by Job ID of
      {status} = ok|error
      {messages} = Messages
'''
def delete_RAST_job(username, password, *jobids):
  return run_query('delete_RAST_job', username, password, {'-job': jobids})

'''
get_job_metadata(username, password, jobid);

where jobid is the RAST id of a RAST job

Return is a hash of
      {status} = ok|error
      {error_message} = Error Message
      {key} => {metdata}
'''
def get_job_metadata(username, password, jobid):
  return run_query('get_job_metadata', username, password, {'-job': jobid})

'''
Below are web-simulated methods
'''

def get_cookies_RAST(username, password):
  data = {'page': 'Home',
          'login': username,
          'password': password,
          'action': 'perform_login'}
  return 'WebSession=' + requests.post('http://rast.nmpdr.org/rast.cgi', data = data).cookies['WebSession']

def logout_RAST(cookies):
  headers = {'Cookie': cookies}
  return requests.get('http://rast.nmpdr.org/rast.cgi?page=Jobs&logout=1', headers = headers)

def find_between(s, first, last):
  try:
    start = s.index(first) + len(first)
    end = s.index(last, start)
    return s[start:end]
  except ValueError:
    return ''

def submit_RAST_job(username, password, seqfile, strain):
  cookies = get_cookies_RAST(username, password)
  headers = {'Cookie': cookies}
  # Phase 1
  data = {'_submitted': '1',
          '_page': '1',
          'page': 'UploadGenome',
          '_submit': 'Use this data and go to step 2'}
  file = {'sequences_file': open(seqfile, 'rb')}
  rawhtml = requests.post('http://rast.nmpdr.org/rast.cgi', data = data, files = file, headers = headers).text
  
  # Phase 2
  dom = htmldom.HtmlDom()
  dom = dom.createDom(rawhtml)
  data = {'_submitted': '2',
          '_page': '2',
          'page': 'UploadGenome',
          'ajax_url': 'http://rast.nmpdr.org/ncbi.cgi',
          'sequences_file': '',
          'taxonomy_id': '210',
          'taxonomy_string': 'Bacteria; Proteobacteria; delta/epsilon subdivisions; Epsilonproteobacteria; Campylobacterales; Helicobacteraceae; Helicobacter',
          'domain': 'Bacteria',
          'genus': 'Helicobacter',
          'species': 'pylori',
          'strain': strain,
          'genetic_code': '11',
          '_submit': 'Use this data and go to step 3'}
  data['upload_dir'] = dom.find('#upload_dir').attr('value')
  data['upload_check'] = htmlunescape(dom.find('#upload_check').attr('value'))
  rawhtml = requests.post('http://rast.nmpdr.org/rast.cgi', data = data, headers = headers).text
  
  # Phase 3
  dom = htmldom.HtmlDom()
  dom = dom.createDom(rawhtml)
  data = {'_submitted': '3',
          '_page': '3',
          'page': 'UploadGenome',
          'ajax_url': 'http://rast.nmpdr.org/ncbi.cgi',
          'sequences_file': '',
          'taxonomy_id': '210',
          'taxonomy_string': 'Bacteria; Proteobacteria; delta/epsilon subdivisions; Epsilonproteobacteria; Campylobacterales; Helicobacteraceae; Helicobacter',
          'domain': 'Bacteria',
          'genus': 'Helicobacter',
          'species': 'pylori',
          'strain': strain,
          'genetic_code': '11',
          'stage_sort_order': 'call-features-rRNA-SEED,call-features-tRNA-trnascan,call-features-repeat-region-SEED,call-selenoproteins,call-pyrrolysoproteins,call-features-insertion-sequences,call-features-strep-suis-repeat,call-features-strep-pneumo-repeat,call-features-crispr,call-features-CDS-glimmer3,call-features-CDS-prodigal,call-features-CDS-genemark,call-features-ProtoCDS-kmer-v1,call-features-ProtoCDS-kmer-v2,annotate-proteins-kmer-v2,annotate-proteins-kmer-v1,annotate-proteins-phage,annotate-proteins-similarity,resolve-overlapping-features,classify_amr,annotate-special-proteins,annotate-families-figfam-v1,annotate-families_patric,find-close-neighbors,annotate-strain-type-MLST,call-features-prophage-phispy',
          'annotation_scheme': 'RASTtk',
          'gene_caller': 'rast',
          'figfam_version': 'Release70',
          'rasttk_customize_pipeline': '1',
          'call-features-rRNA-SEED': '1',
          'call-features-rRNA-SEED-condition': '',
          'call-features-tRNA-trnascan': '1',
          'call-features-tRNA-trnascan-condition': '',
          'call-features-repeat-region-SEED': '1',
          'call-features-repeat-region-SEED-min_identity': '95',
          'call-features-repeat-region-SEED-min_length': '100',
          'call-features-repeat-region-SEED-condition': '',
          'call-selenoproteins': '1',
          'call-selenoproteins-condition': '',
          'call-pyrrolysoproteins': '1',
          'call-pyrrolysoproteins-condition': '',
          'call-features-insertion-sequences-condition': '',
          'call-features-strep-suis-repeat': '1',
          'call-features-strep-suis-repeat-condition': '$genome->{scientific_name} =~ /^Streptococcus\s/',
          'call-features-strep-pneumo-repeat': '1',
          'call-features-strep-pneumo-repeat-condition': '$genome->{scientific_name} =~ /^Streptococcus\s/',
          'call-features-crispr': '1',
          'call-features-crispr-condition': '',
          'call-features-CDS-glimmer3': '1',
          'call-features-CDS-glimmer3-min_training_len': '2000',
          'call-features-CDS-glimmer3-condition': '',
          'call-features-CDS-prodigal': '1',
          'call-features-CDS-prodigal-condition': '',
          'call-features-CDS-genemark-condition': '',
          'call-features-ProtoCDS-kmer-v1-dataset_name': 'Release70',
          'call-features-ProtoCDS-kmer-v1-annotate_hypothetical_only': '1',
          'call-features-ProtoCDS-kmer-v1-condition': '',
          'call-features-ProtoCDS-kmer-v2-min_hits': '5',
          'call-features-ProtoCDS-kmer-v2-condition': '',
          'annotate-proteins-kmer-v2': '1',
          'annotate-proteins-kmer-v2-min_hits': '5',
          'annotate-proteins-kmer-v2-condition': '',
          'annotate-proteins-kmer-v1': '1',
          'annotate-proteins-kmer-v1-dataset_name': 'Release70',
          'annotate-proteins-kmer-v1-annotate_hypothetical_only': '1',
          'annotate-proteins-kmer-v1-condition': '',
          'annotate-proteins-phage': '1',
          'annotate-proteins-phage-annotate_hypothetical_only': '1',
          'annotate-proteins-phage-condition': '',
          'annotate-proteins-similarity': '1',
          'annotate-proteins-similarity-annotate_hypothetical_only': '1',
          'annotate-proteins-similarity-condition': '',
          'resolve-overlapping-features': '1',
          'resolve-overlapping-features-condition': '',
          'classify_amr': '1',
          'classify_amr-condition': '',
          'annotate-special-proteins': '1',
          'annotate-special-proteins-condition': '',
          'annotate-families-figfam-v1': '1',
          'annotate-families-figfam-v1-condition': '',
          'annotate-families_patric': '1',
          'annotate-families_patric-condition': '',
          'find-close-neighbors': '1',
          'find-close-neighbors-condition': '',
          'annotate-strain-type-MLST': '1',
          'annotate-strain-type-MLST-condition': '',
          'call-features-prophage-phispy': '1',
          'call-features-prophage-phispy-condition': '',
          'fix_errors': '1',
          'fix_frameshifts': '1',
          'build_models': '1',
          'backfill_gaps': '1',
          'verbose_level': '0',
          'disable_replication': '1',
          '_submit': 'Finish the upload'}
  data['upload_dir'] = dom.find('#upload_dir').attr('value')
  data['upload_check'] = htmlunescape(dom.find('#upload_check').attr('value'))
  res = requests.post('http://rast.nmpdr.org/rast.cgi', data = data, headers = headers).text
  logout_RAST(cookies)
  res = find_between(res, 'Your upload will be processed as job ', '.')
  return int(res)

def download_RAST_job(username, password, jobid, verbose = False):
  cookies = get_cookies_RAST(username, password)
  headers = {'Cookie': cookies}
  
  def download(jobid, file):
    data = {'page': 'DownloadFile',
            'job': str(jobid),
            'file': file,
            'do_download': 'Download'}
    
    with requests.post('http://rast.nmpdr.org/rast.cgi', data = data, headers = headers, stream = True) as r:
      r.raise_for_status()
      with open(file, 'wb') as f:
        for chunk in r.iter_content(chunk_size = 8192):
          if chunk:
            f.write(chunk)
  
  rawhtml = requests.get('http://rast.nmpdr.org/?page=JobDetails&job=' + str(jobid), headers = headers).text
  dom = htmldom.HtmlDom()
  dom = dom.createDom(rawhtml)
  element = dom.find('select')[0] # dirty hack to work on Python 2
  cnt = element.html().count('value')
  element = element.find('option')
  list_files = [element[x].attr('value') for x in range(cnt)]
  for file in list_files:
    if (verbose):
      print('Downloading ' + file)
    download(jobid, file)
  
  logout_RAST(cookies)

def parse_RAST(tsvfile):
  with open(tsvfile, 'r') as tsv:
    features = [line for line in csv.reader(tsv, dialect = 'excel-tab')][1:]
  
  peg    = list(filter(lambda f: f[2] == 'peg', features))
  repeat = list(filter(lambda f: f[2] == 'repeat', features))
  rna    = list(filter(lambda f: f[2] == 'rna', features))
  tRNA   = list(filter(lambda f: 'tRNA' in f[7], rna))
  rRNA   = list(filter(lambda f: 'rRNA' in f[7], rna))
  
  return peg, repeat, rna, tRNA, rRNA