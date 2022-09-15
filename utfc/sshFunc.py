import paramiko as sshc
import time
class SSH:
    def __init__(self, ip, un, pwd, port=22):
        self.ip = ip
        self.un = un
        self.pwd = pwd
        self.port = port
        self.Client = sshc.SSHClient()
        self.Client.set_missing_host_key_policy(sshc.AutoAddPolicy())
        self.Client.connect(self.ip, self.port, self.un, self.pwd)
        self.channel = self.Client.get_transport().open_session()
        self.channel.get_pty()
        self.channel.invoke_shell()

    def __del__(self):
        try:
            self.channel.close()
            self.Client.close()
        except:
            pass

    def run(self, cmd=''):
        rt = b''
        try:
            si, so, se = self.Client.exec_command(cmd)
            rt += so.read() + se.read()
        except:
            rt += b''
        return rt.decode()

    def send(self, cmd='', waitfor=''):
        if not cmd.strip().endswith('\r'):
            cmd += '\r'
        self.channel.send(cmd)
        ret = b''
        for i in range(50):
            time.sleep(0.2)
            ret += self.channel.recv(1024*3)
            if waitfor in ret:
                return ret.decode()
        return ret.decode()

    def sendList(self, cmdList=[]):
        ret = ''
        for i in cmdList:
            if isinstance(i, tuple):
                ret += self.send(i[0], i[1])
            else:
                ret += self.send(i)
        return ret
