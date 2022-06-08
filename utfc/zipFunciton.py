import string
import zipfile, os
import hashlib
from zlib import crc32
import tqdm
def unzip(zipname):
    while True:
        passwd = zipname.split('.')[0]
        zf = zipfile.ZipFile(zipname, 'r')
        zf.extractall(pwd=passwd.encode())
        zipname = zf.namelist()[0]
        zf.close()

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
            print(i.filename,i.file_size,hex(i.CRC),i.date_time)
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