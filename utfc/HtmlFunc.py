import bs4
import requests


'''
没鸟用
find_all 
name	检索标签的名称
attrs	对标签属性值的检索字符串，可标注属性检索
recursive	布尔型变量，是否对子孙全部检索，默认为True
text	标签节点中文本
'''

class htmf:
    html = ''
    soup = None
    def __init__(self, txt='', url='', fn='', features='html.parser'):
        if url == '' and fn == '':
            self.html = txt
        elif fn == '':
            self.html = requests.get(url).text
        else:
            self.html = open(fn, 'r').read()
        self.soup = bs4.BeautifulSoup(self.html, features=features)
