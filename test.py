__author__ = 'smirnov'
# coding: utf8
import ftplib
import os

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
        print(wor)
        #file_from_ftp.append(tmp[-1].lstrip())
    # скачиваем файл
    ##print(str(file_from_ftp))
except:
    print('fail')


try:

    con = ftplib.FTP(host, ftp_user, ftp_password)

    f = open(wk_out+x, "rb")

    con.cwd('/in') #каталог на ftp
    try:
        send = con.storbinary('STOR '+x, f)
        f.close()
        logging.info(u'Файл '+x+u' помещен на ftp ')
        #print(u'Скопирован на FTP')
        con.close()
        try:
            os.remove(out_dir+x)
            logging.error(u'Файл '+x+u' был в каталоге '+out_dir+' '+str(sys.exc_info()))
        except:
            pass
        try:
            os.remove(wk_out+x)
            logging.info(u'Файл '+x+u' удален из '+wk_out)
        except:
            logging.error(u'Файл '+x+u' не удален из каталога '+wk_out+' '+str(sys.exc_info()))
    except:
        f.close()
        con.close()
        logging.error(u'Ошибка при передаче файла '+x+u' на ftp.'+str(sys.exc_info()))
except BaseException:
    logging.error(u'Ошибка при подключении к ftp.'+str(sys.exc_info()))