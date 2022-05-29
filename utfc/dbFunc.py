import pymysql

class MySqlFunc:
    def __init__(self,h = 'localhost',u= 'root',p = "123456",d = "test", port = 3306,charset = 'utf8mb4'):
        self.host=h
        self.user=u
        self.password=p
        self.database = d
        self.port=port
        self.charset=charset
        self.db =pymysql.connect(host=self.host,user = self.user,password=self.password,database=self.database,port=self.port,charset = self.charset)
        print(self.db)
    def select(self,sql=['select 1'],ptr=False,cw=5):
        with self.db.cursor() as cursor:
            try:
                if isinstance(sql,list):
                    for i in sql:
                        cursor.execute(i)
                else:
                    cursor.execute(sql)
                data = cursor.fetchall()
                if(ptr):
                    title = [i[0] for i in cursor.description]
                    w = [cw for i in title]
                    for i in data:
                        for j in range(len(i)):
                            t = str(i[j])
                            if len(t)>w[j] :
                                w[j] = len(str(i[j]))
                    f_str=''
                    for i in w:
                        f_str += '| {:%d} '%(i)
                    print(len(data), ' rows')
                    titles = f_str.format(*title)
                    print('- '*(len(titles)//2))
                    print(titles)
                    print('- ' *(len(titles)//2))
                    for i in data:
                        print(f_str.format(*i).replace('\n',''))
                    print('- '*(len(titles)//2))
                    print(len(data),' rows')
            except Exception as e:
                print(e.args)
                return (e.args)
            return data
    def run(self, sql=['select 1']):
        with self.db.cursor() as cursor:
            try:
                if isinstance(sql, list):
                    for i in sql:
                        cursor.execute(i)
                else:
                    cursor.execute(sql)
                self.db.commit()
            except Exception as e:
                print(e.args)
                return False,e.args
            return True,cursor.rowcount
    def __del__(self):
        self.db.close()
# db = MySqlFunc(u='regx',p='regx00',d='regx')
# a =db.select('''select mid(ul,1,35), des  from usx  where des like '%flag%' ''',ptr=True,cw=35)