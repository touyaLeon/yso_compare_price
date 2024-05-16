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
    for nm in tqdm(os.listdir(rf'{file}/get_price/smartphonemirai/html_from_smartphonemirai'), desc='Reading Smartphone Mirai price'):
        s = read_file(rf"{file}/get_price/smartphonemirai/html_from_smartphonemirai/{nm}")
        r1 = re.findall('<p class="item-name"><a href="/view/item/(.*)">(.*?)</a></p>', s)
        r2 = re.findall('<p class="price">￥(.*?)<span>（税込）</span></p>', s)
        for i, price in zip(r1, r2):
            name = i[1]
            dic[name] = price
    price_series = pd.Series(dic)
    price_series.to_excel(rf'{file}/get_price/smartphonemirai/data/smartphonemirai_price.xlsx')
