import pandas as pd
import re
import os
from tqdm import tqdm


def read_file(filename):
    s = ''
    with open(filename, mode="r", encoding="utf-8") as f:
        lst = f.readlines()
        f.close
    s = ''.join(lst)
    return s


def main(file):
    dic = {}
    for nm in tqdm(os.listdir(fr'{file}/get_price/linxas/html_from_linxas'), desc='Reading Linxas price'):
        s = read_file(fr"{file}/get_price/linxas/html_from_linxas/{nm}")
        r1 = re.findall('<h2 class="__name">\n            (.*?)\n            \n        </h2>', s)
        r2 = re.findall('<span class="c-tax-sub-price __tax-sub-price __is-out-in">\\(税込(.*?)円\\)</span>', s)
        r3 = re.findall('''<dl class="__jan">
                    <dt>JANコード</dt>
                    <dd>(.*?)</dd>
                </dl>''', s)
        for name, price, id in zip(r1, r2, r3):
            dic[id] = (name, price)
    price_df = pd.DataFrame(dic).T
    if f'linxas_price.xlsx' in os.listdir(f'{file}/get_price/linxas/data'):
        pre_price_df = pd.read_excel(f'{file}/get_price/linxas/data/linxas_price.xlsx', index_col=0)
        price_df['pre_price'] = pd.NA
        for id in pre_price_df.index:
            if id in price_df.index:
                price_df['pre_price'].loc[id] = pre_price_df[1].loc[id]
    price_df.columns
    price_df.to_excel(f'{file}/get_price/linxas/data/linxas_price.xlsx')
