import hashlib
from Crypto import Random
from Crypto.Cipher import AES
'''
Thanks to
http://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
'''
class AESCipher:

    def __init__(self, key):
        self.bs = 32	# Block size
        self.key = hashlib.sha256(key.encode()).digest()	# 32 bit digest

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(raw)

    def decrypt(self, enc):
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


import sys
import struct
import numpy
import matplotlib.pyplot as plt
from PIL import Image



# Decompose a binary file into an array of bits
def decompose(data):
    v = []

    # Pack file len in 4 bytes
    fSize = len(data)
    bytes = [ord(b) for b in struct.pack("i", fSize)]

    bytes += [ord(b) for b in data]

    for b in bytes:
        for i in range(7, -1, -1):
            v.append((b >> i) & 0x1)

    return v


# Assemble an array of bits into a binary file
def assemble(v):
    bts = []
    length = len(v)
    for idx in range(0, len(v) // 8):
        b = 0
        for i in range(0, 8):
            if (idx * 8 + i < length):
                b = (b << 1) + v[idx * 8 + i]
        bts.append(b)
    bts =bytes(bts)
    pl = struct.unpack("i", bts[:4])[0]
    payload_size = pl
    return bts[4: payload_size + 4]
# Set the i-th bit of v to x
def set_bit(n, i, x):
    mask = 1 << i
    n &= ~mask
    if x:
        n |= mask
    return n

# Extract data embedded into LSB of the input file
def extract(in_file, out_file, password):
    # Process source image
    img = Image.open(in_file)
    (width, height) = img.size
    conv = img.convert("RGBA").getdata()
    print( "[+] Image size: %dx%d pixels." % (width, height))

    # Extract LSBs
    v = []
    print(conv)
    for h in range(height):
        for w in range(width):
            (r, g, b, a) = conv.getpixel((w, h))
            v.append(r & 1)
            v.append(g & 1)
            v.append(b & 1)

    data_out = assemble(v)

    # Decrypt
    cipher = AESCipher(password)
    data_dec = cipher.decrypt(data_out)

    # Write decrypted data
    out_f = open(out_file, "wb")
    out_f.write(data_dec)
    out_f.close()

    print( "[+] Written extracted data to %s." % out_file)
    print("[+] ",data_dec)


# Statistical analysis of an image to detect LSB steganography
def analyse(in_file):
    '''
    - Split the image into blocks.
    - Compute the average value of the LSBs for each block.
    - The plot of the averages should be around 0.5 for zones that contain
      hidden encrypted messages (random data).
    '''
    BS = 100  # Block size
    img = Image.open(in_file)
    (width, height) = img.size
    print(    "[+] Image size: %dx%d pixels." % (width, height))
    conv = img.convert("RGBA").getdata()

    # Extract LSBs
    vr = []  # Red LSBs
    vg = []  # Green LSBs
    vb = []  # LSBs
    for h in range(height):
        for w in range(width):
            (r, g, b, a) = conv.getpixel((w, h))
            vr.append(r & 1)
            vg.append(g & 1)
            vb.append(b & 1)

    # Average colours' LSB per each block
    avgR = []
    avgG = []
    avgB = []
    for i in range(0, len(vr), BS):
        avgR.append(numpy.mean(vr[i:i + BS]))
        avgG.append(numpy.mean(vg[i:i + BS]))
        avgB.append(numpy.mean(vb[i:i + BS]))

    # Nice plot
    numBlocks = len(avgR)
    blocks = [i for i in range(0, numBlocks)]
    plt.axis([0, len(avgR), 0, 1])
    plt.ylabel('Average LSB per block')
    plt.xlabel('Block number')
   	# plt.plot(blocks, avgR, 'r.')
   	# plt.plot(blocks, avgG, 'g')
    plt.plot(blocks, avgB, 'bo')

    plt.show()


