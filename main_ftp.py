__author__ = 'smirnov'
# coding: utf8

import ftplib
import logging
import os
import shutil
import site
import sys
import time

site.addsitedir('/opt/swift/')
import smtp

in_dir = '/mnt/trc/_val_/in/'  # Каталог загрузки ЦФТ
out_dir = '/mnt/trc/_val_/out/'  # Каталог выгрузки ЦФТ

wk_out = '/opt/swift/work/out/'  # Рабочий каталог для выгрузки
wk_in = '/opt/swift/work/in/'  # Рабочий каталог для загрузки
wk_event = '/opt/swift/work/event/'  # Рабочий каталог предупреждений

arh_in = '/opt/swift/archive/in/'  # Архив принимаемых сообщений
arh_out = '/opt/swift/archive/out/'  # Архив отправляемых сообщений
arh_event = '/opt/swift/archive/event/'  # Архив предупреждений

log_dir = '/opt/swift/logs/'  # каталог с логами

# host = "web2py.inbank.msk"
# ftp_user = "root"
# ftp_password = "**********"

host = "192.168.43.201"
ftp_user = "INKNRUM2"
ftp_password = "********"

# smb = smbclient.SambaClient(server="db11", share="ibs", username='cb', password='************', domain='DB11')


logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG,
                    filename=log_dir + time.strftime("%Y%m%d") + 'log.log'.encode('utf-8'))

# Блок выгрузки.
try:
    out_list = dict([(f, None) for f in os.listdir(out_dir)])
except BaseException:
    out_list = {}

if out_list != {}:
    for x in out_list:
        if (x[-3:]) == 'swl':
            logging.info(u'Пришел файл ' + x)
            try:
                shutil.copy2(out_dir + x, arh_out)
                logging.info(u'Файл ' + x + u' помещен в архив.')
            except BaseException:
                logging.error(u'Ошибка при копирвоании ' + x + u' в arh_out. Причина:' + str(sys.exc_info()))
                # print(sys.exc_info())
            try:
                # TODO нужен ли этот пункт? Может сразу на ftp  и архив?
                shutil.copy2(out_dir + x, wk_out)
                os.remove(out_dir + x)
                logging.info(u'Файл ' + x + u' перемещен в ' + wk_out)
                # print(u'Файл '+x+u' перемещен в '+wk_out)
            except BaseException:
                logging.error(u'Ошибка при перемещении ' + x + u' в ' + wk_out + u'. Причина:' + str(sys.exc_info()))
                # print(sys.exc_info())
try:
    out_list_wk = dict([(f, None) for f in os.listdir(wk_out)])
except BaseException:
    out_list_wk = {}
if out_list_wk != {}:
    for x in out_list_wk:
        try:
            logging.info(u'Начинаем подключаться к ftp ')
            con = ftplib.FTP(host, ftp_user, ftp_password, timeout=40)
            logging.info(u'Подключились к ftp ')
            f = open(wk_out + x, "r")
            logging.info(u'Открыли файл для передачи на ftp')
            con.cwd('/in')  # каталог на ftp
            try:
                # send = con.storbinary('STOR '+x, f)
                send = con.storlines("STOR " + x, f)
                f.close()
                logging.info(u'Файл ' + x + u' помещен на ftp ')
                # print(u'Скопирован на FTP')
                con.close()
                try:
                    os.remove(out_dir + x)
                    logging.error(u'Файл ' + x + u' был в каталоге ' + out_dir + ' ' + str(sys.exc_info()))
                except:
                    pass
                try:
                    os.remove(wk_out + x)
                    logging.info(u'Файл ' + x + u' удален из ' + wk_out)
                except:
                    logging.error(u'Файл ' + x + u' не удален из каталога ' + wk_out + ' ' + str(sys.exc_info()))
            except:
                f.close()
                con.close()
                logging.error(u'Ошибка при передаче файла ' + x + u' на ftp.' + str(sys.exc_info()))
        except BaseException:
            logging.error(u'Ошибка при подключении к ftp.' + str(sys.exc_info()))
            # print(sys.exc_info())

            # print(sys.exc_info())
# try:
#     con = ftplib.FTP(host, ftp_user, ftp_password)
#     ##print(con.dir('/in'))
#     con.cwd('/in') #каталог на ftp
#     con.quit()
# except BaseException:
#     logging.error(u'Ошибка при подключении к ftp.'+str(sys.exc_info()))
#     #print(sys.exc_info())
# Блок загрузки
try:
    con = ftplib.FTP(host, ftp_user, ftp_password, timeout=40)
    con.cwd('/out')  # каталог на ftp
    listing = []
    con.retrlines("LIST", listing.append)
    file_from_ftp = []
    for wor in listing:
        tmp = (wor.split(None, 8))
        file_from_ftp.append(tmp[-1].lstrip())
    # скачиваем файл
    ##print(str(file_from_ftp))
    for v in file_from_ftp:
        local_filename = os.path.join(r"/opt/swift/work/in/", v)  # этот момент переделать
        lf = open(local_filename, "wb")
        con.retrbinary("RETR " + v, lf.write, 8 * 1024)
        logging.info(u'Файл ' + v + u' скопирован в ' + wk_in)
        lf.close()
        try:
            con.delete(v)
        except:
            logging.error(u'Файл ' + v + u' не удален с ftp')
            # тут отправить письмо об ошибке
        logging.info(u'Файл ' + v + u' удален с ftp')
    con.close()
except BaseException:
    logging.error(u'Ошибка при подключении к ftp.' + str(sys.exc_info()))
    # print(sys.exc_info())
try:
    con = ftplib.FTP(host, ftp_user, ftp_password, timeout=40)
    con.cwd('/event')  # каталог на ftp
    listing = []
    con.retrlines("LIST", listing.append)
    file_from_ftp = []
    for wor in listing:
        tmp = (wor.split(None, 8))
        file_from_ftp.append(tmp[-1].lstrip())
    # скачиваем файл
    ##print(str(file_from_ftp))
    for v in file_from_ftp:
        local_filename = os.path.join(r"/opt/swift/work/event/", v)  # этот момент переделать
        lf = open(local_filename, "wb")
        con.retrbinary("RETR " + v, lf.write, 8 * 1024)
        logging.info(u'Файл ' + v + u' скопирован в ' + wk_event)
        lf.close()
        try:
            con.delete(v)
        except:
            logging.error(u'Файл ' + v + u' не удален с ftp')
            # тут отправить письмо об ошибке
        logging.info(u'Файл ' + v + u' удален с ftp')
    con.close()

except BaseException:
    logging.error(u'Ошибка при подключении к ftp.' + str(sys.exc_info()))
    # print(sys.exc_info())

try:
    con = ftplib.FTP(host, ftp_user, ftp_password, timeout=40)
    con.cwd('/ack_nak')  # каталог на ftp
    listing = []
    con.retrlines("LIST", listing.append)
    file_from_ftp = []
    for wor in listing:
        tmp = (wor.split(None, 8))
        file_from_ftp.append(tmp[-1].lstrip())
    # скачиваем файл
    ##print(str(file_from_ftp))
    for v in file_from_ftp:
        local_filename = os.path.join(r"/opt/swift/archive/in/", v)  # этот момент переделать
        lf = open(local_filename, "wb")
        con.retrbinary("RETR " + v, lf.write, 8 * 1024)
        logging.info(u'Файл ' + v + u' скопирован в ' + arh_in)
        lf.close()
        try:
            con.delete(v)
        except:
            logging.error(u'Файл ' + v + u' не удален с ftp')
            # тут отправить письмо об ошибке
        logging.info(u'Файл ' + v + u' удален с ftp')
    con.close()

except BaseException:
    logging.error(u'Ошибка при подключении к ftp.' + str(sys.exc_info()))
    # print(sys.exc_info())

# МТ190
# МТ192
# МТ195
# МТ196
# МТ910


try:
    in_list = dict([(f, None) for f in os.listdir(wk_in)])
except BaseException:
    in_list = {}
sw103 = {'title': u'Входящее из БФК. Тип: 103', 'text': u'103 - Однократное зачисление клиентских средств.',
         'listfile': []}
sw190 = {'title': u'Входящее из БФК. Тип: 190', 'text': u'190 - Консультации по Сборам, Процентам и Другим Поправкам.',
         'listfile': []}
sw192 = {'title': u'Входящее из БФК. Тип: 192', 'text': u'192 - Запрос об отмене.', 'listfile': []}
sw195 = {'title': u'Входящее из БФК. Тип: 195', 'text': u'195 - Запросы.', 'listfile': []}
sw196 = {'title': u'Входящее из БФК. Тип: 196', 'text': u'196 - Ответы на запросы.', 'listfile': []}
sw199 = {'title': u'Входящее из БФК. Тип: 199', 'text': u'199 - Сообщение в свободном формате.', 'listfile': []}
sw202 = {'title': u'Входящее из БФК. Тип: 202', 'text': u'202 - Обычные переводы финансовых учреждений.',
         'listfile': []}
sw299 = {'title': u'Входящее из БФК. Тип: 299', 'text': u'299 - Сообщение в свободном формате.', 'listfile': []}
sw320 = {'title': u'Входящее из БФК. Тип: 320', 'text': u'320 - Подтверждение долгосрочного кредита/депозита.',
         'listfile': []}
sw900 = {'title': u'Входящее из БФК. Тип: 900', 'text': u'900 - Подтверждение списания.', 'listfile': []}
sw910 = {'title': u'Входящее из БФК. Тип: 910', 'text': u'910 - Подтверждение зачисления.', 'listfile': []}
sw950 = {'title': u'Входящее из БФК. Тип: 950', 'text': u'950 - Выписка.', 'listfile': []}
sw999 = {'title': u'Входящее из БФК. Тип: 999', 'text': u'999 - Сообщение в свободном формате.', 'listfile': []}
swevent = {'title': u'Входящее из БФК. Тип: Информационное', 'text': u'Текст входящего информационного сообщения:\n',
           'listfile': []}
if in_list != {}:
    # print(u'Есть что то в in')
    for x in in_list:
        files = open(wk_in + x, 'r')
        for f in files.readlines():
            # В ЦФТ #
            if f.find('{2:O103') != -1:
                # print(u'нашли строку')
                files.close()
                try:
                    # print(u'Пробуем загрузить на trc')
                    # smb.upload(wk_in+x,"/trc/_val_/in/"+x)
                    shutil.copy2(wk_in + x, in_dir)
                    logging.info(u'Файл ' + x + u' помещен в /trc/_val_/in/.')
                    continue
                except:
                    logging.error(u'Ошибка при копировании ' + x + u' в /trc/_val_/in/. Причина:' + str(sys.exc_info()))
            if f.find('{2:O202') != -1:
                # print(u'нашли строку')
                files.close()
                try:
                    # print(u'Пробуем загрузить на trc')
                    shutil.copy2(wk_in + x, in_dir)
                    logging.info(u'Файл ' + x + u' помещен в /trc/_val_/in/.')
                    continue
                except:
                    logging.error(u'Ошибка при копировании ' + x + u' в /trc/_val_/in/. Причина:' + str(sys.exc_info()))
            # В почту #
            if f.find('FIN 103') != -1:
                files.close()
                sw103['listfile'].append(arh_in + x)
                continue
            if f.find('FIN 190') != -1:
                files.close()
                sw190['listfile'].append(arh_in + x)
                continue
            if f.find('FIN 192') != -1:
                files.close()
                sw192['listfile'].append(arh_in + x)
                continue
            if f.find('FIN 195') != -1:
                files.close()
                sw195['listfile'].append(arh_in + x)
                continue
            if f.find('FIN 196') != -1:
                files.close()
                sw196['listfile'].append(arh_in + x)
                continue
            if f.find('FIN 199') != -1:
                files.close()
                sw199['listfile'].append(arh_in + x)
                continue
            if f.find('FIN 202') != -1:
                files.close()
                sw202['listfile'].append(arh_in + x)
                continue
            if f.find('FIN 299') != -1:
                files.close()
                sw299['listfile'].append(arh_in + x)
                continue
            if f.find('FIN 320') != -1:
                files.close()
                sw320['listfile'].append(arh_in + x)
                continue
            if f.find('FIN 900') != -1:
                files.close()
                sw900['listfile'].append(arh_in + x)
                continue
            if f.find('FIN 910') != -1:
                files.close()
                sw910['listfile'].append(arh_in + x)
                continue
            if f.find('FIN 950') != -1:
                files.close()
                sw950['listfile'].append(arh_in + x)
                continue
            if f.find('FIN 999') != -1:
                files.close()
                sw999['listfile'].append(arh_in + x)
                continue
        try:
            shutil.move(wk_in + x, arh_in)
            logging.info(u'Файл ' + x + u' перемещен в ' + arh_in)
            # print(u'Файл '+x+u' перемещен в '+arh_in)
        except BaseException:
            logging.error(u'Ошибка при перемещении ' + x + u' в ' + arh_in + u'. Причина:' + str(sys.exc_info()))
            # print(sys.exc_info())
try:
    event_list = dict([(f, None) for f in os.listdir(wk_event)])
except BaseException:
    event_list = {}
if event_list != {}:
    # print(u'Есть что то в Event')
    for x in event_list:
        files = open(wk_event + x, 'r')
        for f in files.readlines():
            swevent['text'] = swevent['text'] + f
            files.close()
        swevent['listfile'].append(arh_event + x)
        try:
            shutil.move(wk_event + x, arh_event)
            logging.info(u'Файл ' + x + u' перемещен в ' + arh_event)
            # print(u'Файл '+x+u' перемещен в '+arh_event)
        except BaseException:
            logging.error(u'Ошибка при перемещении ' + x + u' в ' + arh_event + u'. Причина:' + str(sys.exc_info()))
            # print(sys.exc_info())
listi = [sw103, sw190, sw192, sw195, sw196, sw202, sw320, sw900, sw910, sw950, sw199, sw299, sw999, swevent]
listi_950 = [sw950, ]

for x in listi_950:
    if x['listfile'] != []:
        for y in ['reglament@in-bank.ru', 'd.stepanov@in-bank.ru', 'a.dubensky@in-bank.ru']:
            # for y in ['a.smirnov@in-bank.ru',]:
            # print(y)
            # smtp.Send(FileFolder=x['listfile'],subj=x['title']+' '+time.strftime('%Y.%m.%d'),you=y, Text=(x['text']))
            try:
                smtp.Send(FileFolder=x['listfile'], subj=x['title'], you=y, Text=(x['text']))
                # print(u'Отправлено')
                time.sleep(15)
            except BaseException:
                # print(u'Сообщение по почте не отправлено.')
                # print(sys.exc_info())
                logging.error(u'Сообщение по почте не отправлено.' + sys.exc_info())
                time.sleep(60)
                smtp.Send(subj='Сообщение не отправлено!!!' + x['title'], you='reglament@in-bank.ru', Text=(x['text']))

for x in listi:
    if x['listfile'] != []:
        for y in ['reglament@in-bank.ru', 'bfk@in-bank.ru']:
            # for y in ['a.smirnov@in-bank.ru',]:
            # print(y)
            # smtp.Send(FileFolder=x['listfile'],subj=x['title']+' '+time.strftime('%Y.%m.%d'),you=y, Text=(x['text']))
            try:
                smtp.Send(FileFolder=x['listfile'], subj=x['title'], you=y, Text=(x['text']))
                # print(u'Отправлено')
                time.sleep(15)
            except BaseException:
                # print(u'Сообщение по почте не отправлено.')
                # print(sys.exc_info())
                logging.error(u'Сообщение по почте не отправлено.' + sys.exc_info())
                time.sleep(60)
                smtp.Send(subj='Сообщение не отправлено!!!' + x['title'], you='reglament@in-bank.ru', Text=(x['text']))
