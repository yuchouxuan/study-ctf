'''
来源字Y4大佬
'''
from PIL import Image
import itertools
import utfc.StrFunc as sf
import utfc.StaticValue as stv
import zlib
def get_file_ext(file_bin):
    result=''
    for i in stv.file_ext_dict.keys():
        if len(file_bin)>=len(i):
            if file_bin[:len(i)]==i:
                result+=stv.file_ext_dict[i]['Extension']+' file! Description:'+stv.file_ext_dict[i]['Description']+'; '
    return result

def int2bytes(num):
    s=str(bin(num))[2:]
    s='0'*(8-len(s))+s
    return(s)
def rgba2bytes(bytes_arr,plane,bit_order):
    ori_bit=''
    plane=plane.lower().replace('r','0').replace('g','1').replace('b','2').replace('a','3')
    for i in plane:
        for j in bit_order:
            ori_bit+=int2bytes(bytes_arr[int(i)])[7-int(j)]
    return(ori_bit)

def binstr2bytes(binstr,_type):
    output=b''
    for i in range(int(len(binstr)/8)):
        if _type=='lsb':
            output+=int(binstr[8*i:8*i+8],2).to_bytes(1,byteorder='big')
        else:
            b=binstr[8*i:8*i+8]
            output+=int(b[::-1],2).to_bytes(1,byteorder='big')
    return(output)

'''
源图片-ori_pic，输入图片文件名
写入字节位 -order,字符串类型'01234567',有多位时按排列顺序决定写入顺序
例如'7532'相当于Stegsolve中选择7 5 3 2位和MSBFirst，也相当于zsteg的 -b 10101100
例如'0124'相当于Stegsolve中选择4 2 1 0位和LSBFirst（zsteg不支持LSBFirst）
支持‘1024’这种字节位乱序读取的方式，但Stegsolve和zsteg里没有对应选项或参数
写入通道-plane：字符串类型，大写，默认写入RGB通道，按排列顺序决定写入顺序
写入时的顺序是先通道，再字节，即一个通道的所有字节位写完再写下一个通道，所有通道写完再写下一个像素
不支持每个通道写入字节位不同的情况（Stegsolve是支持的，但不常用）
坐标读取顺序-axis：默认行优先-x，列优先-y，其他包含倒序的请通过提前翻转源图片实现
写入模式 -_type,支持lsb和msb模式，默认每8bit从前往后读取-lsb，从后往前读-msb，Stegsolve仅支持lsb
是否全读取 -full，默认只读取首行
'''
def decodelsb(ori_pic,order,plane='RGB',axis='x',_type='lsb',full=0):
    img_src=Image.open(ori_pic)
    w, h, m = img_src.size[0], img_src.size[1], img_src.mode
    str_strlist = img_src.load()
    output=''
    if full==0:
        if axis=='x':
            h=1
        else:
            w=1
    if axis=='x':
        for j in range(h):
            for i in range(w):
                output=output+rgba2bytes(bytes_arr=str_strlist[i,j],plane=plane,bit_order=order)
    if axis=='y':
        for i in range(w):
            for j in range(h):
                output=output+rgba2bytes(bytes_arr=str_strlist[i,j],plane=plane,bit_order=order)
    return(binstr2bytes(output,_type=_type))
def num2order(num):
    return ''.join([str(i) for i in range(8) if int2bytes(num)[::-1][i]=='1'])

def exp(fn,bits="0123",channel="RGB",axises='x',_type='lsb',full=0,):
    tempfn=''
    for i in range(1,len(fn)):
        if fn[-i] == '/' or fn[-i] == '\\':
            tempfn = fn[:-i]+'/tmp.xyz'
            break
    d = decodelsb(ori_pic=fn, order=''.join(bits), plane=''.join(channel), axis=axises, _type=_type,full=full)
    with open(tempfn,'wb') as f:
        f.write(d)
        sf.printc('[+] FileOUT -> '+tempfn, sf.cmd_color.green)



def myb(fn,bits="0123",channel="RGB",axises='xy',full=0):
    for i in range(1,len(fn)):
        if fn[-i] == '/' or fn[-i] == '\\':
            tempfn = fn[:-i]+'/tmp'
            break
    bord = []
    if isinstance(bits,int):
        for i in range(bits) :
            bord.append(num2order(i))
            bord.append(num2order(i)[::-1])
    elif isinstance(bits,str):
        bord = itertools.permutations(bits)
    for order in bord:
        for plane in itertools.permutations(channel.upper()):
            for axis in axises:
                    for type in ['msb','lsb']:
                        d = decodelsb(ori_pic=fn, order=''.join(order), plane=''.join(plane), axis=axis, _type=type,full=full)
                        guess = get_file_ext(d)
                        if len(guess) > 2:
                            print('- '*80)
                            print('[-]', ''.join(order), ''.join(plane), axis, type,'|',guess)
                            print(d[:80])
                        if b"ctf" in d or b'flag' in d or b'CTF' in d:
                            sf.printc('[+] FIND -> '+str(d),sf.cmd_color.green)
                        if "Zlib compressed data" in guess:
                            try:
                                print(zlib.decompress(d))
                                sf.printc('[+] FIND -> '+zlib.decompress(d).decode(), sf.cmd_color.green)
                            except:
                                pass
                        if ".ZIP file" in guess:
                            try:
                                with open(tempfn+'.zip', 'wb') as f:
                                    f.write(d)
                                sf.printc('[+] FileOUT -> '+tempfn+'.zip', sf.cmd_color.green)
                            except:
                                pass
                        if ".PNG file" in guess:
                            try:
                                with open(tempfn+'.zip', 'wb') as f:
                                    f.write(d)
                                sf.printc('[+] FileOUT -> '+tempfn+'.png', sf.cmd_color.green)
                            except:
                                pass


