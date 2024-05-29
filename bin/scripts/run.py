from get_price.linxas.scripts import linxas_html2pricecsv, linxas_url2html
from get_price.smartphonemirai.scripts import smartphonemirai_html2pricecsv, smartphonemirai_url2html
from compare_price.scripts.compare_price import compare_price
from set_price_test.scripts.set_price_test import set_price, find_best_limitation
import os


def get_sm_html_price(file):
    smartphonemirai_url2html.main(file)
    smartphonemirai_html2pricecsv.main(file)


def get_linxas_html_price(file):
    linxas_url2html.main(file)
    linxas_html2pricecsv.main(file)


def run(file):
    while input('\n按回车继续，键入「e」回车后结束\n') != 'e':
        a = input('''
请选择操作（输入数字并回车）：
1. 重新爬取对手价格
2. 比对价格
3. 固定利润，利润比与利润上下限定价
4. 其他算法
''')
        if a == '1':
            b = input('''\n
请输入要爬取的对象：
1. smartphonemirai
2. linxas
3. all
''')
            while b:
                if b == 'e':
                    exit()
                elif b.isnumeric():
                    b = int(b)
                    if b > 0 and b < 3:
                        if b == 1:
                            get_sm_html_price(file)
                            break
                        elif b == 2:
                            get_linxas_html_price(file)
                            break
                        elif b == 3:
                            get_sm_html_price(file)
                            get_linxas_html_price(file)
                            break
                else:
                    print('\n无法识别')
                    continue
        elif a == '2':
            files = os.listdir(f'{file}/compare_price/data')
            files_s = '\n'.join(map(lambda x: str(x[0]) + '. ' + x[1], enumerate(files)))
            file_num = input(f'''
请选择要进行比较的文件
{files_s}
''')
            while True:
                if file_num == 'e':
                    exit()
                if file_num.isnumeric():
                    if int(file_num) < len(files):
                        break
                file_num = input(f'''
请选择要进行比较的文件（请输入文件前的整数，0-{len(files)-1}）
{files_s}
''')
            filename = files[int(file_num)]
            if filename == 'all_id.xlsx':
                print('无法比较')
                continue
            compare_price(file, filename)
        elif a == '3':
            set_price(file)
        elif a == '4':
            b = input('\n1. 根据竞品价格寻找指定分类下的最优参数\n')
            if b == '1':
                find_best_limitation(file)
        else:
            print('\n无法识别此指令\n')
    else:
        exit()
