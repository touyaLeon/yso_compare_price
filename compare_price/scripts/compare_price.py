import pandas as pd
from tqdm import tqdm
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


def create_df_cols(df):
    df['差额1'] = pd.NA
    df['差额2'] = pd.NA
    df['百分比1'] = pd.NA
    df['百分比2'] = pd.NA
    df['贵或便宜或居中'] = None
    df['linxas_id'] = None
    df['linxas_name'] = None
    df['linxas_price￥'] = pd.NA
    df['smartphonemirai_id'] = None
    df['smartphonemirai_name'] = None
    df['smartphonemirai_price￥'] = pd.NA
    return df


def compare_price_func(x, lst):
    if x > max(lst):
        return '贵'
    elif x < min(lst):
        return '便宜'
    elif sum(pd.Series(lst).isna()):
        return None
    else:
        return '居中'



def compute_price_ratio(df, yso_price_name='受注明細/税込価格'):
    df['smartphonemirai_price￥'] = pd.to_numeric(df['smartphonemirai_price￥'])
    df['linxas_price￥'] = pd.to_numeric(df['linxas_price￥'])
    df['差额1'] = df[yso_price_name] - df['linxas_price￥']
    df['百分比1'] = list(map(lambda x, y: '{:.2f}%'.format(x/y*100) if not pd.isna(x) else pd.NA, df['差额1'], df[yso_price_name]))
    df['差额2'] = df[yso_price_name] - df['smartphonemirai_price￥']
    df['百分比2'] = list(map(lambda x, y: '{:.2f}%'.format(x/y*100) if not pd.isna(x) else pd.NA, df['差额2'], df[yso_price_name]))
    df['贵或便宜或居中'] = list(map(compare_price_func, df[yso_price_name], zip(df['smartphonemirai_price￥'], df['linxas_price￥'])))
    return df


def compare_price(file, filename):
    print('Reading Price Data')
    id_df = pd.read_excel(f'{file}/compare_price/data/all_id.xlsx', index_col=0)
    linxas_df = pd.read_excel(f'{file}/get_price/linxas/data/linxas_price.xlsx', index_col=0)
    smartphonemirai_df = pd.read_excel(f'{file}/get_price/smartphonemirai/data/smartphonemirai_price.xlsx', index_col=0)
    yso_df = pd.read_excel(f'{file}/compare_price/data/{filename}')
    if 'id' in yso_df.columns:
        yso_df.index = yso_df['id']
        del yso_df['id']
    elif '受注明細/製品/ID' in yso_df.columns:
        yso_df.index = yso_df['受注明細/製品/ID']
        del yso_df['受注明細/製品/ID']
    else:
        print('匹配ID出错')
        return
    yso_df = create_df_cols(yso_df)
    for i, ysoid in enumerate(tqdm(id_df.index, desc='Comparing Price')):
        linxas_id = id_df['linxas_id'].loc[ysoid]
        smartphonemirai_id = id_df['smartphonemirai_id'].loc[ysoid]
        if not pd.isna(linxas_id):
            if linxas_id in linxas_df.index:
                linxas_id = int(linxas_id)
                linxas_name = linxas_df[0].loc[linxas_id]
                linxas_price = ''.join(linxas_df[1].loc[linxas_id].split(','))
                if ysoid in yso_df.index:
                    yso_df['linxas_id'].loc[ysoid] = str(linxas_id)
                    yso_df['linxas_name'].loc[ysoid] = linxas_name
                    yso_df['linxas_price￥'].loc[ysoid] = linxas_price
        if not pd.isna(smartphonemirai_id):
            if smartphonemirai_id in smartphonemirai_df.index:
                smartphonemirai_name = smartphonemirai_df[0].loc[smartphonemirai_id]
                smartphonemirai_price = ''.join(smartphonemirai_df[1].loc[smartphonemirai_id].split(','))
                if ysoid in yso_df.index:
                    yso_df['smartphonemirai_id'].loc[ysoid] = smartphonemirai_id
                    yso_df['smartphonemirai_name'].loc[ysoid] = smartphonemirai_name
                    yso_df['smartphonemirai_price￥'].loc[ysoid] = smartphonemirai_price
    if 'faxed_price' in yso_df.columns:
        yso_price_name = 'faxed_price'
    else:
        yso_price_name = '受注明細/税込価格'
    compared_df = compute_price_ratio(yso_df, yso_price_name=yso_price_name)
    ntm = datetime.now()
    tm = str(datetime.date(ntm)) + '-' + str(ntm.hour) + '-' + str(ntm.minute)
    nm_lst = filename.split(' ')
    if len(nm_lst) > 1:
        nm = nm_lst[1]
    else:
        nm = nm_lst[0]
    if nm[-4:] == 'xlsx':
        nm = nm[:-5]
    result_name = f'{tm} {nm} result.xlsx'
    compared_df.to_excel(f'{file}/results/{result_name}')
    print(f'对比完成，结果已保存到{result_name}')
    return compared_df.dropna(axis='index', subset=[yso_price_name])