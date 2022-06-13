
from Model import *
import imaplib,email,os
from bs4 import BeautifulSoup

class Receiver():

    def __init__(self):
        self.imapServerDict = {
            "qq.com":"imap.qq.com",
            "outlook.com":"outlook.office365.com"
        }
    def loadInformation(self,user,password):
        self.user=user
        self.password=password
        flag_server=self.loadServer()
        print("information loaded, user:" + self.user + "\npassword: " + self.password + "\nserver: " + self.server)
        return flag_server


    # def loadIDPassword(self,id,password):
    #     self.user=id
    #     self.password=password
    #     flag_server=self.loadServer()
    #     print("information loaded, user:"+self.user+"\npassword: "+self.password+"\nserver: "+self.server)
    #     return flag_server
    def loadServer(self):
        try:
            suffix = self.user.split('@')[1]
            self.server = self.imapServerDict[suffix]
            self.connectServer()
            print("success load server")
            return True
        except:
            return False


    def connectServer(self):
        try:
            self.conn=imaplib.IMAP4_SSL(self.server)
        except:
            pass
    def userLogin(self):
        # try:
        self.conn.login(self.user,self.password)
        self.conn.select('INBOX')
        # except:
        #     raise Exception("Fail to Login, please recheck your id and password")
    def buildEmailList(self):
        result,dataid=self.conn.search(None,'from')
        self.mailIDList=dataid[0].split()
        self.mailDict={}
        for id in self.mailIDList:
            result, data = self.conn.fetch(id, '(RFC822)')
            e = email.message_from_bytes(data[0][1])
            msg=Message(e,id)
            self.mailDict.update({id:msg})

    def deleteMail(self,id):
        self.conn.store(id, '+FLAGS', '\\Deleted')
        self.conn.expunge()
        self.buildEmailList()
    # def showMailList(self):

