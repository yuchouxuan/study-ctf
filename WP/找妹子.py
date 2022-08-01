import matplotlib.pyplot as plt
import numpy as np
import cv2,requests ,base64,gc

iall = cv2.imread('z:/all.png')[50:-1,50:-1,:]
plt.imshow(iall)
iall.shape
h,w = 75,50
url = 'http://e3e42887-0eae-4633-9b01-29e8d74b9840.challenge.ctf.show'
se = requests.session()
import time
cookie={}
while True:
    txt = se.get(url+'/start').text
    if 'ctfshow' in txt:
        print(txt)
        break
    b64start = txt.find('data:image/jpeg;base64,')
    print(txt[-125:-115])
    txt = txt[b64start+23:txt.find("'",b64start)]
    with open('tmp.png','wb') as f:
        f.write(base64.b64decode(txt))
        f.close()
    tmpf = cv2.imread('tmp.png')
    th,tw,_ = tmpf.shape
    tmp=cv2.resize(tmpf,(tw//10,th//10),cv2.INTER_LANCZOS4)
    res =cv2.matchTemplate( iall,tmp,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    tmpall = iall.copy()
    rb=(max_loc[0]+tw//10,max_loc[1]+th//10)
    cv2.rectangle(tmpall, max_loc, rb, (0,0,255), 3)
    try:
        nW = 'ABCDEFGHIJ'[(max_loc[1])//h] + str(int((max_loc[0])//w))
    except:
        pass
    print('find:---->',nW)
    cv2.imshow('Target',tmpf)
    cv2.imshow('Find-resault',tmpall)
    po={'meizi_id':nW}
    resp= se.post(url+'/check',data=po)
    txt = resp.text
    cv2.waitKey(delay=10)
    if "回答错误" not in txt:
       cookie = resp.cookies.get('session')
    else:
        print(txt)
        se.cookies.clear_session_cookies()
        se.cookies.set('session',cookie)
    del res,tmpf,tmp ,tmpall
    gc.collect()
input()
cv2.destroyAllWindows()