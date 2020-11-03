# coding: utf8
import os
import shutil
import time
import logging
import ftplib
import sys
import smbclient

print('sd')
smb = smbclient.SambaClient(server="db02", share="ibs", username='cb', password='1q2w3e!Q@W#E', domain='DB02')
#smb = smbclient.SambaClient(server="192.168.110.192", share="kvt", username='admin', password='chuchuNDR@', domain='WEB2PY')


#
# try:
#     #smb.listdir('/')
#     file_cft=smb.listdir("/trc/_mbr_/out/")
#     #print(file_cft)
#     if file_cft!=[]:
#         for fl in file_cft:
#             print((fl.split())[0])
#             remote_file=((fl.split())[0])
#             if remote_file[-3:]=='xml':
#                 print('xml')
#                 #smb.download("/trc/_mbr_/out/"+remote_file,'/home/net/smirnov/swift/tmp/'+remote_file)
#             else:
#                 continue
#
#     print('copy done')
# except:
#     print(sys.exc_info())


# try:
#     #smb.listdir('/')
#     print('ljikb')
#     file_cft=smb.listdir("/")
#     print(file_cft)
#     if file_cft!=[]:
#         for fl in file_cft:
#             print('не пустой')
#             #smb.download("/trc/_val_/out/"+fl,)
#     print('copy done')
# except:
#     print(sys.exc_info())

log_dir='C:\\\\work\\inbank\\swift\\' # каталог с логами
out_dir='c:\\\\work\\inbank\\swift\\db02\\trc\\out\\' #Каталог выгрузки ЦФТ
wk_out='C:\\\\work\\inbank\\swift\\wk\\out\\' #Рабочий каталог для выгрузки
wk_out_arh='C:\\\\work\\inbank\\swift\\wk\\arh_out\\' #Архив отправляемых сообщений
wk_in='C:\\\\work\\inbank\\swift\\wk\\in\\' #Рабочий каталог для загрузки
wk_in_arh='C:\\\\work\\inbank\\swift\\wk\\arh_in\\' #Архив принимаемых сообщений
in_dir='c:\\\\work\\inbank\\swift\\db02\\trc\\in\\' #Каталог загрузки ЦФТ

host = "192.168.43.201"
ftp_user = "INKNRUM2"
ftp_password = "273D_INHDR"

# host = "web2py.inbank.msk"
# ftp_user = "root"
# ftp_password = "140271685+-"

try:
    con = ftplib.FTP(host, ftp_user, ftp_password)
    con.cwd('/in') #каталог на ftp
    listing = []
    con.retrlines("LIST", listing.append)
    file_from_ftp=[]
    for wor in listing:
        tmp=(wor.split(None, 8))
        file_from_ftp.append(tmp[-1].lstrip())
    print(file_from_ftp)
except BaseException:
    print(sys.exc_info())
# try:
#     print(u'Подключаемся к фтп')
#     con = ftplib.FTP(host, ftp_user, ftp_password)
#     f = open('00000370.swl', "rb")
#     con.cwd('/in') #каталог на ftp
#     send = con.storbinary('STOR '+'00000370.swl',f)
#     #logging.info(u'Файл '+remote_file+u' помещен на ftp ')
#     print(u'Скопирован на FTP')
#     f.close()
#     con.close()
# except BaseException:
#     #logging.error(u'Ошибка при подключении к ftp.'+str(sys.exc_info()))
#     print(sys.exc_info())