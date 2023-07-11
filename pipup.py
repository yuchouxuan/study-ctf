
import os
def up(mn=0,ilist=['NoName_______']):
    mirr=[
        '',
        '-i https://mirror.baidu.com/pypi/simple ',
        '-i https://pypi.mirrors.ustc.edu.cn/simple',
        ]

    m=mirr[mn]

    pipl = os.popen('pip list --outdate '+m).readlines()[2:]
    print(f'OUTDATE: {len(pipl)}')
    print('- '*40)
    list(map(lambda x:print(x.replace('\n','')),pipl))
    print('- '*40)
    for i in pipl :
        for ing in ilist:
            if ing in i :
                continue
        wname=i.split()[0]
        print('- '*(len(wname)//2+2))
        print(f' {wname}')
        print('- '*40) 
        cmd = f'pip3 install {wname} -U  '+m
        os.system(cmd)
        print('\n\n')


    
