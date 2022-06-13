
import smtplib
from email.mime.text import MIMEText

from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header


class Sender():
    def __init__(self):
        self.smtpServerDict={
            "qq.com":"smtp.qq.com",
            "outlook.com":"outlook.office365.com"
        }
        self.user=""
        self.password=""
    def connectServer(self):

        # if self.server not in self.smtpServerDict.values():
        #     raise Exception(self.server+"Not Support")
            # print(self.server+"Not Support")
            # print(self.smtpServerDict.keys())
        try:
            self.conn=SMTP_SSL(self.server)
            print("Connect successfully")
        except:
            # Controller().loginWindow.showConnectError()
            pass

    def userLogin(self):
        print("enter_userLogin")
        self.conn.login(self.user,self.password)
        print("login_success")

    def loadIDPassword(self,id,password):
        self.user=id
        self.password=password
        flag_server=self.loadServer()
        print("information loaded, user:"+self.user+"\npassword: "+self.password+"\nserver: "+self.server)
        return flag_server
    def loadServer(self):
        try:
            self.server = self.smtpServerDict[self.user.split('@')[1]]
            self.connectServer()
            print("success load server")
            return True
        except:
            return False
    def sendMail(self):
        self.conn.sendmail(self.user,self.recv,self.mail.as_string())

    def createMail(self):
        self.mail=MIMEMultipart()
    def loadMail(self,subject,To,content):
        self.recv=To
        self.mail["Subject"]=Header(subject,'utf-8')
        self.mail["From"]=Header(self.user,'utf-8')
        self.mail["To"]=Header(To,'utf-8')
        self.mail.attach(MIMEText(content,"plain","utf-8"))
    def attach(self,filePath):
        att1 = MIMEApplication(open(filePath, 'rb').read())
        att1.add_header('Content-Disposition', 'attachment', filename=filePath.split('/').pop())
        self.mail.attach(att1)
