import pandas as pd
from datetime import datetime


def set_price(file):
    categoryDF = pd.read_excel(f'{file}/set_price_test/data/category.xlsx', index_col='product_variant_ids/id')
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
    df_categ_lst = []
    solid_profit_lst = []
    profit_ratio_lst = []
    profit_upperline_list = []
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
        profit_upperline = input(f'请设置产品类别{categ}的利润上限\n')
        while not profit_upperline.isnumeric():
            if profit_upperline == 'e':
                return
            profit_upperline = input(f'输入有误，请再次设置产品类别{categ}的利润上限（正整数）\n')
        profit_upperline_list.append(int(profit_upperline))
    df_index_lst = []
    for categ in df_categ_lst:
        for id in categ_id_dic[categ]:
            df_index_lst.append(id)
    df = pd.DataFrame(index=df_index_lst, columns=['name', 'barcode', 'categ', 'solid_profit', 'profit_ratio', 'profit_upperline', 'standard_price', 'setted_price'])
    for categ, solid_profit, profit_ratio, profit_upperline in zip(df_categ_lst, solid_profit_lst, profit_ratio_lst, profit_upperline_list):
        for id in categ_id_dic[categ]:
            df.index.name = 'id'
            df['name'].loc[id] = categoryDF['product_variant_ids/name'].loc[id]
            df['barcode'].loc[id] = categoryDF['barcode'].loc[id]
            df['categ'].loc[id] = categoryDF['categ_id'].loc[id]
            df['solid_profit'].loc[id] = solid_profit
            df['profit_ratio'].loc[id] = profit_ratio
            df['profit_upperline'].loc[id] = profit_upperline
            standard_price = categoryDF['standard_price'].loc[id]
            df['standard_price'].loc[id] = standard_price
            profit = min(standard_price * profit_ratio, profit_upperline)
            setted_price = int(standard_price + profit)
            df['setted_price'].loc[id] = setted_price
    df_categ_s = ','.join(df_categ_lst)
    ntm = datetime.now()
    tm = str(datetime.date(ntm)) + ' ' + str(ntm.hour) + ':' + str(ntm.minute) + ':' + str(ntm.second)
    df.to_excel(f"{file}/compare_price/data/{tm}-setted_price({df_categ_s}).xlsx")
