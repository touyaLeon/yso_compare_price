from get_price.linxas.scripts import linxas_html2pricecsv, linxas_url2html
from get_price.smartphonemirai.scripts import smartphonemirai_html2pricecsv, smartphonemirai_url2html
from compare_price.scripts.compare_price import compare_price


def getHtml(file):
    linxas_url2html.main(file)
    smartphonemirai_url2html.main(file)


def getPrice(file):
    linxas_html2pricecsv.main(file)
    smartphonemirai_html2pricecsv.main(file)


def comparePrice(file):
    all_result = compare_price(file)
    return all_result


def main():
    file = '.'
    if input('Update price data? [y/n]: ') == 'y':
        getHtml(file)
    getPrice(file)
    all_result, iphone_result = comparePrice(file)
    print('Saving results')
    all_result.to_excel(f'{file}/results/all_results.xlsx')
    iphone_result.to_excel(f'{file}/results/iphone_results.xlsx')


if __name__ == '__main__':
    main()
