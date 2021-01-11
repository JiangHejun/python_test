'''
Description:
Author: Hejun Jiang
Date: 2021-01-11 11:33:56
LastEditTime: 2021-01-11 15:53:39
LastEditors: Hejun Jiang
Version: v0.0.1
Contact: jianghejun@hccl.ioa.ac.cn
Corporation: hccl
'''
import os
import uuid
import time
import base64
from pyDes import des, CBC, PAD_PKCS5


def get_mac_address():
    node = uuid.getnode()
    mac = uuid.UUID(int=node).hex[-12:]
    return mac


def get_sys_time():
    return str(int(time.time()))


def getinfo(machinefile):
    info = get_mac_address() + ' ' + get_sys_time()
    with open(machinefile, 'w', encoding='utf-8') as fout:
        f = base64.b64encode(info.encode('utf-8'))
        fout.write(f.decode('utf-8'))
    print('get new {} file success'.format(machinefile))
    exit(-1)


def checkinfo():
    Des_key = "think@it"  # Key,需八位
    Des_IV = "\x11\2\x2a\3\1\x27\2\0"  # 自定IV向量
    machinefile = './machine.info'
    licensefile = './license.dat'
    timelen = 10  # system time lenght
    if not os.path.isfile(licensefile):
        print('{} is not exists, please submit the {} file to manager for getting the LICENSE file'.format(licensefile, machinefile))
        getinfo(machinefile)
    else:
        with open(licensefile, 'r', encoding='utf-8') as fin:
            linfo = fin.readlines()
            lmacinfo = linfo[0].split()[0].encode('utf-8')  # bytes
            ltimeinfo = linfo[1].split()[0]  # str

            k = des(Des_key, CBC, Des_IV, pad=None, padmode=PAD_PKCS5)  # just for mac address
            macinfo = base64.b64encode(k.encrypt(get_mac_address().encode('utf-8')))
            if macinfo == lmacinfo:
                ltimeinfo = base64.b64decode(ltimeinfo)
                lmaxday = int(ltimeinfo[timelen:])  # day
                ltimeinfo = int(ltimeinfo[:timelen])  # time
                interval = (int(get_sys_time()) - ltimeinfo) / 86400  # day
                if interval > lmaxday:
                    print('{} is out of date, please submit the {} file to manager again for getting the new LICENSE file'.format(licensefile, machinefile))
                    getinfo(machinefile)
                else:
                    print('check {} file success'.format(licensefile))
            else:
                print('LICENSE file check failure, please submit the {} file to manager for getting the new LICENSE file'.format(licensefile))
                getinfo(machinefile)


if __name__ == '__main__':
    checkinfo()
