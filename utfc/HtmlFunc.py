import bs4
import requests


'''
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


url='https://www.thisav.com/videos?o=mr&type=&c=0&t=a&page={}'
proxies = {
  "http": "http://127.0.0.1:12367",
  "https": "http://127.0.0.1:12367",
}
import time
import bs4
from urllib import parse
import requests
fall = 246791 //12
import random
i=1
while i < fall:
    try:
        s =  bs4.BeautifulSoup(requests.get(url.format(i),proxies=proxies,timeout=30).text, features='html.parser')
        uall = s.find_all('a',class_='video_link')
        with open('c:/CTFDOCS/uav.txt','a') as f:
            for x in uall:
                u = parse.unquote(x.get('href'))
                if u.endswith('html') or u.endswith('htm') : f.write(u+'\n')
        time.sleep(random.random())
        print(f'[+]Pange:{i:06d}/{fall}\t {round(i/fall),4}% OK')
        i+=1
    except:
        time.sleep(random.random()*5)
        print(f'[-]Pange:{i:06d}-ERR')