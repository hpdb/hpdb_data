import requests, html, os, csv
from htmldom import htmldom

def phase1():
    data = {'_submitted': '1',
            '_page': '1',
            'page': 'UploadGenome',
            '_submit': 'Use this data and go to step 2'}
    file = {'sequences_file': open('genomic.fna','rb')}
    headers = {'Cookie': '__utmc=61055151; __utmz=61055151.1574184736.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=61055151.1443795716.1574184736.1574184736.1574434365.2; WebSession=ccbf70236e38e90066d792843efb5b08; __utmt=1; __utmb=61055151.15.10.1574434365'}
    res = requests.post('http://rast.nmpdr.org/rast.cgi', data = data, files = file, headers = headers).text
    return res

def phase2(rawhtml, strain):
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
    data['upload_check'] = html.unescape(dom.find('#upload_check').attr('value'))
    headers = {'Cookie': '__utmc=61055151; __utmz=61055151.1574184736.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=61055151.1443795716.1574184736.1574184736.1574434365.2; WebSession=ccbf70236e38e90066d792843efb5b08; __utmt=1; __utmb=61055151.15.10.1574434365'}
    res = requests.post('http://rast.nmpdr.org/rast.cgi', data = data, headers = headers).text
    return res

def phase3(rawhtml, strain):
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
    data['upload_check'] = html.unescape(dom.find('#upload_check').attr('value'))
    headers = {'Cookie': '__utmc=61055151; __utmz=61055151.1574184736.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=61055151.1443795716.1574184736.1574184736.1574434365.2; WebSession=ccbf70236e38e90066d792843efb5b08; __utmt=1; __utmb=61055151.15.10.1574434365'}
    res = requests.post('http://rast.nmpdr.org/rast.cgi', data = data, headers = headers).text
    return res
    
if __name__ == "__main__":
    with open('complete genome.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != 'Name':
                strain = row[0][20:] + ' [' + row[1] + ']'
                print('Uploading ' + strain + '...')
                os.chdir(row[1])
                rawhtml = phase1()
                rawhtml = phase2(rawhtml, strain)
                rawhtml = phase3(rawhtml, strain)
                os.chdir('..')