import zipfile, os


def unzip(zipname):
    while True:
        passwd = zipname.split('.')[0]
        zf = zipfile.ZipFile(zipname, 'r')
        zf.extractall(pwd=passwd.encode())
        zipname = zf.namelist()[0]
        zf.close()


if __name__ == '__main__':

    unzip("OKMIlLVft.tar.gz")
