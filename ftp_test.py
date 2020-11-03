# coding: utf8
import os
import shutil
import time
import logging
import ftplib
import sys

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

try:
    con = ftplib.FTP(host, ftp_user, ftp_password)
    con.cwd('/out') #каталог на ftp
    listing = []
    con.retrlines("LIST", listing.append)
    file_from_ftp=[]
    for wor in listing:
        tmp=(wor.split(None, 8))
        file_from_ftp.append(tmp[-1].lstrip())
    print(file_from_ftp)
    # скачиваем файл
    for v in file_from_ftp:
        local_filename = os.path.join(r"c:\work\inbank\swift\wk\in", v)
        lf = open(local_filename, "wb")
        con.retrbinary("RETR " + v, lf.write, 8*1024)
        lf.close()
        con.delete(v)
    print('Скопирован на FTP')
    con.close()
except BaseException:
    logging.error('Ошибка при подключении к ftp.'+str(sys.exc_info()))
    print(sys.exc_info())



try:
    in_list = dict ([(f, None) for f in os.listdir(wk_in)])
except BaseException:
    in_list = {}
if in_list:
    for x in in_list:
        files=open(wk_in+x,'r')
        for f in files.readlines():
            if f.find('{2:O103')!=-1 or f.find('{2:O202')!=-1:
                files.close()
                try:
                    shutil.copy2(wk_in+x,in_dir)
                    logging.info('Файл '+x+' помещен в '+in_dir)
                    print('Файл '+x+' помещен в архив.')
                except BaseException:
                    logging.error('Ошибка при копирвоании '+x+' в '+in_dir+'. Причина:'+str(sys.exc_info()))
                    print(sys.exc_info())
        try:
            shutil.move(wk_in+x,wk_in_arh)
            logging.info('Файл '+x+' перемещен в '+wk_in_arh)
            print('Файл '+x+' перемещен в '+wk_in_arh)
        except BaseException:
            logging.error('Ошибка при перемещении '+x+' в '+wk_in_arh+'. Причина:'+str(sys.exc_info()))
            print(sys.exc_info())