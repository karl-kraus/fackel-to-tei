import csv
import glob
import jinja2
import lxml.etree as ET

import os
import shutil

from acdh_tei_pyutils.tei import TeiReader
from tqdm import tqdm

from utils import split_fackel_path

templateLoader = jinja2.FileSystemLoader(searchpath=".")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template('./templates/text.xml')

OUT_DIR = 'data/fackel_out'
TEI_DIR = 'data/editions'

files = sorted(glob.glob('./data_orig/*/*.xml'))
try:
    shutil.rmdir('./data')
except:
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(TEI_DIR, exist_ok=True)

transform = ET.XSLT(ET.parse('totei.xsl'))

div_start = False
title_id = None
container = []
item = {}
errors = []
csv_file = 'texts.csv'
csv_cols = [
    'text_title',
    'start_file',
    'f_jg',
    'f_nr',
    'start_page_value',
    'start_page',
    'year',
    'month',
    'day',
    'end_file',
    'end_page',
    'date',
    'node_count',
    'title_id',
    'par_id'
]
first_row = True
with open(csv_file, 'w') as csvfile:
    writer = csv.writer(csvfile)
    for x in tqdm(files, total=len(files)):
        _, tail = os.path.split(x)
        doc = TeiReader(x)
        tree = doc.tree
        for elem in tree.iter():
            if elem.tag == 'DIV_START' and elem.attrib.get('titleID'):
                item["text_title"] = elem.attrib.get('title', 'kein Titel vorhanden')
                item["start_file"] = tail
                item['f_jg'], item['f_nr'], item['start_page_value'] = split_fackel_path(x)
                try:
                    item["start_page"] = doc.any_xpath('.//PN/text()')[0]
                except IndexError:
                    item["start_page"] = 'XXXXXXXXXXXXXXXXXXX'
                    errors.append(f"missing PN in {tail}")
                
                try:
                    item['year'] = doc.any_xpath('.//PUBL_YEAR/@a')[0]
                except IndexError:
                    item['year'] = '1234'
                try:
                    month = doc.any_xpath('.//PUBL_MONTH/@a')[0]
                except IndexError:
                    month = '1'
                try:
                    item['month'] = f"{int(month):02}"
                except ValueError:
                    item['month'] = "01"
                try:
                    item['day'] = doc.any_xpath('.//PUBL_DAY/@a')[0]
                except IndexError:
                    item['day'] = '01'
                item['date'] = f"{item['year']}-{item['month']}-{item['day']}"
                title_id = f"text__{elem.attrib.get('titleID')}.xml"
                par_id = elem.attrib.get('parid')
                div_start = True
            if elem.tag == 'DIV_END' and title_id:
                item["end_file"] = tail
                try:
                    item["end_page"] = doc.any_xpath('.//PN/text()')[0]
                except IndexError:
                    item["end_page"] = 'XXXXXXXXXXXXXXXXXXX'
                    errors.append(f"missing PN in {tail}")
                container.append(elem)
                item["node_count"] = len(container)
                item['title_id'] = title_id
                item["parid"] = par_id
                if first_row:
                    writer.writerow([y for y in item.keys()])
                    first_row = False
                writer.writerow([y for y in item.values()])
                item['content'] = [ET.tostring(node).decode('utf-8') for node in container]
                with open(f"{os.path.join('data', 'fackel_out', title_id)}", 'w') as f:
                    f.write(template.render(**item))                
                container = []
                item = {}
                div_start = False
                title_id = None
            if div_start:
                container.append(elem)

print(f"converting text files from {OUT_DIR} into TEIs in {TEI_DIR}")
xmls = sorted(glob.glob(f"{OUT_DIR}/*.xml"))

failed = []
for x in tqdm(xmls, total=len(xmls)):
    new_file_name = x.replace('fackel_out', 'editions')
    try:
        doc = ET.parse(x)
    except Exception as e:
        failed.append([x, e])
    result = transform(doc)
    with open(f'{new_file_name}', 'w') as f:
        f.write(str(result))
