import string
import zipfile, os
from zlib import crc32
import tqdm
def unzip(zipname):
    while True:
        passwd = zipname.split('.')[0]
        zf = zipfile.ZipFile(zipname, 'r')
        zf.extractall(pwd=passwd.encode())
        zipname = zf.namelist()[0]
        zf.close()
import tqdm
class zipF (zipfile.ZipFile):
    fn=""
    pwd=None
    flist=[]
    def __init__(self,fn:str ,pws=None):
        super().__init__(fn,'r')
        self.fn=fn
        self.pwd=pws
        for  i in self.filelist:
            self.flist.append(i.filename)
            print(i.filename,i.file_size,hex(i.CRC),i.date_time,end=" | ")
            # print(,,hex(self.NameToInfo[i].CRC))
    def unzip(self,fn:str,pwd=None,ofn:str=None):
        if pwd==None: pwd=self.pwd
        if isinstance(pwd,str) :pwd=pwd.encode()
        if ofn!=None:
            with open(ofn,'wb') as f:
                f.write(self.read(fn,pwd))
        return self.read(fn,pwd)
    def crc(self,fn,ab=string.printable):
        if isinstance(ab,str):
            ab = ab.encode()
        if isinstance(ab,list) and isinstance(ab[0],str) :
            ab=[x.encode() for x in ab]
        crc = self.NameToInfo[fn].CRC
        counter = len(ab) ** self.NameToInfo[fn].file_size
        for i in tqdm.trange(counter):
            trying=[]
            k = i
            for j in range(self.NameToInfo[fn].file_size):
                trying.append(ab[k%len(ab)])
                k=k//len(ab)
            crct = crc32(bytes(trying))
            if crct==crc :
                return  bytes(trying)
            
    def crcall(self,ab=string.printable,maxl=6 ):
        if isinstance(ab,str):
            ab = ab.encode()
        if isinstance(ab,list) and isinstance(ab[0],str) :
            ab=[x.encode() for x in ab]
        fn = [f for f in  self.NameToInfo]
        crcl = [self.NameToInfo[f].CRC for f in fn]
        counter = len(ab) **maxl
        find=0
        for i in tqdm.trange(counter):
            trying=[]
            k = i
            for j in range(maxl):
                trying.append(ab[k%len(ab)])
                k=k//len(ab)
            crct = crc32(bytes(trying))
            if crct in crcl :
                print(fn[crcl.index(crct)], bytes(trying) )
                find+=1
                if find >=len(fn):
                    return 
                
        
        

# 彩虹表模式，四位的，3位用不着，5位内存吃不太消~~
# tab默认是b64码表~~~,有些莫名其妙的bug，回头改~
import utfc.BaseQ as baseq
def rt_crc_4b(zip,fn=[],tab=None):
    if tab is None:
        tab = baseq.BaseQ.defTable['64'].decode() +"="
    if isinstance(tab,bytes):
        tab =tab.decode()
    xf = zipF(zip)
    rainbow = {}
    for i in tqdm.tqdm(tab):
        for j in tab:
            for q in tab:
                for k in tab:
                    x = i + j + q + k
                    rainbow[crc32(x.encode())] = x
    bc = ''
    for i in fn:
        try:
            fcrc = xf.NameToInfo[i].CRC
            print(i, fcrc, '->', rainbow[fcrc], end='|')
            bc += rainbow[fcrc]
        except:
            print(i, fcrc, '->','ERROR', end='|')
    return bc


def rt_crc_6b(zip,fn=[],tab='0123456789abcdef\n'):
    if isinstance(tab,bytes):
        tab =tab.decode()
    xf = zipF(zip)
    rainbow = {}
    for i in tqdm.tqdm(tab):
        for j in tab:
            for q in tab:
                for k in tab:
                     for l in tab:
                          for m in tab:
                                x = i + j + q + k+l+m
                                rainbow[crc32(x.encode())] = x
    bc = ''
    for i in fn:
        try:
            fcrc = xf.NameToInfo[i].CRC
            print(i, fcrc, '->', rainbow[fcrc], end='|')
            bc += rainbow[fcrc]
        except:
            print(i, fcrc, '->','ERROR', end='|')
    return bc