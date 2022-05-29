from subprocess import *
import time


class cmdF:
    cmd = ''

    def __init__(self, c=''):
        self.cmd = c

    def runScript(self, cmdL=[], sl=0.1):
        with  Popen(self.cmd, shell=True, stdin=PIPE, stdout=PIPE) as p:
            for i in cmdL:
                time.sleep(sl)
                p.stdin.write(bytes((i + '\n'), 'utf-8'))
            time.sleep(sl)


import paramiko
def ssh2(ip,username,passwd,cmd,port=22):
    out=''
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,port,username,passwd,timeout=5)
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m)
            out = stdout.readlines()
            for i in (out):
                print(i,end='')
        ssh.close()
    except :
        print ('[ ]%s'%(ip) )
    return out

def changepass(Ip,user,old_password,new_password):
    # 建立一个sshclient对象
    ssh = paramiko.SSHClient()
    # 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 调用connect方法连接服务器
    #如果远程执行命令错误信息是b'the input device is not a TTY\n' 去掉docker exec -it 中的t就好了
    try:
        ssh.connect(hostname=Ip, port=22, username=user, password=old_password,timeout=5)
        #ubuntu修改密码两种方法
        #方法一
        # command1 = "echo '%s:%s' | chpasswd"%(user,new_password)
        # stdin, stdout, stderr = ssh.exec_command(command1)
        # out, err = stdout.read(), stderr.read()
        # if err != '':
        #     print(err)
        #
        # else:
        #     print(out)
        # # 关闭连接
        # ssh.close()
        #方法二
        command = "passwd %s" %(user)
        stdin, stdout, stderr = ssh.exec_command(command)
        #\n模拟回车 输两次密码
        stdin.write(old_password+'\n'+new_password + '\n' + new_password + '\n')
        out, err = stdout.read(), stderr.read()
        print(out,err)
        # 关闭连接
        ssh.close()
    except paramiko.ssh_exception.AuthenticationException as e:
        print(Ip + ' ' + '\033[31m账号密码错误!\033[0m')
        with open('nossh.txt','a') as f:
            f.write(Ip + '\n')
    except :
        print(Ip + ' ' + '\033[31m连接超时！\033[0m')
        with open('timeoutssh','a') as f:
            f.write(Ip + '\n')
