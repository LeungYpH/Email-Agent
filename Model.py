import smtplib
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import imaplib,email,os
from bs4 import BeautifulSoup
class Mail():
    def __init__(self,title):
        pass

class Message():
    '''
    邮件的基本元素【主题】【内容】【来源】
    '''
    def __init__(self, msg,id):
        self.mail=msg
        self.id=id
        try:
            self.subject = email.header.make_header(email.header.decode_header(msg['SUBJECT']))
        except:
            self.subject=None
        try:
            self.mailFrom = email.header.make_header(email.header.decode_header(msg['FROM']))
        except:
            self.mailFrom=None

        self.body = self.getBody(msg)

        try:
            self.date=email.header.make_header(email.header.decode_header(msg['Date']))
        except:
            self.date=None

        try:
            self.attachmentList=self.getAttachmentList()
        except:
            self.attachmentList=[]
    '''
    获得邮件内容【正文】
    '''

    '''
    将文件下载到指定目录
    '''
    def getAttachmentList(self):
        attachmentList=[]
        for part in self.mail.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            attachmentList.append(filename)
        return attachmentList

    def downloadAttachments(self, attachDir):
        print("enter download")
        for part in self.mail.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            if bool(filename):
                filepath = os.path.join(attachDir, filename)
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                    print("should be wirrten")

    def readBody(self,msg):
        if msg.is_multipart():
            return self.readBody(msg.get_payload(0))
        else:
            return msg.get_payload(None, decode=True)

    def getBody(self,msg):
        subject = email.header.decode_header(msg.get('subject'))
        # subject包含文档编码
        default_code = subject[0][1]
        if default_code is None:
            default_code='utf-8'
        result=""
        # 是否multipart类型，分别处理
        ctype = msg.get_content_type()
        html=""
        if msg.is_multipart():
            pl = msg.get_payload()
            for m in pl:
                ctype = m.get_content_type()
                if 'html' in ctype:
                    # 注意decode参数，如果是True将解码base64/quoted-printable等格式编码内容，否则不解码
                    html = str(m.get_payload(decode=True), m.get('content-type').split('=')[1])
                # BeautifulSoup解析网页
                soup = BeautifulSoup(html, "lxml")
                divs = soup.select('body')
                for d in divs:
                    # 提取所有文本内容
                    text = d.get_text(strip=True)
                    result+=text
        else:
            html = str(msg.get_payload(decode=True), default_code)
            # BeautifulSoup解析网页
            soup = BeautifulSoup(html, "lxml")
            # 提取body标签里面的所有文本内容
            divs = soup.select('body')
            for d in divs:
                text = d.get_text(strip=True)
                result+=text
        return result
    def getBody2(self,e):
        print("echo1")
        mail_content=""
        maintype = e.get_content_maintype()
        if maintype == 'multipart':
            for part in e.get_payload():
                if part.get_content_maintype() == 'text':
                    mail_content = part.get_payload(decode=True).strip()
        elif maintype == 'text':
            mail_content = e.get_payload(decode=True).strip()
        return mail_content
