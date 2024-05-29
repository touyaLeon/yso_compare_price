from pdb import line_prefix
import pandas as pd
from datetime import datetime
import os
import numpy as np
from tqdm import tqdm


def screen_categs(categoryDF):
    categs = sorted(set(categoryDF['categ_id']))
    categ_id_dic = {}
    for categ in categs:
        categ_id_dic[categ] = list(categoryDF.loc[categoryDF['categ_id'] == categ].index)
    categ_s = ''
    for i, categ in enumerate(categs):
        categ_s = categ_s + str(i) + '. ' + categ + '\n'
    b = input(f'''
请输入类别（空格隔开）：
{categ_s}
''')
    c = len(categs)
    while True:
        if b == 'e':
            return
        b_lst = b.split(' ')
        if not ''.join(b_lst).isnumeric():
            b = input(f'请再次输入类别（整数{0}-{c}，空格隔开）\n')
            continue
        else:
            if sum(pd.Series(map(lambda x: int(x), b_lst)) > c) > 0:
                b = input(f'请再次输入类别（整数{0}-{c}，空格隔开）\n')
                continue
            break
    return b_lst, categs, categ_id_dic


def set_price(file):
    categoryDF = pd.read_excel(f'{file}/set_price_test/data/category.xlsx', index_col='product_variant_ids/id')
    if 'yso_price.xlsx' in os.listdir(f'{file}/compare_price/data'):
        yso_price_df = pd.read_excel(f'{file}/compare_price/data/yso_price.xlsx', index_col='受注明細/製品/ID')
    else:
        print('无法找到yso_price.xlsx文件')
        return
    b_lst, categs, categ_id_dic = screen_categs(categoryDF)
    df_categ_lst = []
    solid_profit_lst = []
    profit_ratio_lst = []
    profit_lines_list = []
    for i in b_lst:
        categ = categs[int(i)]
        df_categ_lst.append(categ)
        print(f'''
产品类别{i}: {categ}
''')
        solid_profit = input(f'请设置产品类别{categ}的固定利润\n')
        if solid_profit == 'e':
            return
        while not solid_profit.isnumeric():
            solid_profit = input(f'输入有误，请再次设置产品类别{categ}的固定利润（正整数）\n')
        solid_profit_lst.append(int(solid_profit))
        profit_ratio = input(f'请设置产品类别{categ}的利润比率\n')
        while sum(pd.Series(map(lambda x: x.isnumeric() if len(x) > 0 else False, profit_ratio.split('.')))) != 2:
            if profit_ratio == 'e':
                return
            profit_ratio = input(f'输入有误，请设置输入产品类别{categ}的利润比率（正小数）\n')
        profit_ratio_lst.append(float(profit_ratio))
        profit_lines = input(f'请设置产品类别{categ}的利润上下限\n')
        while sum(pd.Series(map(lambda x: x.isnumeric(), profit_lines.split(' ')))) != 2:
            if profit_lines == 'e':
                return
            profit_lines = input(f'输入有误，请再次设置产品类别{categ}的利润上下限（正整数，空格隔开）\n')
        profit_lines_ = profit_lines.split(' ')
        d, u = int(profit_lines_[0]), int(profit_lines_[1])
        if d > u:
            d, u = u, d
        profit_lines_list.append([d, u])
    df_index_lst = []
    for categ in df_categ_lst:
        for id in categ_id_dic[categ]:
            df_index_lst.append(id)
    df = pd.DataFrame(index=df_index_lst, columns=['name', 'barcode', 'categ', 'solid_profit', 'profit_ratio', 'profit_downline', 'profit_upperline', 'standard_price', 'setted_price', 'faxed_price', 'yso_price'])
    for categ, solid_profit, profit_ratio, profit_lines in zip(df_categ_lst, solid_profit_lst, profit_ratio_lst, profit_lines_list):
        for id in categ_id_dic[categ]:
            df.index.name = 'id'
            df['name'].loc[id] = categoryDF['product_variant_ids/name'].loc[id]
            df['barcode'].loc[id] = categoryDF['barcode'].loc[id]
            df['categ'].loc[id] = categoryDF['categ_id'].loc[id]
            df['solid_profit'].loc[id] = solid_profit
            df['profit_ratio'].loc[id] = profit_ratio
            df['profit_downline'].loc[id] = profit_lines[0]
            df['profit_upperline'].loc[id] = profit_lines[1]
            standard_price = categoryDF['standard_price'].loc[id]
            df['standard_price'].loc[id] = standard_price
            profit = max(min(standard_price * profit_ratio, profit_lines[1]), profit_lines[0])
            setted_price = int(standard_price + profit + solid_profit)
            df['setted_price'].loc[id] = setted_price
            df['faxed_price'].loc[id] = int(setted_price * 1.1)
            df['yso_price'].loc[id] = yso_price_df['受注明細/税込価格'].loc[id]
    df_categ_s = ','.join(df_categ_lst)
    ntm = datetime.now()
    tm = str(datetime.date(ntm)) + '-' + str(ntm.hour) + '-' + str(ntm.minute)
    fname = f'{tm} setted_price({df_categ_s}).xlsx'
    df.to_excel(f"{file}/compare_price/data/{fname}")
    print(f'新设置的价格表{fname}已保存至{file}/compare_price/data')


def find_best_limitation(file):
    linxas_df = pd.read_excel(f'{file}/get_price/linxas/data/linxas_price.xlsx', index_col=0)
    spmr_df = pd.read_excel(f'{file}/get_price/smartphonemirai/data/smartphonemirai_price.xlsx', index_col=0)
    id_df = pd.read_excel(f'{file}/compare_price/data/all_id.xlsx', index_col=0)
    categoryDF = pd.read_excel(f'{file}/set_price_test/data/category.xlsx', index_col='product_variant_ids/id')
    if 'yso_price.xlsx' in os.listdir(f'{file}/compare_price/data'):
        yso_price_df = pd.read_excel(f'{file}/compare_price/data/yso_price.xlsx', index_col='受注明細/製品/ID')
    else:
        print('无法找到yso_price.xlsx文件')
        return
    b_lst, categs, categ_id_dic = screen_categs(categoryDF)
    df_categ_lst = []
    price_lst = []
    for b in b_lst:
        categ = categs[int(b)]
        df_categ_lst.append(categ)
        for id in categ_id_dic[categ]:
            if id not in id_df.index:
                print(f'error: {id}')
                continue
            linxas_id = id_df['linxas_id'].loc[id]
            spmr_id = id_df['smartphonemirai_id'].loc[id]
            if pd.isna(linxas_id):
                linxas_price = pd.NA
            elif linxas_id not in linxas_df.index:
                linxas_price = pd.NA
            else:
                linxas_price = linxas_df[1].loc[linxas_id]
            if pd.isna(spmr_id):
                spmr_price = pd.NA
            elif spmr_id in spmr_df.index:
                spmr_price = spmr_df[1].loc[spmr_id]
            else:
                spmr_price = pd.NA
            standard_price = categoryDF['standard_price'].loc[id]
            if not pd.isna(standard_price):
                price_lst.append([int(standard_price), spmr_price, linxas_price])
    dt_lst = []
    for lst in price_lst:
        x, y1, y2 = lst[0], lst[1], lst[2]
        if pd.isna(y1) and pd.isna(y2):
            y = pd.NA
        elif pd.isna(y1):
            y = y2
        elif pd.isna(y2):
            y = y1
        else:
            y = min(y1, y2)
        if pd.isna(y) or pd.isna(x):
            continue
        else:
            y = float(''.join(y.split(',')))
            dt_lst.append([x, y])
    dt = np.array(dt_lst)
    x = dt[:, 0]
    y = dt[:, 1]
    lst = []
    m = len(x)
    mx = 0
    lst_i = list(np.array(range(100, 200)) / 100) + list(np.array(range(200, 300)) / 200)
    lst_j = []
    c = 5
    while c < 100000:
        if c < 1000:
            lst_j.append(c)
            c += 5
        elif c < 10000:
            lst_j.append(c)
            c += 50
        else:
            lst_j.append(c)
            c += 500
    for i in tqdm(lst_i):
        for j in lst_j:
            s = sum((y * 0.95 - (i*x + j) * 1.1) < 0)
            if s <= len(dt) * 0.2:
                if mx < sum((i * x + j) * 1.1 - x):
                    mx = sum((i * x + j) * 1.1 - x)
                    solid_profit = j
                    profit_ratio = i - 1
            if s <= m:
                m = s
                m_lst = [m, i, j]
    if m > len(dt) * 0.2:
        solid_profit = m_lst[2]
        profit_ratio = m_lst[1] - 1
    _y = (1+profit_ratio) * x + solid_profit
    profit_ratio = int(profit_ratio * 100) / 100
    upperline = np.max(_y - x)
    lowerline = np.min(_y - x)
    print(f'最佳固定利润为：{solid_profit},\n最佳利润比为{profit_ratio},\n此时上下限为{upperline}, {lowerline}')
    c = input('是否保存价格表 [y/n]:\n')
    if c != 'y':
        return
    df_index_lst = []
    for categ in df_categ_lst:
        for id in categ_id_dic[categ]:
            df_index_lst.append(id)
    df = pd.DataFrame(index=df_index_lst, columns=['name', 'barcode', 'categ', 'solid_profit', 'profit_ratio', 'profit_downline', 'profit_upperline', 'standard_price', 'setted_price', 'faxed_price', 'yso_price'])
    for categ in df_categ_lst:
        for id in categ_id_dic[categ]:
            df.index.name = 'id'
            df['name'].loc[id] = categoryDF['product_variant_ids/name'].loc[id]
            df['barcode'].loc[id] = categoryDF['barcode'].loc[id]
            df['categ'].loc[id] = categoryDF['categ_id'].loc[id]
            df['solid_profit'].loc[id] = solid_profit
            df['profit_ratio'].loc[id] = profit_ratio
            df['profit_downline'].loc[id] = lowerline
            df['profit_upperline'].loc[id] = upperline
            standard_price = categoryDF['standard_price'].loc[id]
            df['standard_price'].loc[id] = standard_price
            profit = max(min(standard_price * profit_ratio, upperline), lowerline)
            setted_price = int(standard_price + profit + solid_profit)
            df['setted_price'].loc[id] = setted_price
            df['faxed_price'].loc[id] = int(setted_price * 1.1)
            if id not in yso_price_df.index:
                continue
            df['yso_price'].loc[id] = yso_price_df['受注明細/税込価格'].loc[id]
    df_categ_s = ','.join(df_categ_lst)
    ntm = datetime.now()
    tm = str(datetime.date(ntm)) + '-' + str(ntm.hour) + '-' + str(ntm.minute)
    fname = f'{tm} setted_price({df_categ_s}).xlsx'
    df.to_excel(f"{file}/compare_price/data/{fname}")
    print(f'新设置的价格表{fname}已保存至{file}/compare_price/data')

