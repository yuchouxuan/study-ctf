import cv2 as cv
import numpy as np
import struct
import binascii
from PIL import Image, ImageDraw, ImageFont
import pyzbar.pyzbar as pyzbar
import imageio
import matplotlib.pyplot as plt

import tqdm
import zlib
import re
import utfc.os_lsb as os_lsb
from utfc.lsb_decode import *

'''opencv 其他常用函数
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
画圆:
cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
        img：要画的圆所在的矩形或图像
        center：圆心坐标，如 (100, 100)
        radius：半径，如 10
        color：圆边框颜色，如 (0, 0, 255) 红色，BGR
        thickness：正值表示圆边框宽度. 负值表示画一个填充圆形
        lineType：圆边框线型，可为 0，4，8
        shift：圆心坐标和半径的小数点位数
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
画线
:cv2.line(img, pt1, pt2, color[, thickness[, lineType[, shift]]])
        img：要画的圆所在的矩形或图像
        pt1：直线起点
        pt2：直线终点
        color：线条颜色，如 (0, 0, 255) 红色，BGR
        thickness：线条宽度
        lineType：
        - 8 (or omitted) ： 8-connected line
        - 4：4-connected line
        - CV_AA - antialiased line
        shift：坐标点小数点位数
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
画方块
cv2.rectangle(img, pt1, pt2, color[, thickness[, lineType[, shift]]]) 
        mg：要画的圆所在的矩形或图像
        pt1：矩形左上角的点
        pt2：矩形右下角的点
        color：线条颜色，如 (0, 0, 255) 红色，BGR
        thickness：线条宽度
        lineType：
        8 (or omitted) ： 8-connected line
        4：4-connected line
        CV_AA - antialiased line
        shift：坐标点小数点位数
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
画椭圆  
cv2.ellipse(img, center, axes, rotateAngle, startAngle, endAngle, color[, thickness[, lineType[, shift]]]) 
        img：要画的圆所在的矩形或图像
        center：椭圆的中心点
        axes：椭圆的长半轴和短半轴的大小
        rotateAngle：椭圆的旋转角度
        startAngle：椭圆弧的起始角度
        endAngle：椭圆弧的终止角度
        color：线条颜色，如 (0, 0, 255) 红色，BGR
        thickness：线条宽度
        lineType：
        8 (or omitted) ： 8-connected line
        4：4-connected line
        CV_AA - antialiased line
        shift：坐标点小数点位数
'''

import exifread
class imgBase:
    img = None
    fn = ''
    height = 0
    weight = 0
    channels = 0

    def __init__(self, fn=None, w=100, h=100):
        if fn == None:
            self.fn = 'Temp'
            self.createImage(w, h)
            return
        try:
            try :
                with open(fn,'rb') as f:
                    w = exifread.process_file(f)
                    for i in w:
                        print(i,'\t',w[i])
                    f.close()
            except: pass

            self.img = cv.imread(fn)
            self.fn = fn
            self.height = self.img.shape[0]
            self.weight = self.img.shape[1]
            self.channels = self.img.shape[2]
            print(fn, self.weight, self.height, self.channels)
        except:
            pass

    def zbar(self):
        code = ''
        try:
            code = pyzbar.decode(self.img)
            code = code[0][0]
        except:
            pass
        return code

    def show(self, wname='image'):
        cv.imshow(wname, self.img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def getxy(self, x=0, y=0):
        height = self.img.shape[0]
        weight = self.img.shape[1]
        channels = self.img.shape[2]
        if x < 0: x = -x
        if y < 0: y = -y
        ret = []
        for c in range(channels):
            ret.append(self.img[y % height, x % weight, c])
        return ret

    def setxy(self, x=0, y=0, col=[0, 0, 0]):
        height = self.img.shape[0]
        weight = self.img.shape[1]
        if x < 0: x = -x
        if y < 0: y = -y
        self.img[y % height, x % weight] = col


    def drawtext(self, text='', x=0, y=0, size=18, col=(0, 0, 0)):
        img = Image.fromarray(cv.cvtColor(self.img, cv.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        fontStyle = ImageFont.truetype("font/simsun.ttc", size, encoding="utf-8")
        draw.text((x, y), text, col, font=fontStyle)
        self.img = cv.cvtColor(np.asarray(img), cv.COLOR_RGB2BGR)


    def createImage(self, w=100, h=100):
        self.weight = w
        self.height = h
        self.img = np.zeros((h, w, 3), np.uint8)
        self.img.fill(255)


    def rev(self):  # 负片
        for x in tqdm.trange(self.weight):
            for y in range(self.height):
                c = self.getxy(x, y)
                self.setxy(x, y, [~c[0], ~c[1], ~c[2]])


    def drawHist(self, line=''):  # 直方图
        b, g, r = cv.split(self.img)
        hists, bins = np.histogram(b.flatten(), 256, [0, 256])
        plt.plot(hists, line + 'b')
        hists, bins = np.histogram(g.flatten(), 256, [0, 256])
        plt.plot(hists, line + 'g')
        hists, bins = np.histogram(r.flatten(), 256, [0, 256])
        plt.plot(hists, line + 'r')

    def save(this, fn=''):
        if fn == '': fn = this.fn
        cv.imwrite(fn, this.img)


class PicQP(imgBase):  # 棋盘绘图，二维码用
    w = 600
    dw = 60

    def __init__(self, w=600, dw=30):
        self.w = w
        self.dw = dw
        self.img = np.zeros((w + 1, w + 1, 3), np.uint8)
        self.img.fill(255)

    def show(self):
        cv.imshow('image', self.img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def drawBox(self, pos=(0, 0), col=(128, 128, 128)):
        x0 = int(self.dw * pos[0])
        y0 = int(self.dw * pos[1])
        cv.rectangle(self.img, (x0, y0), (x0 + self.dw, y0 + self.dw), col, -1, 0)

    @staticmethod
    def fromStr(w, h, imgb="0000000", dw=1):
        qp = PicQP(max(w, h) * dw, dw)
        cont = 0
        for i in imgb:
            if (cont >= w * h): break
            if i == '0':
                qp.drawBox((cont // w, cont % w), [0, 0, 0])
            cont += 1
        return qp


class ImgBits(imgBase):  # 像素操作

    def b2l(self):
        if self.fn == '': return []
        height = self.img.shape[0]
        weight = self.img.shape[1]
        channels = self.img.shape[2]
        retx = []
        for row in range(height):
            for col in range(weight):
                ch = []
                for c in range(channels):
                    ch.append(self.img[row, col, c])
                retx.append(ch)
        return retx

    def b2ml(self):
        if self.fn == '': return []
        height = self.img.shape[0]
        weight = self.img.shape[1]
        channels = self.img.shape[2]
        retx = []
        for row in range(height):
            coll = []
            for col in range(weight):
                ch = []
                for c in range(channels):
                    ch.append(self.img[row, col, c])
                coll.append(ch)
            retx.append(coll)
        return retx

    @staticmethod
    def gif2bl(fn=''):
        rtl = []
        im = Image.open(fn)
        print("FrameCont:", im.n_frames)
        for i in range(im.n_frames):
            im.seek(i)
            print('duration[04%d] :'%i,im.info['duration'])
            CF = Image.new("RGBA", im.size)
            CF.paste(im)
            img = cv.cvtColor(np.asarray(CF), cv.COLOR_RGB2BGR)
            nb = ImgBits()
            nb.img = img
            nb.height = im.height
            nb.weight = im.width

            nb.fn = 'Tmp'
            rtl.append(nb)
        return rtl

    @staticmethod
    def imgl2gif(image_list, gif_name, duration=0.35):
        frames = []
        for image_name in image_list:
            frames.append(imageio.imread(image_name))
        imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
        return


class PicF:  #
    @staticmethod
    def CompImgFileALL(fn1='', fn2=''):
        for i in range(8):
            for j in range(3):
                PicF.CompImgFile(fn1, fn2, (j, i),SIG=True)
        cv.waitKey()
        cv.destroyAllWindows()


    @staticmethod
    def CompImgFile(fn1='', fn2='', bits=(0, 0),SIG=False):
        img1 = imgBase(fn1)
        img2 = imgBase(fn2)
        PicF.CompImg(img1, img2,bits=bits)

    @staticmethod
    def CompImg(img1, img2, bits=(0, 0),SIG=False):
        w = min(img1.weight, img2.weight)
        h = min(img1.height, img2.height)
        c = min(img1.channels, img2.channels)
        img = np.zeros((h + 1, w + 1, c), np.uint8)
        img.fill(0)
        for i in range(w):
            for j in range(h):
                b1 = img1.getxy(i, j)
                b2 = img2.getxy(i, j)
                if bits == (0, 0):
                    for x in range(c):
                        xr = 0
                        if b1[x] ^ b2[x] == 0: xr = 255
                        img[j,i] = img[j,i] | xr
                elif not ((b1[bits[0]]) & (1 << bits[1]) & 0xff)  < ((b2[bits[0]])== (1 << bits[1]) & 0xff):
                    img[j, i] = 255
        cv.imshow('image%d,%d'%bits, img)
        if SIG:
            cv.waitKey(0)
            cv.destroyAllWindows()


class pngFunc(ImgBits):
    def crc_wh(self):
        self.crc_blaster(self.fn)
    @staticmethod
    def crc_blaster(fn='', cx=0):  # PNG求宽高
        m = open(fn, "rb").read()
        k = 0
        if cx == 0:
            cx = m[0x1d] << 24 | m[0x1e] << 16 | m[0x1f] << 8 | m[0x20]
        print(fn)
        print('- ' * 15)
        print('CRC: x%X' % cx)

        for i in range(5000):
            for j in range(5000):
                c = m[12:16] + struct.pack('>i', i) + struct.pack('>i', j) + m[24:29]
                crc = binascii.crc32(c) & 0xffffffff
                if crc == cx:
                    print("\r\nW:%08X\r\nH:%08X" % (i, j));
        print('- ' * 15)



    png_chunk = []
    imgb=b''
    def __init__(self,fn=''):
        super(pngFunc, self).__init__(fn)
        self.imgb = open(fn, 'rb').read()
        self.png_chunk=[]
        sp = 8
        cont = 0
        self.png_chunk.append([cont, 0, 'HEAD', 8, '00000000', '00000000',self.imgb[:8]])
        cont=1

        while sp < len(self.imgb):
            lenx = int(struct.unpack_from('>I', self.imgb[sp:sp + 4])[0])#长度
            sp += 4
            typex = self.imgb[sp:sp + 4].decode()#标志头
            sp += 4
            ssp = sp #不包括头和长度的chunk起始

            dat = self.imgb[sp:sp + int(lenx)]
            sp += lenx
            crcx = self.imgb[sp:sp + 4].hex() # 虚假的crc

            crc = format(binascii.crc32(self.imgb[ssp - 4:sp]), '08x')# 真实的crc
            sp += 4

            print('%4d' % cont, typex, crcx, crc, '[ ]' if crcx == crc else '[x]', '%-5d' % lenx, '%-5x' % ssp,
                  dat[:40])
            self.png_chunk.append([cont, ssp-8, typex, lenx+12, crcx, crc ,dat])
            cont += 1
            if 'IEND' == typex:
                print('%4d' % cont, '----', '00000000', '00000000',  '[ ]', '%-5d' % (len(self.imgb) - sp), '%-5x' % sp, self.imgb[sp:])
                self.png_chunk.append([cont, sp, '----',  len(self.imgb) - sp,'00000000','00000000' ,self.imgb[sp:]])
            
        print('Filters:')
        self.Filters = self.getFilters() 

    def getFilters(self):
        bit=b''
        for i in self.png_chunk:
            if i[2] =="IDAT":
                bit+=i[-1]
        bit = zlib.decompress(bit)
        linew = self.weight*self.channels
        bf = []
        for i in range(self.height):
            bf.append(bit[linew*i+i])
        print(''.join(map(str,bf)))
        return bf

    def getunZip(self,cn=1):
        bits=b''
        if isinstance(cn,list):
            for i in cn:
                bits+=self.png_chunk[i][-1]
        else:
            bits=self.png_chunk[cn][-1]
        try:
            print(len(bits))
            return zlib.decompress(bits)
        except:
            return 'zlib.decompress Error'
    def getChunk(self,i):
        try:
            tca = self.png_chunk[i]
            print(tca[:-1])
            return self.imgb[tca[1]:tca[1]+tca[3]]
        except:
            return b''

def wh_blaster(fn): #爆破宽高
    img = cv.imread(fn)
    img = img.reshape(-1, 1, 3)
    totPoints = img.shape[0]
    mins = 1e10

    def getgauss(w):
        tp = totPoints - totPoints % w
        src = img[:tp, :, :].reshape(-1, w, 3)
        gauss = cv.GaussianBlur(src, (3, 3), 3)
        gaussedge = cv.Canny(gauss, 0, 50)
        ge = np.sum(gaussedge)
        return ge
    x = []
    y = []
    for i in tqdm.trange(10, len(img) // 3, 1):
        now = getgauss(i)
        x.append(i)
        y.append(now)
        if now < mins:
            mins = now
            tp = totPoints - totPoints % i
            src = img[:tp, :, :].reshape(-1, i, 3)
            print('w=',i)
            plt.cla()
            plt.imshow(src)
            plt.pause(0.1)
    plt.show()
    plt.plot(x, y)
    plt.show()
from apng import APNG
def apng_png(s=''):
    x = APNG.open(s)
    for i in range(len(x.frames)):
        tmp = x.frames[i][0].to_bytes()
        fn=s[:-4]+'_%3d.png'%i
        w = open(fn, 'wb')
        w.write(tmp)
        w.close()

''' 盲水印，调用举例
f,a = plt.subplots()
f.set_size_inches(8,8)
f.set_dpi(100)
plt.set_cmap('gray')
for i in range(20,50):
    tmp = imf.bwmdecode(alpha=i*1.0/20)
    # cv2.imwrite('z:/tmp.png', tmp)
    print(i/5.0)
    a.cla()
    a.imshow(tmp[:,:,0])
    plt.pause(0.01)

    del tmp
'''
import cv2
import random
def bwmdecode(fn1='z:/ctf/2.png',fn2='z:/ctf/1.png',alpha=1.0, seed = 20160930):
    img = cv2.imread(fn1)
    img_wm = cv2.imread(fn2)
    random.seed(seed)
    m, n = list(range(int(img.shape[0] * 0.5))), list(range(img.shape[1]))
    random.shuffle(m)
    random.shuffle(n)
    f1 = np.fft.fft2(img)
    f2 = np.fft.fft2(img_wm)
    rwm = (f2 - f1) / alpha
    rwm = np.real(rwm)
    wm = np.zeros(rwm.shape)
    for i in range(int(rwm.shape[0] * 0.5)):
        for j in range(rwm.shape[1]):
            wm[m[i]][n[j]] = np.uint8(rwm[i][j])
    for i in range(int(rwm.shape[0] * 0.5)):
        for j in range(rwm.shape[1]):
            wm[rwm.shape[0] - i - 1][rwm.shape[1] - j - 1] = wm[i][j]
    return wm%255




def img2BF(fn=''):
    img = Image.open(fn)
    def brainfuck(i):
        if i == (255, 0, 0):    return '>'
        elif i == (128, 0, 0):  return '<'
        elif i == (0, 255, 0):  return '+'
        elif i == (0, 128, 0):  return '-'
        elif i == (0, 0, 255):  return '.'
        elif i == (0, 0, 128):  return '.'
        elif i == (255, 255, 0): return '['
        elif i == (128, 128, 0): return ']'
        return ''
    h = img.height
    w = img.width
    out = ''
    for y in range(h):
        if y % 2 == 0:
            for x in range(w):
                res = img.getpixel((x, y))
                out+=brainfuck(res)
        elif y % 2 != 0:
            for x in range(28):
                res = img.getpixel((27 - x, y))
                out+=brainfuck(res)
    print('- '*30)
    print(out)
    print('- ' * 30)
    return out


    plt.figure(figsize=(6.8, 4), dpi=600)
    plt.axis("scaled")

    K_ = K//17
    for x in range(W):
        for y in range(H):
            if K_ & 1:
                plt.bar(x+0.5, bottom=y, height=1,
                        width=1, linewidth=0, color="black")
            K_ >>= 1


import textwrap
def Tupper(K,H = 17,W = 106):
    plt.figure(figsize=(6.8, 4), dpi=100)
    plt.axis("scaled")
    K_ = K // H
    for x in range(W):
        for y in range(H):
            if K_ & 1:
                plt.bar(x + 0.5, bottom=y, height=1,
                        width=1, linewidth=0, color="black")
            K_ >>= 1
    plt.figtext(0.5, 0.8, r"$\frac{1}{2}<\left\lfloor \operatorname{mod}\left(\left\lfloor\frac{y}{%d}\right\rfloor 2^{-%d\lfloor x\rfloor-\operatorname{mod}(\lfloor y\rfloor, %d)}, 2\right)\right\rfloor$" % (H, H, H), ha="center", va="bottom", fontsize=18)
    plt.subplots_adjust(top=0.8, bottom=0.5)
    K_str = textwrap.wrap(str(K), 68)
    K_str[0] = f"K={K_str[0]}"
    for i in range(1, len(K_str)):
        K_str[i] = f"  {K_str[i]}".ljust(70)
    K_str = "\n".join(K_str)
    plt.figtext(0.5, 0.8,
                r"$\frac{1}{2}<\left\lfloor \operatorname{mod}\left(\left\lfloor\frac{y}{%d}\right\rfloor 2^{-%d\lfloor x\rfloor-\operatorname{mod}(\lfloor y\rfloor, %d)}, 2\right)\right\rfloor$" % (
                H, H, H), ha="center", va="bottom", fontsize=18)
    plt.subplots_adjust(top=0.8, bottom=0.5)
    K_str = textwrap.wrap(str(K), 68)
    K_str[0] = f"K={K_str[0]}"
    for i in range(1, len(K_str)):
        K_str[i] = f"  {K_str[i]}".ljust(70)
    K_str = "\n".join(K_str)
    plt.figtext(0.5, 0.45, K_str, fontfamily="monospace", ha="center", va="top")

    plt.xlim((0, W))
    plt.ylim((0, H))
    xticks = list(range(0, W + 1))
    xlabels = ["" for i in xticks]
    xlabels[0] = "0"
    xlabels[-1] = str(W)
    plt.xticks(xticks, xlabels)
    yticks = list(range(0, H + 1))
    ylabels = ["" for i in yticks]
    ylabels[0] = "K"
    ylabels[-1] = f"K+{H}"
    plt.yticks(yticks, ylabels)
    plt.grid(b=True, linewidth=0.5)
    plt.show()

def chkimg(fn,find_list={'key','flag','Zmxh','ctf'},lsbpws='123456'):
    pf=pngFunc(fn)
    print('- '*40)

    with open(fn,'rb') as f:
        x = f.read()
        for i in find_list:
            stf = b'('+i.encode()+ b'.{10})'
            for j in re.findall(stf,x,re.I):
                print(j)

    print('- '*40)
    try:
        os_lsb.analyse(fn)
        os_lsb.extract(fn,f'{fn}.txt',lsbpws)
    except: pass

    print('- ' * 40)

    cvp =cv2.imread(fn,-1)
    w,h,n = cvp.shape


    for i in range(8):
        for j in range(n):
            plt.figure(figsize=(h/10,w/10),dpi=10)
            plt.tight_layout()
            print(f'Bit{i},Chi{j}')
            plt.axis('off')
            plt.xticks([])
            plt.yticks([])
            plt.imshow((cvp[:,:,j]>>i)&1)
            plt.show()
    plt.show()
    plt.figure(figsize=(30,15))
    print('L:1')
    for i in range(8):
        for j in range(n):
            plt.subplot(8*n,1,n*i+j+1)
            plt.tight_layout()
            plt.title(f'Bit{i},Chi{j}')
            plt.axis('off')
            plt.xticks([])
            plt.yticks([])
            plt.imshow((cvp[:1,:200,j]>>i)&1)
    plt.show()
    print('L:-1')
    plt.figure(figsize=(30,15))
    for i in range(8):
        for j in range(n):
            plt.subplot(8*n,1,n*i+j+1)
            plt.tight_layout()
            plt.title(f'Bit{i},Chi{j}')
            plt.axis('off')
            plt.xticks([])
            plt.yticks([])
            plt.imshow((cvp[-1:,:200,j]>>i)&1)
    plt.show()
    print('R:1')
    plt.figure(figsize=(20,10))
    for i in range(8):
        for j in range(n):
            plt.subplot(1,8*n,n*i+j+1)
            plt.tight_layout()
            plt.title(f'Bit{i},Chi{j}')
            plt.axis('off')
            plt.xticks([])
            plt.yticks([])
            plt.imshow((cvp[:100,:1,j]>>i)&1)
    plt.show()
    print('R:-1')
    plt.figure(figsize=(20,10))
    for i in range(8):
        for j in range(n):
            plt.subplot(1,8*n,n*i+j+1)
            plt.tight_layout()
            plt.title(f'Bit{i},Chi{j}')
            plt.axis('off')
            plt.xticks([])
            plt.yticks([])
            plt.imshow((cvp[:100,-1:,j]>>i)&1)
    plt.show()