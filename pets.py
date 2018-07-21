import requests
from bs4 import BeautifulSoup
import os


def get_html_text(url):  # 获得对应页面
    try:
        r = requests.get(url)
        r.raise_for_status
        return r.text
    except:
        return ""


def get_photo_list(lst, pets_url):  # 获得包含所有宠物图片url的列表
    html = get_html_text(pets_url)
    soup = BeautifulSoup(html, 'html.parser')
    imgs = soup.find_all('img', attrs={'class': 'photo-item__img'})
    for img in imgs:
        lst.append(img.attrs['src'])  # 此时的lst是包含图片url链接的列表


def get_photos(lst, root):
    count = 0   # 为循环计数做准备，用于计算爬取进度
    for url in lst:
        count += 1
        # print('\r当前进度:{:.2f}%'.format(count * 100 / len(lst)), end='')  # 一个当前爬取进度的输出
        path = root + str(count) + '.jpg'
        try:
            if not os.path.exists(root):  # 判断根目录是否存在，如果不存在，建立一个这样的目录
                os.mkdir(root)
            if not os.path.exists(path):
                r = requests.get(url)
                with open(path, 'wb') as f:
                    f.write(r.content)
                    f.close()
                    print('\r文件保存成功,当前进度:{:.2f}%'.format(count * 100 / len(lst)), end='')
            else:
                print('\r文件已存在,当前进度:{:.2f}%'.format(count * 100 / len(lst)), end='')
        except:
            print('获取失败')


def main():
    pets_url = 'https://www.pexels.com/search/pets/'
    root = 'D://pics//'
    lst = []
    get_photo_list(lst, pets_url)
    get_photos(lst, root)


main()
