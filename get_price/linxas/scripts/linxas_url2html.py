import requests
import time, os
from tqdm import tqdm


def download_content(url):
    header = {
        "referer": "https://www.baidu.com.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    }
    cookies_str = 'remember_customer_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IjdMK2xrUWlBbUttQW40Vm5uSFVCcUE9PSIsInZhbHVlIjoid3FIbmJpUGU5OFRxdWJuTTNXVGpHWkVCQ1lwR3d1bXdSOFJSQ1R0bHRoYXdMeWRCN0ZMUUhvZ1hkM0UrMHdmVEJqUjBDUXlUS0FscFZYUDRXVzZPQ2FjemFQalZoNThLTG9xOWc2djNQZ212UHJoRWY3T0JkN2wzaUg0MlBmRVgrRFFnQVNRQzRRY21lM2MvLzl4ZGg1TFpkK1UwS3dVTk9sWmNyK1AreWpxNHo5RkkrS00veGpvbWtDT1BDL0NIL3YzUWRmQXNYdEpYQWNnS2RVWERpaUoxNi9uRVZHVUdHVnNLSzlPMDRPTT0iLCJtYWMiOiJmNDY0OGMwNGI2MDEyMjU3ZjRlMjMzYWEyNTg1NzI1NWU2ZjFkMTkwNzU5YWQ2OTgwMzA0Y2M5N2IxMTFmNDFhIiwidGFnIjoiIn0%3D; product_viewed=eyJpdiI6IlRqOTJvY1dsTjB0MVhoMXhWK2RTV3c9PSIsInZhbHVlIjoicm5HKzZEVnpCNFVicFIwQmttRG9CODVESmVjVEI4L2sybVRVM1o5VUNYWklBaFo2YUJ3NnZmVlVQMzh1akRlRHhRM1pyeW1CYW9pd1J6ZVh0amNtMFFVY0dJVVh4SitJS3RvcUpZYlEyVlU9IiwibWFjIjoiNjJiOTFlYjllN2MzN2VmZTIyMWUwMWQwMWE3YTA1ZjZmMDRjOTk1N2U3YmU3YjM1ODY4MDE5MGJjNjZkYmU5NCIsInRhZyI6IiJ9; XSRF-TOKEN=eyJpdiI6IjNReEFLWmJkVzdtanZaNVlYTU5idmc9PSIsInZhbHVlIjoiR0RxbmNrTlJmRHlGUzlPb2xKMnRkTk0xQkdFUDlUa0FmaUxiYkYzYmhham9DWXN3V3FwSFRMSk1HdHBoS2EyRHRIeXNtekQzUDVTMXNrb3prN2FheXhkWEE4V1dsaVZTZnA4RGcwT1hMNjZVb2FOSVBZZW1Hb2wyUFQyWFU3MnQiLCJtYWMiOiJjYTUyMDhkNzExMjMwMzBjYWFiNGYwNTljZjE0NjQ1ZjljMWZiZGY4ZmU4MWRlYjI4Mzk0YWI4OTQ1NTU4ZmM4IiwidGFnIjoiIn0%3D; b_ses=eyJpdiI6Im02MTNISStZQ0xVekYvd2QwNThJbVE9PSIsInZhbHVlIjoiRXd3VHNLdi8xbzhncGExYzM3dDdKNHkweGVaVVpSV05Tc2JyK29kZm8zSHdzckhJTWZ2N2E1aDE5UVVvb05xSE0zOEVjOHNHWnBldEFqbGZRN1kzQ0RySlptZ0NpYlBLTVk2cCtoOUQxNXl0TVJid25FZU1BM1RvcjZCQlU5ZngiLCJtYWMiOiJhOWU1MDU5OWNjN2FjMzRjYmFkYWU2ZGM5YjAxZjI5ZjFjZjZmODY3NTg1MGEzZTQyNzI5ZTcyOWQ2OWQ3MjRlIiwidGFnIjoiIn0%3D'
    cookies_lst = cookies_str.split('; ')
    cookies = {}
    for cookie in cookies_lst:
        lst = cookie.split('=')
        key, value = lst[0], lst[1]
        cookies[key] = value
    response = requests.get(url=url, headers=header, cookies=cookies).text
    time.sleep(5)
    return response


def save_to_file(filename, content):
    with open(filename, mode="w", encoding="utf-8") as f:
        f.write(content)


def main(file):
    for i in tqdm(range(3, 200), desc='Crawling Linxas'):
        filepath = fr"{file}\get_price\linxas\html_from_linxas\id{i}.html"
        if f'id{i}.html' in os.listdir(fr'{file}\get_price\linxas\html_from_linxas'):
            filestat = os.stat(filepath)
            if time.time() - filestat.st_mtime < 15 * 24 * 60 * 60:  # 如果距离上次更改时间多于15天则更新
                continue
        else:
            continue
        _url = f"https://linxas.online/product.php?id={i}"
        result = download_content(_url)
        if 'ページが見つかりません' in result:
            continue
        save_to_file(filepath, result)
