from posixpath import split
import pandas as pd
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')


def compute_price_ratio(df):
    df['smartphonemirai_price'] = pd.to_numeric(df['smartphonemirai_price'])
    df['linxas_price'] = pd.to_numeric(df['linxas_price'])
    df['linxas/yso'] = df['linxas_price'] / df['受注明細/単価']
    df['smartphonemirai/yso'] = df['smartphonemirai_price'] / df['受注明細/単価']
    return df


def compare_price(file):
    print('Reading Price Data')
    id_df = pd.read_excel(f'{file}/compare_price/data/all_id.xlsx', index_col=0)
    linxas_df = pd.read_excel(f'{file}/get_price/linxas/data/linxas_price.xlsx', index_col=0)
    smartphonemirai_df = pd.read_excel(f'{file}/get_price/smartphonemirai/data/smartphonemirai_price.xlsx', index_col=0)
    yso_df = pd.read_excel(f'{file}/compare_price/data/yso_price.xlsx', index_col='受注明細/製品/ID')
    iphone_num = 155
    yso_iphone_df = yso_df.iloc[:iphone_num].copy(deep=True)
    yso_df['linxas_id'] = None
    yso_df['linxas_name'] = None
    yso_df['linxas_price'] = pd.NA
    yso_df['smartphonemirai_id'] = None
    yso_df['smartphonemirai_name'] = None
    yso_df['smartphonemirai_price'] = pd.NA
    yso_iphone_df['linxas_id'] = None
    yso_iphone_df['linxas_name'] = None
    yso_iphone_df['linxas_price'] = pd.NA
    yso_iphone_df['smartphonemirai_id'] = None
    yso_iphone_df['smartphonemirai_name'] = None
    yso_iphone_df['smartphonemirai_price'] = pd.NA
    for i, ysoid in enumerate(tqdm(id_df.index, desc='Comparing Price')):
        linxas_id = id_df['linxas_id'].loc[ysoid]
        smartphonemirai_id = id_df['smartphonemirai_id'].loc[ysoid]
        if not pd.isna(linxas_id):
            if linxas_id in linxas_df.index:
                linxas_id = int(linxas_id)
                linxas_name = linxas_df[0].loc[linxas_id]
                linxas_price = ''.join(linxas_df[1].loc[linxas_id].split(','))
                yso_df['linxas_id'].loc[ysoid] = linxas_id
                yso_df['linxas_name'].loc[ysoid] = linxas_name
                yso_df['linxas_price'].loc[ysoid] = linxas_price
                if i < iphone_num:
                    yso_iphone_df['linxas_id'].loc[ysoid] = linxas_id
                    yso_iphone_df['linxas_name'].loc[ysoid] = linxas_name
                    yso_iphone_df['linxas_price'].loc[ysoid] = linxas_price
        if not pd.isna(smartphonemirai_id):
            if smartphonemirai_id in smartphonemirai_df.index:
                smartphonemirai_name = smartphonemirai_df[0].loc[smartphonemirai_id]
                smartphonemirai_price = ''.join(smartphonemirai_df[1].loc[smartphonemirai_id].split(','))
                yso_df['smartphonemirai_id'].loc[ysoid] = smartphonemirai_id
                yso_df['smartphonemirai_name'].loc[ysoid] = smartphonemirai_name
                yso_df['smartphonemirai_price'].loc[ysoid] = smartphonemirai_price
                if i < iphone_num:
                    yso_iphone_df['smartphonemirai_id'].loc[ysoid] = smartphonemirai_id
                    yso_iphone_df['smartphonemirai_name'].loc[ysoid] = smartphonemirai_name
                    yso_iphone_df['smartphonemirai_price'].loc[ysoid] = smartphonemirai_price
    yso_df = compute_price_ratio(yso_df)
    yso_iphone_df = compute_price_ratio(yso_iphone_df)
    return yso_df, yso_iphone_df
