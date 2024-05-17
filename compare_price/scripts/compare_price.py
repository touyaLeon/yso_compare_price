from posixpath import split
import pandas as pd
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')


def create_df_cols(df):
    df['差额1'] = pd.NA
    df['差额2'] = pd.NA
    df['百分比1'] = pd.NA
    df['百分比2'] = pd.NA
    df['贵或便宜或居中'] = pd.NA
    df['参考价'] = pd.NA
    df['与卖价差额'] = pd.NA
    df['与卖价差额百分比'] = pd.NA
    df['linxas_id'] = None
    df['linxas_name'] = None
    df['linxas_price￥'] = pd.NA
    df['smartphonemirai_id'] = None
    df['smartphonemirai_name'] = None
    df['smartphonemirai_price￥'] = pd.NA
    return df


def compare_price_func(x, y, z):
    if x > y and x > z:
        return '贵'
    elif x < y and x < z:
        return '便宜'
    else:
        return '居中'


def get_reference_price(x, y, z):
    if z > x*0.95 and z > y*0.95:
        return z
    else:
        m = min(x*0.95, y*0.95)
        if pd.isna(m):
            return pd.NA
        else:
            return '{:.0f}'.format(m)


def compute_price_ratio(df, yso_price_name='受注明細/税込価格'):
    df['smartphonemirai_price￥'] = pd.to_numeric(df['smartphonemirai_price￥'])
    df['linxas_price￥'] = pd.to_numeric(df['linxas_price￥'])
    df['差额1'] = df[yso_price_name] - df['linxas_price￥']
    df['百分比1'] = list(map(lambda x, y: '{:.2f}%'.format(x/y*100) if not pd.isna(x) else pd.NA, df['差额1'], df[yso_price_name]))
    df['差额2'] = df[yso_price_name] - df['smartphonemirai_price￥']
    df['百分比2'] = list(map(lambda x, y: '{:.2f}%'.format(x/y*100) if not pd.isna(x) else pd.NA, df['差额2'], df[yso_price_name]))
    df['贵或便宜或居中'] = list(map(compare_price_func, df[yso_price_name], df['smartphonemirai_price￥'], df['linxas_price￥']))
    return df


def compute_reference_price(df, yso_price_name='受注明細/税込価格'):
    df['参考价'] = list(map(get_reference_price, df['smartphonemirai_price￥'], df['linxas_price￥'], df['受注明細/製品/原価']))
    df['与卖价差额'] = pd.to_numeric(df['参考价']) - df[yso_price_name]
    df['与卖价差额百分比'] = list(map(lambda x, y: '{:.2f}%'.format(x/y), df['与卖价差额'], df[yso_price_name]))
    return df


def compare_price(file):
    print('Reading Price Data')
    id_df = pd.read_excel(f'{file}/compare_price/data/all_id.xlsx', index_col=0)
    linxas_df = pd.read_excel(f'{file}/get_price/linxas/data/linxas_price.xlsx', index_col=0)
    smartphonemirai_df = pd.read_excel(f'{file}/get_price/smartphonemirai/data/smartphonemirai_price.xlsx', index_col=0)
    yso_df = pd.read_excel(f'{file}/compare_price/data/yso_price.xlsx', index_col='受注明細/製品/ID')
    iphone_num = 155
    yso_iphone_df = yso_df.iloc[:iphone_num].copy(deep=True)
    yso_df = create_df_cols(yso_df)
    yso_iphone_df = create_df_cols(yso_iphone_df)
    for i, ysoid in enumerate(tqdm(id_df.index, desc='Comparing Price')):
        linxas_id = id_df['linxas_id'].loc[ysoid]
        smartphonemirai_id = id_df['smartphonemirai_id'].loc[ysoid]
        if not pd.isna(linxas_id):
            if linxas_id in linxas_df.index:
                linxas_id = int(linxas_id)
                linxas_name = linxas_df[0].loc[linxas_id]
                linxas_price = ''.join(linxas_df[1].loc[linxas_id].split(','))
                yso_df['linxas_id'].loc[ysoid] = str(linxas_id)
                yso_df['linxas_name'].loc[ysoid] = linxas_name
                yso_df['linxas_price￥'].loc[ysoid] = linxas_price
                if i < iphone_num:
                    yso_iphone_df['linxas_id'].loc[ysoid] = str(linxas_id)
                    yso_iphone_df['linxas_name'].loc[ysoid] = linxas_name
                    yso_iphone_df['linxas_price￥'].loc[ysoid] = linxas_price
        if not pd.isna(smartphonemirai_id):
            if smartphonemirai_id in smartphonemirai_df.index:
                smartphonemirai_name = smartphonemirai_df[0].loc[smartphonemirai_id]
                smartphonemirai_price = ''.join(smartphonemirai_df[1].loc[smartphonemirai_id].split(','))
                yso_df['smartphonemirai_id'].loc[ysoid] = smartphonemirai_id
                yso_df['smartphonemirai_name'].loc[ysoid] = smartphonemirai_name
                yso_df['smartphonemirai_price￥'].loc[ysoid] = smartphonemirai_price
                if i < iphone_num:
                    yso_iphone_df['smartphonemirai_id'].loc[ysoid] = smartphonemirai_id
                    yso_iphone_df['smartphonemirai_name'].loc[ysoid] = smartphonemirai_name
                    yso_iphone_df['smartphonemirai_price￥'].loc[ysoid] = smartphonemirai_price
    yso_df = compute_price_ratio(yso_df)
    yso_df = compute_reference_price(yso_df)
    yso_iphone_df = compute_price_ratio(yso_iphone_df)
    yso_iphone_df = compute_reference_price(yso_iphone_df)
    return yso_df, yso_iphone_df
