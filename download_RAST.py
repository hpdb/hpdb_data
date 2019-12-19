import RAST_sdk as rast
import requests, html, os, csv
from htmldom import htmldom

def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else:
      raise

def find_between(s, first, last):
  try:
    if first != '':
      start = s.index(first) + len(first)
    else:
      start = 0
    if last != '':
      end = s.index(last, start)
    else:
      end = len(s)
    return s[start:end]
  except ValueError:
    return ""

def download(jobid, file, headers):
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

def get_cookies_RAST(username, password):
  data = {'page': 'Home',
          'login': username,
          'password': password,
          'action': 'perform_login'}
  return 'WebSession=' + requests.post('http://rast.nmpdr.org/rast.cgi', data = data).cookies['WebSession']

def process(jobid, headers):
  rawhtml = requests.get('http://rast.nmpdr.org/?page=JobDetails&job=' + str(jobid), headers = headers).text
  dom = htmldom.HtmlDom()
  dom = dom.createDom(rawhtml)
  jobtable = dom.find('table')[1]
  genomeid_name = jobtable.find('td')[0].text()
  genomeid = find_between(genomeid_name, '', ' -')
  name = find_between(genomeid_name, '- ', '')
  ncbiid = find_between(name, '[', ']')
  list_files = [x.attr('value') for x in dom.find('select')[0].find('option')]
  print('[+] Processing ' + genomeid_name)
  print('[-] NCBI ID: ' + ncbiid)
  os.chdir(ncbiid)
  mkdir_p('RAST')
  os.chdir('RAST')
  for file in list_files:
    print('[-] Downloading ' + file)
    download(jobid, file, headers)
  os.chdir('../../')
  global cur
  print('[+] Done {}/{}'.format(cur, total))
  print('')
  print('')

if __name__ == "__main__":
  username = ''
  password = ''
  cookies = get_cookies_RAST(username, password)
  headers = {'Cookie': cookies}
  
  rawhtml = requests.get('http://rast.nmpdr.org/?page=Jobs', headers = headers).text
  dom = htmldom.HtmlDom()
  dom = dom.createDom(rawhtml)
  data = dom.find('#table_data_0').attr('value')
  rows = data.split('@~')
  
  global total, cur
  total = len(rows)
  cur = 0
  for r in rows:
    cur += 1
    cols = r.split('@^')
    process(cols[0], headers)