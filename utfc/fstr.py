import hashlib
from urllib import parse
import re
import base64 
class cmd_color:
    none = "\033[0m"
    rev = '\033[7m'
    black = "\033[0;30m"
    dark_gray = "\033[1;30m"
    blue = "\033[0;34m"
    light_blue = "\033[1;34m"
    green = "\033[0;32m"
    light_green = "\033[1;32m"
    cyan = "\033[0;36m"
    light_cyan = "\033[1;36m"
    red = "\033[0;31m"
    light_red = "\033[1;31m"
    purple = "\033[0;35m"
    light_purple = "\033[1;35m"
    brown = "\033[0;33m"
    yellow = "\033[1;33m"
    light_gray = "\033[0;37m"
    white = "\033[1;37m"

def printc(s, color=cmd_color.none, end='\n'):
    print(strcolor(s, color), end=end)
def strcolor(s, color=cmd_color.none):
    return color + s + cmd_color.none

class fstr(str):

    @staticmethod 
    def randRegX(rt = 'B+v*'):
        '''生成随机符合正则的字符串'''
        ret = rstr.xeger(rt)
        print('- '*30)
        print('RandRSt:', ret)
        print('- ' * 30)
        return ret
    
    def BinMath(op1, op2 = b'\x50\x4b\x03\x04', op='^'):
        '''位运算'''
        if isinstance(op2,str):
            op2=op2.encode()
        if len(op1) ==0:
            return fstr('')
        if len(op2)==0:
            return op1
        op1=op1.encode()
        bout = []
        for i in range(0, len(op1), len(op2)):
            for j in range(len(op2)):
                try:
                    o = f'op1[i+j]{op}op2[j]'
                    x = eval(o)
                    bout.append(x)
                except:
                    pass
        try :
            return fstr(bytes(bout).decode())
        except:
            return bytes(bout)

    def __xor__(self,right):
        return self.BinMath(right)

    def __and__(self,right):
        return self.BinMath(right,'&')

    def __or__(self,right):
        return self.BinMath(right,'|')

    def base(self,encoder=None):
        '''打base
        bFunc:encode函数,如base64.b58encode'''
        if encoder==None:
            encoder=base64.b64encode
        return fstr(encoder(self.encode()))
    
    @staticmethod
    def frombase(strin,decode=None):
        '''解base
        bFunc:encode函数,如base64.b58encode'''
        if decode==None:
            decode=base64.b64decode
        bout=decode(strin)
        try:
            return fstr(bout.decode())
        except:
            return bout

    def url(self,force=False,cs='utf-8'):
        '''url编码,force=True时,强制对所有字符编码'''
        ret =''
        if force:
             for i in self.encode(cs):
                ret+='%%%x'%i
        else:
            ret =  parse.quote(self,encoding=cs)           
        return fstr(ret.upper())

    @staticmethod
    def fromurl(url):
        '''url解码'''
        return fstr(parse.unquote(url))

    @staticmethod
    def __new__(cls,strin,o: object = ...):
        if isinstance(strin,bytes):
            try:
                strin = strin.decode()
            except:
                printc('[*]Byte->Str,decode Error',cmd_color.red)
        return super().__new__(cls,strin)
        
    def re(self,strfind,only1=True,flag=re.IGNORECASE+re.M):
        """正则-findall
        only1=True 时返回第一个匹配项
        无匹配返回None"""
        ret =  re.findall(strfind,self,flag)
        if len(ret) == 0:
            return None
        if only1:
            return ret[0]
        return ret
    
    def hex(self):
        """转16进制"""
        return ''.join(['{:02x}'.format(ord(c)) for c in self])

    def hex_c(strin, mask='\\x'):
        """转16进制_c格式"""
        return fstr(''.join([mask+'{:02x}'.format(ord(c)) for c in strin]))
    
    def charRange(st='a',end='z'):
        if isinstance(st, str): st = ord(st)
        if isinstance(end, str): end = ord(end)
        return fstr('',join([chr(i) for i in range(st, end + 1)]))
    
    def haveAny(self,sfind) -> bool:
        '''包含任意'''
        if isinstance(sfind,str):
            return sfind in self 
        elif isinstance(sfind,bytes):
            return sfind in self.encode() 
        elif isinstance(sfind,(set,list,tuple)) :
            for i in sfind:
                if self.haveAny(i) :
                    return True 
            return False 
        elif isinstance(sfind,dict):
            for v in sfind.values():
                if self.haveAny(v) :
                    return True 
            return False 
        return False 

    def haveAll(self,sfind)->bool:
        '''包含所有'''
        if isinstance(sfind,str):
            return sfind in self 
        elif isinstance(sfind,bytes):
            return sfind in self.encode() 
        elif isinstance(sfind,(set,list,tuple)) :
            for i in sfind:
                if not self.haveAll(i) :
                    return False 
            return True 
        elif isinstance(sfind,dict):
            for v in sfind.values():
                if not self.haveAll(v) :
                    return False 
            return True 
        return False 

    def fullChar(self):
        """半角字符转全角"""
        full = ''
        for ch in self:
            if ord(ch) in range(33, 127):
                ch = chr(ord(ch) + 0xfee0)
            elif ord(ch) == 32:
                ch = chr(0x3000)
            else:
                pass
            full += ch
        return full 
    
    def toHeader(self,splitby=['\n',':'],delspace=True)->dict:
        """字符串转字典,用于构造requests请求头和cookie,
        delspace用于清理没用的头尾空格"""
        ret ={}
        for i in self.split(splitby[0]) :
            if delspace:
                i=i.strip()
            if len(i) > 0:
                if splitby[1] in i :
                    k = i[:i.index(splitby[1])]
                    v = i[i.index(splitby[1])+1:]
                    if delspace:
                        k=k.strip()
                        v=v.strip()
                    ret[k]=v
                else :
                    ret[i]=''
        return ret
 
    @staticmethod
    def read(fn,cs='utf-8') :
        """直接从文件中读取字符串"""
        with open(fn,'rb') as f:
            s = f.read()
            try:
                s.decode(cs)
            except:
                printc('[-]ERR:can decode by'+cs,cmd_color.red)
                pass 
        return fstr(s)
    
    def write(self,fn,openFlag='w'):
        with open(fn,openFlag) as f :
            return f.write(self)

    def __getitem__(self,i):
        if isinstance(i,int):
            i%=len(self)
        return super().__getitem__(i)
        
    def replaceloop(self,s:str,d:str):
        if s == '':
            return fstr('')  
        ret = self
        while ret.find(s)>=0:
            ret = ret.replace(s,d)
        return ret
 
if __name__ == "__main__":
    a = fstr('flaaaaaaaag啊')
    print(a.replaceloop('laa','l')) 



 

    pass

