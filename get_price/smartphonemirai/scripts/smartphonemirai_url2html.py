import requests
import os
import time
from tqdm import tqdm
import re


def download_content(url):
    header = {
        "referer": "https://www.baidu.com.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    }
    cookies_str = 'Cookie:tempid=d10f9cdb8aefcf8e0334b106e2ff5582; _ga=GA1.1.1359910223.1714033652; makeshop-yummy666888__zc=3.662a13f4334cb0001fda0526.3.0.0.0.; makeshop-yummy666888__zc_store={%22cv%22:null}; chr_id=3301; chr_id230327000001=3301; db=yummy666888; identify=f044c435ecc3a279f0362fb8e6a9a862; PHPSESSID=rjm2bpipdn76e50ja62hp615u2; secure_yummy666888_key=0e4b52847d94e210c14019f0f43bbd31; login_id=230327000001; 230327000001_key=e14c6ae0cd7d5b6bc283f0e2b787865f; AWSALB=TH33zjfM1JfbhqgLrEpSY4ZstKgVqGrUp5QkrvS6SDz57asThh3ht+P+nN5s4jk8RyLaUXZTtOoh+VVlTt2nTRHx1W+Hx2F+Myw6UqI/snfAffwyBSPRMVkxkpVYhA/f7TsldTkCXhvpAIXO7KdidQEWiODdFak6qTmT5KsC9U2nwEW+kWmZsjONYIDRxg==; AWSALBCORS=TH33zjfM1JfbhqgLrEpSY4ZstKgVqGrUp5QkrvS6SDz57asThh3ht+P+nN5s4jk8RyLaUXZTtOoh+VVlTt2nTRHx1W+Hx2F+Myw6UqI/snfAffwyBSPRMVkxkpVYhA/f7TsldTkCXhvpAIXO7KdidQEWiODdFak6qTmT5KsC9U2nwEW+kWmZsjONYIDRxg==; slvd=1714540847; makeshop-yummy666888__zc_us=6631cdeb1dbdbf00357836f4.0.18.1714540011077; _ga_HFBR56ZH89=GS1.1.1714540009.4.1.1714540855.0.0.0'
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
        filestat = os.stat(rf'{file}\{filepath}')
        lst = re.findall('ct(.*?)_(.*?).html', filepath)
        i = lst[0][1]
        j = lst[0][0]
        if time.time() - filestat.st_mtime < 15 * 24 * 60 * 60:  # 如果距离上次更改时间多于15天则更新
            continue
        _url = f"https://www.smartmirai.net/view/category/ct{j}?page={i}"
        result = download_content(_url)
        if 'このカテゴリーには商品がありません' in result:
            break
        save_to_file(rf'{file}\{filepath}', result)
