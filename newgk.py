import bs4 ,requests ,utfc.StrFunc as sf,tqdm.notebook as tqdm
import os,datetime as dtt ,time

urllist='https://www.samrela.com/student/my_course.do'
urlheartbit='https://www.samrela.com/portal/seekNew.do'
header='''Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding:gzip, deflate, br
Accept-Language:zh-CN,zh;q=0.9,en;q=0.8
Cache-Control:max-age=0
Content-Length:108
Content-Type:application/x-www-form-urlencoded
Origin:https://www.samrela.com
Referer:https://www.samrela.com/student/my_course.do
Sec-Ch-Ua:"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"
Sec-Ch-Ua-Mobile:?0
Sec-Ch-Ua-Platform:"Windows"
Sec-Fetch-Dest:document
Sec-Fetch-Mode:navigate
Sec-Fetch-Site:same-origin
Sec-Fetch-User:?1
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'''
header = sf.CharF.str2Dir(header)
cookies='aliyungf_tc=f9903b83fe52c5c25efb215332b3713b85275c01c2a555410ff54d61ee8eabfe; acw_tc=0bc5047116987209564335566ead1671d3c8794c610276d548e2f4fe69a380; SESSION=YzQyNjYzMWQtMzEyZC00Y2M1LTgzOTAtNGRlOWQwYjMzNTVl; Hm_lvt_2a44bcedc6cb4650939a4a8eac1adfb9=1698720958; Hm_lpvt_2a44bcedc6cb4650939a4a8eac1adfb9=1698722431'
cookies=sf.CharF.str2Dir(cookies,';','=')
ses=requests.session()

def flash_list():
    global ses,header,cookies
    slist = []
    for i in range(1):
        postdata = f'pageType=%24%7Btype%7D&searchType=1&pageType=%24%7Btype%7D&rowCount=44&menu=course&pageSize=10&currentPage={i+1}'
        postdata = sf.CharF.str2Dir(postdata,'&','=')
        # print(postdata)
        htmplist=ses.post(urllist,data=postdata,cookies=cookies,headers=header).text
        listx = bs4.BeautifulSoup(htmplist,"html.parser")
        for row in listx.find_all(class_='hoz_course_row'):
            try:
                name = row.find_all(class_='hoz_course_name')[0].text
                id = row.find_all(class_='fr btn_group')[0].find_all('input')[0]['onclick'].split('(')[1].replace(')','')
                sid=row.find_all(class_="hoz_course_name")[0].findAll('a')[0]['href'].split('courseId=')[1]
                proc=row.find_all(class_='h_pro_percent')[0].text
                slist.append((name,id,sid,proc))
            except:
                pass 
    
    os.system('cls')
    for i in slist[::-1]:
        print(i[0],i[1],i[2],i[3])
    return slist

icont = 1
slist=flash_list()
while len(slist)>0:
    t=dtt.datetime.now()
    heartbit='id=73263211&serializeSco={"res01":{"lesson_location":2457,"session_time":30,"last_learn_time":"_TTT_"},"last_study_sco":"res01"}&duration=30&study_course=b0fef2ffad3f44688b0d7961174a4aa7'
    heartbit=heartbit.replace('_TTT_',f'{t.year}-{t.month}-{t.day} -{t.hour}:{t.minute}:{t.second}')
    heartbit=sf.CharF.str2Dir(heartbit,'&','=')
    heartbit['id'] = f'{slist[0][1]}'
    
    playurl=f'https://www.samrela.com/portal/getManifest.do?id={slist[0][2]}&is_gkk=false&_=1698731660834'
    # print(playurl)
    try:
        ses.get(playurl,cookies=cookies,timeout=0.1)
    except:
        # print('time out_p.')
        pass
    try:
        ses.post(urlheartbit,data=heartbit,cookies=cookies,headers=header,timeout=1)
    except:
        print('time out_u.')

    # print('=',end=' ')
    
    time.sleep(0.1)
    if icont%5==0:
        slist=flash_list()
    icont+=1
    
    

