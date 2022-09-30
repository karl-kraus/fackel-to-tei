import os
from tqdm import tqdm
from acdh_tei_pyutils.tei import TeiReader


def yield_data(files):
    for x in tqdm(files, total=len(files)):
        head, tail = os.path.split(x)
        doc = TeiReader(x)

        for t in doc.any_xpath('.//DIV_START[@title]'):
            item = {
                'full_path': x
            }
            try:
                item['parid'] = t.attrib['parid']
            except KeyError:
                print(
                    [
                        tail, "missing parid in './/DIV_START[@title]'"
                    ]
                )
                continue
            try:
                item['id'] = t.attrib['titleID']
            except KeyError:
                print(
                    [
                        tail, "missing titleId in './/DIV_START[@title]'"
                    ]
                )
                continue
            try:
                item['author'] = t.attrib['author']
            except KeyError:
                item['author'] = '(not set)'
            try:
                item['text_title'] = t.attrib['title']
            except KeyError:
                item['text_title'] = '(not set)'
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
            yield(item)                

def yield_par_ids(merged_df, p_df):
    for i, row in tqdm(merged_df.iterrows(), total=len(merged_df)):
        start_ix = p_df.loc[p_df['parid'] == row['parid']].index[0]
        end_ix = p_df.loc[p_df['parid'] == row['next_parid']].index[0]-1
        item = {
            "parid": row['parid'],
            "parid_start_ix": start_ix,
            "parid_end_ix": end_ix,
        }
        yield item


def fix_page_nr(pn):
    try:
        page = int("".join([(s) for s in pn if s.isdigit()]).lstrip('0'))
    except ValueError:
        page = 0
    return page


def split_fackel_path(fackel_path):
    _, tail = os.path.split(fackel_path)
    _, f_jg, rest = tail.replace('.xml', '').split('-')
    try:
        f_nr, page = rest.split('_')
    except ValueError:
        f_nr, page = 'keine Nr', 'keine Seite'
    return (f_jg, f_nr, page)

def get_paragraphs(item, paragraphs):
    return paragraphs[item['parid_start_ix']:item['parid_end_ix']]