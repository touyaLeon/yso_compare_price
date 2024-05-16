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
    for nm in tqdm(os.listdir(fr'{file}\get_price\linxas\html_from_linxas'), desc='Reading Linxas price'):
        s = read_file(fr"{file}\get_price\linxas\html_from_linxas\{nm}")
        r1 = re.findall('<h2 class="__name">\n            (.*?)\n            \n        </h2>', s)
        r2 = re.findall('<span class="c-tax-sub-price __tax-sub-price __is-out-in">\\(税込(.*?)円\\)</span>', s)
        r3 = re.findall('''<dl class="__jan">
                    <dt>JANコード</dt>
                    <dd>(.*?)</dd>
                </dl>''', s)
        for name, price, id in zip(r1, r2, r3):
            dic[id] = (name, price)
    price_series = pd.DataFrame(dic).T
    price_series.columns
    price_series.to_excel(fr'{file}\get_price\linxas\data\linxas_price.xlsx')
