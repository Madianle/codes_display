from selenium import webdriver
from time import sleep

# #测试
# browser = webdriver.Chrome(r'D:\2017\百度云下载文件\Chrome-bin\Chrome-bin\chromedriver.exe')  #写入自己的路径
# browser.get('http://www.baidu.com')
# browser.maximize_window()
# sleep(1)
# browser.quit()

# 实例
import csv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote

#chrome的无界面模式，爬取时不会弹出浏览器(需要调试时建议还是换到有界面模式)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(r'D:/Program Files/Chrome-bin/Chrome-bin/chromedriver.exe', chrome_options=chrome_options)

#chrome的有界面模式：
#browser = webdriver.Chrome(r'D:/Program Files/Chrome-bin/Chrome-bin/chromedriver.exe')

KEYWORD = 'iPad'  # 设置你所要爬取的商品
wait = WebDriverWait(browser, 10)  # 这是一个显式等待的设置

# 定义index_page()方法用于抓取本页商品列表
def index_page(page):
    """
    抓取索引页
    :param page: 页码
    """
    print('正在爬取第', page, '页')
    #先定义csv文件并写上标签栏
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)  # quote()可有效屏蔽一些url中不被允许的字符
        browser.get(url)  # 用chrome打开url对应界面
        if page == 1:
            browser.maximize_window() #为使location信息加载完全
        if page > 1:
                input = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="mainsrp-pager"]//div[@class="form"]/input')))
                # 在规定时间(10s)内返回查找到的页面跳转输入框，并赋给input
                submit = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="mainsrp-pager"]//div[@class="form"]/span[3]')))
                # 在规定时间(10s)内返回查找到的确定点击按钮，并赋给submit
                input.clear()
                input.send_keys(page)  # 输入要跳转页面到跳转框内
                submit.click()  # 点击确定按钮

        wait.until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active span'), str(page)))
            # 等到跳转页面数出现在可点击页面中
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
            # 等到商品出现在跳转后的页面中
        get_products()  # 获取商品信息并写入json文件

    except TimeoutException:
        index_page(page)  # 若超时或出现错误则重新加载


def get_products():
    """
    提取商品数据
    """
    nums = len(browser.find_elements_by_css_selector('.m-itemlist .items .item'))  # 提取商品个数
    #products = []
    for num in range(nums):
        product = {
            'price': browser.find_elements_by_css_selector('.m-itemlist .items .item .price strong')[num].text,
            'deal': browser.find_elements_by_css_selector('.m-itemlist .items .item .deal-cnt')[
                num].text,
            'title': browser.find_elements_by_css_selector('.m-itemlist .items .item .title')[num].text,
            'shop': browser.find_elements_by_css_selector('.m-itemlist .items .item .shop')[num].text,
            'location': browser.find_elements_by_css_selector('.m-itemlist .items .item .location')[
                num].text
        }
        print(product)
        #products.append(product)
        save_to_csv(product)

def save_to_csv(product):
    try:
        with open('C:\\Users\\47458\\Desktop\\data.csv', 'a', encoding='gb18030', newline='') as csvfile:
            fieldnames = ['price', 'deal', 'title', 'shop', 'location']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(product)
        print('存储到csv文件成功')

    except:
        print('存储到csv文件失败')




def main():
    """
    遍历每一页
    """
    MAX_PAGE = 100
    #在主函数中创建csv文件的标签行
    with open('C:\\Users\\47458\\Desktop\\data.csv', 'w', encoding='gb18030', newline='') as csvfile:
        fieldnames = ['price', 'deal', 'title', 'shop', 'location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    for i in range(1, MAX_PAGE + 1):
        index_page(i)
    browser.close()


if __name__ == '__main__':
    main()
