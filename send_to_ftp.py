# coding: utf8

import os
import shutil
import time
import logging
import ftplib
import sys
import site
import smbclient

site.addsitedir('/opt/swift/')
import smtp


in_dir='/mnt/trc/_val_/in/' 		#Каталог загрузки ЦФТ
out_dir='/mnt/trc/_val_/out/' 		#Каталог выгрузки ЦФТ

wk_out='/opt/swift/test/out/' 		#Рабочий каталог для выгрузки
wk_in='/opt/swift/work/in/' 		#Рабочий каталог для загрузки
wk_event='/opt/swift/work/event/' 	#Рабочий каталог предупреждений

arh_in='/opt/swift/archive/in/' 	#Архив принимаемых сообщений
arh_out='/opt/swift/archive/out/' 	#Архив отправляемых сообщений
arh_event='/opt/swift/archive/event/' 	#Архив предупреждений

log_dir='/opt/swift/logs/' 		#каталог с логами

# host = "web2py.inbank.msk"
# ftp_user = "root"
# ftp_password = "140271685+-"

host = "192.168.43.201"
ftp_user = "INKNRUM2"
ftp_password = "273D_INHDR"


x='1000077100.swl'


try:
    con = ftplib.FTP(host)

    print(1)
    con.set_pasv(False)
    print(2)
    con.login(ftp_user, ftp_password)
    print(3)
    print(con.getwelcome())
    con.cwd('/in') #каталог на ftp
    try:
        #send = con.storbinary('STOR '+x, f)
        print('Start')
        con.storlines("STOR " + x, open(wk_out+x, "r"))
        con.close()
        try:
            os.remove(out_dir+x)
            print('Файл '+x+' был в каталоге '+out_dir+' '+str(sys.exc_info()))
        except:
            print(sys.exc_info())
            pass
        try:
            os.remove(wk_out+x)
            print('Файл '+x+' удален из '+wk_out)
        except:
            print('Файл '+x+' не удален из каталога '+wk_out+' '+str(sys.exc_info()))
    except:
        print(sys.exc_info())
        con.abort()
        con.close()

except BaseException:

    print(sys.exc_info())
