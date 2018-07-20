import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def get_html_text(url, code='utf-8'):  # 获得对应页面
    try:
        r = requests.get(url)
        r.raise_for_status
        r.encoding = code
        return r.text
    except:
        return ""


def get_stock_list(lst, stock_url):  # 获得包含所有股票信息的列表
    html = get_html_text(stock_url, 'GB2312')  # 用定义的函数获取页面信息(东方财富网的编码方式为‘GB2312’)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')  # a=soup中包含的所有<a>标签的列表
    for i in a:  # 遍历所用<a>标签(不是所用的<a>标签都有着包含着我们所需要的信息的结构，所以用try,except)
        try:
            href = i.attrs['href']  # 获取<a>标签中的链接属性
            lst.append(re.findall(r'[s][z]\d{6}', href)[0])  # 用正则表达式寻找以sz开头的后面跟着6个数字的上证股票代码
        except:
            continue  # 忽略其他不符合要求的报错信息


def get_stock_info(lst, stock_url, out_file):
    count = 0  # 为循环计数做准备，用于计算爬取进度(股票数)
    lst2 = []  # 设置为空列表，将要存放lst中个股信息的字典
    for stock in lst:
        print('\r当前进度:{:.2f}%'.format(count * 100 / 66), end='')  # 一个当前爬取进度的输出
        if count > 65:  # 设置爬取数量为66条
            break
        url = stock_url + stock + ".html"
        # 如万科A股的url为https://gupiao.baidu.com/stock/sz000002.html，所以可以通过此方法构造对应的url
        html = get_html_text(url)
        try:
            infoDict = {}
            soup = BeautifulSoup(html, 'html.parser')
            stockInfo = soup.find('div', attrs={'class': 'stock-bets'})  # 找到属性为class=stock-bets的<div>标签，下文有网页源代码展示
            name = stockInfo.find_all(attrs={'class': 'bets-name'})[0]  # 加[0]返回tag
            if name is None:  # 如果获取不到股票名称跳出循环，且不计数
                continue

            infoDict.update({'a股票名称': name.text.strip()})

            keylist = stockInfo.find_all('dt')
            valuelist = stockInfo.find_all('dd')
            for i in range(len(keylist)):
                key = keylist[i].text
                val = valuelist[i].text
                infoDict[key] = val  # 向字典中新增内容
            count += 1
            lst2.append(infoDict)

        except:
            continue
    df = pd.DataFrame(lst2)  # 将由字典组成的列表lst2转换成二维数组，并以这种方式输出到out_file文件中
    df.rename(columns={'a股票名称': '股票名称'}, inplace=True)
    df.to_csv(out_file, index=False, sep=',')


def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    output_file = 'D://BaiduStockInfo.csv'
    lst = []
    get_stock_list(lst, stock_list_url)  # 获得股票列表
    get_stock_info(lst, stock_info_url, output_file)


main()
