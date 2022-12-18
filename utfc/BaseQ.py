from utfc.StrFunc import *
import base91
import base64
import base58
import math
import libnum
import utfc.base92 as base92
'''---------------------------------------------
    Base全家桶--残次品，92以上跑着有问题
---------------------------------------------'''
class BaseQ:
    defTable = {
        '16': b'0123456789ABCDEF',
        '32': b'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
        '36': b'0123456789abcdefghijklmnopqrstuvwxyz',
        '58': b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz',
        '58b': b'rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz',
        '62':  b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
        '62a': b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        '62b': b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        '62c': b"abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        '62d': b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',
        '62e': b'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz',

        '64' : b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/',
        '85' : b'!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstu',
        '85b': br'!"#$%&()*+-./0123456789:<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^abcdefghijklmnopqrstuvwxyz{}',
        '85z': b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.\\-:+=^!/*?&<>()[]{}@%$#',
        '85v6':br'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+\-;<=>?@^_`{|}~',
        '91': br'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~"',
        '92': br"!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_abcdefghijklmnopqrstuvwxyz{|}",
        '128': b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\xb5\xb6\xb7\xbc\xbd\xbe\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff',
        'r16': b'FEDCBA9876543210',
        'r32': b'765432ZYXWVUTSRQPONMLKJIHGFEDCBA',
        'r36': b'zyxwvutsrqponmlkjihgfedcba9876543210',
        'r58': b'zyxwvutsrqponmkjihgfedcbaZYXWVUTSRQPNMLKJHGFEDCBA987654321',
        'r62': b'zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA9876543210',
        'r62b': b'9876543210ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba',
        'r64': b'/+9876543210zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA',
        'r85': b'utsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)(\'&%$#"!',
        'r85b': b'}{zyxwvutsrqponmlkjihgfedcba^][ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<:9876543210/.-+*)(&%$#!',
        'r85c': b'~}|{`_^@?>=<;-+*)(&%$#!zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA9876543210',
        'r91': b'"~}|{`_^][@?>=<;:/.,+*)(&%$#!9876543210zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA',
        'r92': b"}|{zyxwvutsrqponmlkjihgfedcba_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)('&%$#!",
        'r128': b'\xff\xfe\xfd\xfc\xfb\xfa\xf9\xf8\xf7\xf6\xf5\xf4\xf3\xf2\xf1\xef\xee\xed\xec\xeb\xea\xe9\xe8\xe7\xe6\xe5\xe4\xe3\xe2\xe1\xdf\xde\xdd\xdc\xdb\xda\xd9\xd8\xd7\xd6\xd5\xd4\xd3\xd2\xd1\xcf\xce\xcd\xcc\xcb\xca\xc9\xc8\xc7\xc6\xc5\xc4\xc3\xc2\xc1\xbe\xbd\xbc\xb7\xb6\xb5zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA9876543210',

    }
    
    @staticmethod
    def short_div(i=65537,b=16):
        if isinstance(i,bytearray) : i = i.decode()
        if isinstance(i,str) : i = libnum.s2n(i)
        retarr=[]
        while i >0:
            retarr.append(i%b)
            i//=b
        return retarr[::-1]

    @staticmethod
    def Dc(txt=''):
        reta = []
        retb = []
        i=b''
        for i in BaseQ.defTable:
            c = BaseQ.decode(txt, i)
            for i in c[0]:
                reta.append(bytes(i, 'utf-8'))
                retb.append(c[1][0])
        return [reta, retb]

    @staticmethod
    def decode(txt='', tab='', base=None):
        if '62' in tab: #有个网站不知道为啥给base62分段了，好多题都是用这个网站出的，也就只能这样了
                        #后来有无良大佬，直接搞了个不管多少都分段的。。。凑合着用吧。
            retb = b''
            reta = []
            for fd in (11,len(txt)):
                rtmp=f'{fd}->|'
                for ct in range(0,len(txt),fd):
                    a,retb = BaseQ._decode(txt[ct:ct+fd], tab, base=None)
                    rtmp += a[0]
                reta.append(rtmp)
            return [reta,retb]
        else:
            return BaseQ._decode(txt, tab, base)
    @staticmethod
    def _decode(txt='', tab='', base=None):
        txt = list(txt.encode())
        if isinstance(tab, bytes):
            tab = tab.encode()
        if base != None and len(tab) < base:
            tab += '=' * (base - len(tab))
        elif base != None and len(tab) > base:
            tab = tab[:base]
        ret = []
        alpha = tab
        if tab not in BaseQ.defTable: tab = 'UserDef'
        if (alpha.lower() in BaseQ.defTable): alpha = BaseQ.defTable[alpha.lower()]
        # 码长
        if isinstance(alpha,str):
            alpha = alpha.encode()
        alpha =list(alpha)

        clong = len(alpha)
        pr = 1
        bigint = 0
        rev = txt[::-1]
        for i in rev:
            try:
                iv = alpha.index(i)
            except:
                iv = 0
            bigint = bigint + iv * pr
            pr *= clong
        st = str(bin(bigint))[2:]
        st = '0' * (8 - len(st) % 8) + st
        ret = CharF.num2str(st, bs=2, spl=8)
        return [[ret], ['Base:' + tab]]

    @staticmethod
    def DcTW(fn):
        c = ''
        with open(fn, 'r') as f:
            c = f.read()
        BaseQ.DcStrQJT(c)

    @staticmethod
    def DcStrQJT(in_c='',findflag=['flag','ctf'],fromb='|'):
        def base91dec(str_in):
            ret =  base91.decode(str_in).decode()
            return ret

        def dec(in_c,fc):
            for padding in range(6):

                try:
                    return fc(in_c.decode())
                except:
                    try:
                       return fc(in_c)
                    except:
                        pass
                if isinstance(in_c,bytes):
                    in_c = (in_c.decode() + '=').encode()
                else:
                    in_c +='='
            return False
        base = [base64.b16decode,base92.base92_decode, base64.b16decode, base64.b32decode, base58.b58decode, base64.b85decode, base91dec,base64.b64decode]
        base = [base64.b16decode,base92.base92_decode, base64.b32decode, base58.b58decode, base64.b85decode, base91dec,base64.b64decode]
        for i in base:
            try :

                enc = dec(in_c,i)
                c = enc
                if enc==False: continue
                path = fromb + '->' + i.__name__+'|'
                try:
                    enc=enc.decode()
                except:pass
                if (len(enc) > 1):
                    for x in findflag:
                        if x in enc:
                            printc(path+enc, cmd_color.light_green)
                            break;
                    else:
                        if enc.isprintable():
                            printc(path + enc, cmd_color.yellow)
                        print(path, enc)
                    BaseQ.DcStrQJT(c, fromb=path)
            except: pass

if __name__ == "__main__":
    print(BaseQ.Dc(''))
    pass
