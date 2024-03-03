import hashlib
import re
class fstr(str):
    def __new__(cls,strin,o: object = ...):
        if isinstance(strin,bytes):
            try:
                strin = strin.decode()
            except:
                pass
        return super().__new__(cls,strin)
        
    def re(self,strfind,flag=re.IGNORECASE+re.M):
        return re.findall(strfind,self,flag)
    

        



if __name__ == "__main__":
    a = fstr('''123456789
    fff
    265''') 
 
    print(a.re(r'(2\d+5)'))
    print(a)
 

    pass

