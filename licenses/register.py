'''
Description:
Author: Hejun Jiang
Date: 2021-01-11 10:55:33
LastEditTime: 2021-01-11 15:55:24
LastEditors: Hejun Jiang
Version: v0.0.1
Contact: jianghejun@hccl.ioa.ac.cn
Corporation: hccl
'''
import os
import base64
from pyDes import des, CBC, PAD_PKCS5


def register(day):
    Des_key = "think@it"  # Key,需八位
    Des_IV = "\x11\2\x2a\3\1\x27\2\0"  # 自定IV向量
    machinefile = './machine.info'
    licensefile = './license.dat'
    if not os.path.isfile(machinefile):
        print('{} is not exists'.format(machinefile))
        exit(-1)
    else:  # DES+base64加密
        with open(machinefile, 'r', encoding='utf-8') as fin:
            f = fin.read()
            info = base64.b64decode(f.encode('utf-8')).decode('utf-8').split()  # mac, time

            k = des(Des_key, CBC, Des_IV, pad=None, padmode=PAD_PKCS5)  # just for mac address
            info[0] = k.encrypt(info[0].encode('utf-8'))
            info[1] = (info[1] + str(day)).encode('utf-8')

            with open(licensefile, 'w', encoding='utf-8') as fout:
                for line in info:
                    fout.write(base64.b64encode(line).decode('utf-8')+'\n')
                print('{} is registed success'.format(licensefile))


if __name__ == '__main__':
    register(30)
