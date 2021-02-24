'''
Description:
Author: Hejun Jiang
Date: 2021-01-11 10:55:33
LastEditTime: 2021-02-24 11:11:34
LastEditors: Hejun Jiang
Version: v0.0.1
Contact: jianghejun@hccl.ioa.ac.cn
Corporation: hccl
'''
import io
import os
import gzip
import base64
from sys import exit
from pyDes import des, CBC, PAD_PKCS5


def gzip_compress(buf):
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=out, mode="w") as f:
        f.write(buf)
    return out.getvalue()


def gzip_decompress(buf):
    obj = io.BytesIO(buf)
    with gzip.GzipFile(fileobj=obj) as f:
        result = f.read()
    return result


def register(day):
    Des_key = "think@it"  # Key,需八位
    Des_IV = "\x11\2\x2a\3\1\x27\2\0"  # 自定IV向量
    machinefile = './machine.info'
    licensefile = './license.dat'
    if not os.path.isfile(machinefile):
        print('{} is not exists'.format(machinefile))
        exit(-1)
    else:  # DES+base64加密
        with open(machinefile, 'rb') as fin:  # gzip+base64
            f = gzip_decompress(fin.read())
            info = base64.b64decode(f).decode('utf-8').split()  # mac, time
            k = des(Des_key, CBC, Des_IV, pad=None, padmode=PAD_PKCS5)  # just for mac address
            info[0] = k.encrypt(info[0].encode('utf-8'))
            info[1] = (info[1] + str(day)).encode('utf-8')  # bytes
            msg = base64.b64encode(info[0]).decode('utf-8') + ' ' + base64.b64encode(info[1]).decode('utf-8')  # base64
            with open(licensefile, 'wb') as fout:
                fout.write(gzip_compress(msg.encode('utf-8')))
                print('{} is registed success'.format(licensefile))


if __name__ == '__main__':
    register(30)
