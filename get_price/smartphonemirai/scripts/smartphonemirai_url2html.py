import requests
import os
import time
from tqdm import tqdm
import re


def download_content(url, cookie):
    header = {
        "referer": "https://www.baidu.com.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    }
    cookies_str = f'Cookie:{cookie}'
    cookies_lst = cookies_str.split('; ')
    cookies = {}
    for cookie in cookies_lst:
        lst = cookie.split('=')
        key, value = lst[0], lst[1]
        cookies[key] = value
    response = requests.get(url=url, headers=header, cookies=cookies).text
    return response


def save_to_file(filename, content):
    with open(filename, mode="w", encoding="utf-8") as f:
        f.write(content)


def main(file):
    file = rf'{file}/get_price/smartphonemirai/html_from_smartphonemirai'
    for filepath in tqdm(os.listdir(file), desc='Crawling Smartphone Mirai'):
        filestat = os.stat(rf'{file}/{filepath}')
        if time.time() - filestat.st_mtime < 15 * 24 * 60 * 60:  # 如果距离上次更改时间多于15天则更新
            return
        if 'cookie' not in locals().keys():
            cookie = input('Please input Smartphone Mirai Cookie: ')
        lst = re.findall('ct(.*?)_(.*?).html', filepath)
        i = lst[0][1]
        j = lst[0][0]
        _url = f"https://www.smartmirai.net/view/category/ct{j}?page={i}"
        result = download_content(_url, cookie)
        if 'このカテゴリーには商品がありません' in result:
            break
        save_to_file(rf'{file}/{filepath}', result)
