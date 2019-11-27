import requests, html, os, csv
from htmldom import htmldom

headers = {'Cookie': '__utmc=61055151; __utmz=61055151.1574184736.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=61055151.1443795716.1574184736.1574184736.1574434365.2; WebSession=ccbf70236e38e90066d792843efb5b08; __utmt=1; __utmb=61055151.15.10.1574434365'}

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

def download(jobid, file):
    data = {'page': 'DownloadFile',
            'job': str(jobid),
            'file': file,
            'do_download': 'Download'}
    
    with requests.post('http://rast.nmpdr.org/rast.cgi', data = data, headers = headers, stream = True) as r:
        r.raise_for_status()
        with open(file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk:
                    f.write(chunk)

def process(jobid):
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
        download(jobid, file)
    os.chdir('../../')
    global cur
    print('[+] Done {}/{}'.format(cur, total))
    print('')
    print('')

if __name__ == "__main__":
    rawhtml = requests.get('http://rast.nmpdr.org/?page=Jobs', headers = headers).text
    dom = htmldom.HtmlDom()
    dom = dom.createDom(rawhtml)
    data = dom.find('#table_data_0').attr('value')
    rows = data.split('@~')
    global total, cur
    total = len(rows)
    cur = 0
    last = '799169'
    ok = False
    for r in rows:
        cur += 1
        cols = r.split('@^')
        if not ok:
            if cols[0] == last:
                ok = True
                process(cols[0])
        else:
            process(cols[0])