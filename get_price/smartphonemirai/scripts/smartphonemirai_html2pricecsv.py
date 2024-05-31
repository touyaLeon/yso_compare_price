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
    file = rf'{file}/get_price/smartphonemirai'
    for nm in tqdm(os.listdir(f'{file}/html_from_smartphonemirai'), desc='Reading Smartphone Mirai price'):
        s = read_file(f"{file}/html_from_smartphonemirai/{nm}")
        r1 = re.findall('''<div class="item-title">

                    

                    <div class="item-detail-icon">

                                        </div>

                    <p class="item-category-name">(.*?)</p>

                    (.*?)

                </div>''', s)
        if len(r1) == 0:
            r1 = re.findall('''<div class="item-title">

                    

                    <div class="item-detail-icon">

                                            <p class="item-detail-soldout">SOLD OUT</p>

                                        </div>

                    <p class="item-category-name">(.*?)</p>

                    (.*?)

                </div>''', s)
        r2 = re.findall('<p class="item-price">￥<span data-id="makeshop-item-price:1">(.*?)</span><span class="item-tax">（税込）</span></p>', s)[0]
        r3 = re.findall('''<dl>

                            <dt>独自商品コード</dt>

                            <dd>：(.*?)</dd>

                        </dl>''', s)[0]
        if len(r1) != 0 and len(r2) != 0 and len(r3) != 0:
            name = r1[0][1]
            price = r2
            id = r3
            dic[id] = (name, price)
    price_df = pd.DataFrame(dic).T
    if f'smartphonemirai_price.xlsx' in os.listdir(f'{file}/data/'):
        pre_price_df = pd.read_excel(f'{file}/data/smartphonemirai_price.xlsx', index_col=0)
        price_df['pre_price'] = pd.NA
        for id in pre_price_df.index:
            if id in price_df.index:
                price_df['pre_price'].loc[id] = pre_price_df[1].loc[id]
    price_df.to_excel(f'{file}/data/smartphonemirai_price.xlsx')
