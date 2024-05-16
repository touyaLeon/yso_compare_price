import enum
from re import T
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
from tqdm import tqdm


def compare_price(file):
    print('Reading Price Data')
    id_df = pd.read_excel(rf'{file}\compare_price\data\all_id.xlsx', index_col=0)
    linxas_df = pd.read_excel(rf'{file}\get_price\linxas\data\linxas_price.xlsx', index_col=0)
    smartphonemirai_df = pd.read_excel(rf'{file}\get_price\smartphonemirai\data\smartphonemirai_price.xlsx', index_col=0)
    yso_df = pd.read_excel(rf'{file}\compare_price\data\yso_price.xlsx', index_col='受注明細/製品/ID')
    iphone_num = 155
    yso_iphone_df = yso_df.iloc[:iphone_num].copy(deep=True)
    yso_df['linxas_id'] = None
    yso_df['linxas_name'] = None
    yso_df['linxas_price'] = None
    yso_df['smartphonemirai_id'] = None
    yso_df['smartphonemirai_name'] = None
    yso_df['smartphonemirai_price'] = None
    yso_iphone_df['linxas_id'] = None
    yso_iphone_df['linxas_name'] = None
    yso_iphone_df['linxas_price'] = None
    yso_iphone_df['smartphonemirai_id'] = None
    yso_iphone_df['smartphonemirai_name'] = None
    yso_iphone_df['smartphonemirai_price'] = None
    for i, ysoid in enumerate(tqdm(id_df.index, desc='Comparing Price')):
        linxas_id = id_df['linxas_id'].loc[ysoid]
        smartphonemirai_id = id_df['smartphonemirai_id'].loc[ysoid]
        if not pd.isna(linxas_id):
            linxas_id = int(linxas_id)
            yso_df['linxas_id'].loc[ysoid] = linxas_id
            yso_df['linxas_name'].loc[ysoid] = linxas_df[0].loc[linxas_id]
            yso_df['linxas_price'].loc[ysoid] = linxas_df[1].loc[linxas_id]
            if i < iphone_num:
                yso_iphone_df['linxas_id'].loc[ysoid] = linxas_id
                yso_iphone_df['linxas_name'].loc[ysoid] = linxas_df[0].loc[linxas_id]
                yso_iphone_df['linxas_price'].loc[ysoid] = linxas_df[1].loc[linxas_id]
        if not pd.isna(smartphonemirai_id):
            smartphonemirai_id = int(smartphonemirai_id)
            yso_df['smartphonemirai_id'].loc[ysoid] = smartphonemirai_id
            yso_df['smartphonemirai_name'].loc[ysoid] = smartphonemirai_df[0].loc[smartphonemirai_id]
            yso_df['smartphonemirai_price'].loc[ysoid] = smartphonemirai_df[1].loc[smartphonemirai_id]
            if i < iphone_num:
                yso_iphone_df['smartphonemirai_id'].loc[ysoid] = smartphonemirai_id
                yso_iphone_df['smartphonemirai_name'].loc[ysoid] = smartphonemirai_df[0].loc[smartphonemirai_id]
                yso_iphone_df['smartphonemirai_price'].loc[ysoid] = smartphonemirai_df[1].loc[smartphonemirai_id]
    return yso_df, yso_iphone_df
