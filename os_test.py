__author__ = 'smirnov'
# coding: utf8

import os
import shutil
from shutil import copyfile
import time
import logging
import ftplib
import sys
import site
import smbclient

site.addsitedir('/opt/swift/')
import smtp

print('start')

in_dir='/mnt/trc/_val_/in' 		#Каталог загрузки ЦФТ
out_dir='/mnt/trc/_val_/out/'

wk_out='/opt/swift/work/out/' 		#Рабочий каталог для выгрузки
wk_in='/opt/swift/work/in/' 		#Рабочий каталог для загрузки
wk_event='/opt/swift/work/event/'


ftp_in='/mnt/webdav/IN/'
ftp_in_tst='/mnt/webdav/IN-test/'
ftp_out='/mnt/webdav/OUT/'
ftp_event='/mnt/webdav/EVENT/'
ftp_ack_nak='/mnt/webdav/ACK_NAK/'


x='/opt/swift/test.txt'

# try:
#     print(u'Пробуем загрузить на trc')
#     #print(os.listdir(ftp_out))
#     # f = open(ftp_in+'test2.txt', "w")
#     # f.write('Test')
#     # f.close()
#     copyfile(x, ftp_in_tst)
#     print(u'Файл '+x+u' помещен в /trc/_val_/in/.')
#
# except:
#     print(sys.exc_info())
print(x)
print(ftp_in_tst)
# shutil.copy(x,ftp_in_tst)

print(os.listdir(ftp_out))
print(os.path.getsize(x))
print('---------------')
