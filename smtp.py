import os
import smtplib

#import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def Send(subj="Test", Text="Test", me='noreply@inbank.msk', you='reglament@in-bank.ru;', FileFolder=None):
    msg = MIMEMultipart()
    server = "ex01.inbank.msk:587"
    #port = 2525
    user_name = "noreply@inbank.msk"
    user_passwd = "*****************"

    body = MIMEText(Text, "", "cp1251")
    msg['Subject'] = "[ROBOT] " + subj
    msg['From'] = me
    msg['To'] = you

    s = smtplib.SMTP(server)
    s.set_debuglevel(0)
    s.starttls()
    s.login(user_name, user_passwd)
    msg.attach(body)
    #if File!=None and os.path.isfile(File):
    #    attachment = MIMEApplication(open(File,'rb').read())
    #    attachment.add_header('Content-Disposition', 'attachment', filename=File)
    #    msg.attach(attachment)
    #if FileFolder!=None and os.path.isdir(FileFolder):
    #files=glob.glob(os.path.join(FileFolder+'\\'+fileinfolder))
    files = (FileFolder)
    if files!=None:
        for item in files:
            #print(item)
            attachment = MIMEApplication(open(item, 'rb').read())
            attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(item))
            msg.attach(attachment)
            #print(files)
    s.sendmail(me, you, msg.as_string())

    s.quit()