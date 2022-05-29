# -*- coding:utf-8 -*
import socket
import threading
import sys, getopt
## 这个代码是用来做端口转发的 emmm 你问有什么用？没用，删了他吧 (摊手
# 错误
def l_w(s):
    print("[!] {}".format(s))
# 信息
def l_i(s):
    print("[+] {}".format(s))
# 毁灭性错误
def l_a(s):
    print("[-] {}".format(s))
    exit()
def help():
    print("""
      -h 提供帮助，就是你看到的这个
      -s 指定监听的本地ip，默认为 127.0.0.1
      -l 指定监听的端口号，必须指定
      -d 指定转发的目的主机，默认为 127.0.0.1
      -p 指定转发的目的端口，必须指定

         本程序具有超级牛力！ moo~~ moo~~~
   """)
    exit()
s_host = "127.0.0.1"
s_port = 0
d_host = "127.0.0.1"
d_port = 0
# 将来自s套接字的数据转发到d套接字(函数名 forward)
def fw(s, d):
    try:
        while True:
            buf = s.recv(4096)
            l_i("{} ====> {} {} 字节".format(s.getpeername(), d.getpeername(), len(buf)))
            if (len(buf) == 0):
                l_w("{} 断开连接".format(s.getpeername()))
                return
            d.send(buf)
    except:
        return
# 处理请求，每一个连接对应一个 (函数名 request thread)
def rt(request_socket):
    des_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        des_socket.connect((d_host, int(d_port)))
    except Exception as e:
        l_a("连接目标 {}:{} 失败！err: {}".format(d_host, d_port, str(e)))
    threading.Thread(target=fw, args=(request_socket, des_socket)).start()
    fw(des_socket, request_socket)
# 获取参数
try:
    opts, args = getopt.getopt(sys.argv[1:], "hs:l:d:p:")
except getopt.GetoptError:
    l_w("参数不正确")
    help()
for opt, arg in opts:
    if opt == '-h':
        help()
    elif opt == '-s':
        s_host = arg
    elif opt == '-l':
        s_port = arg
    elif opt == '-d':
        d_host = arg
    elif opt == '-p':
        d_port = arg
if s_host == "127.0.0.1":
    l_w("将会监听: 127.0.0.1")  # 因为可能你不想绑定 127.0.0.1 所以作出提示 (也许是0.0.0.0呢)
if s_port == 0 or d_port == 0:
    l_a("没有指定端口号或指定为0 通过 -h 参数看帮助")
l_i("监听 {}:{}".format(s_host, s_port))
l_i("将会连接 {}:{}".format(d_host, d_port))
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_socket.bind((s_host, int(s_port)))
except Exception as e:
    l_a("绑定 {}:{} 端口失败 {}".format(s_host, s_port, str(e)))
server_socket.listen(50)  # 应该同时连接不会超过 50 个吧...
l_i("准备就绪")
while True:
    request_socket, addr = server_socket.accept()
    l_i("{} 已连接".format(request_socket.getpeername()))
    threading.Thread(target=rt, args=(request_socket,)).start()
