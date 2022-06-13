from Views import *
from Sender import *
from Receiver import *
class Controller():
    # _instance=None
    def __init__(self):
        self.loginWindow = LoginWindow()
        self.sender = Sender()
        self.receiver=Receiver()
    # def getSingleton(cls):
    #     if cls._instance is None:
    #         cls._instance=Controller()
    #         return cls.__init__()
    #     else:
    #         return cls._instance
    def runLogin(self):
        self.loginWindow.show()
        # try:#没用，这行的本质是连接而已，要抛出异常还是需要在内部函数中，这或许需要用到单例模式
        self.loginWindow.loadInfoSig.connect(self.checkConnect)


    def checkConnect(self,user,password):
        if not (self.sender.loadIDPassword(user,password) and self.receiver.loadInformation(user,password)):
            self.loginWindow.showConnectError()
            print("fail")
        else:
            try:
                self.sender.userLogin()
                self.receiver.userLogin()
                self.enterMainWindow()
            except:
                self.loginWindow.showLoginError()
    def enterMainWindow(self):
        print("enter MainWindow")
        self.receiver.buildEmailList()
        print(self.receiver.mailDict)
        self.mainWindow=MainWindow(self.sender.user,self.receiver.mailDict)
        self.mainWindow.show()
        self.mainWindow.basicSig.connect(self.sendMail)
        self.mainWindow.attachSig.connect(self.sender.attach)
        self.mainWindow.newMailSig.connect(self.intoNewMail)
        self.mainWindow.showMailSig.connect(self.showMailDetail)


    def showMailDetail(self,id):
        print("into showMailDetail")
        print(id)
        id=id.encode()
        msg=self.receiver.mailDict[id]
        self.createMailView(msg)



    def createMailView(self,msg):
        print("enter CreateMailview")
        self.mailview=MailWindow(msg)
        self.mailview.downloadSig.connect(self.downloadAttach)
        self.mailview.show()

    def intoNewMail(self):
        # self.mainWindow.changeFrame.setCurrentIndex(1)
        self.sender.createMail()
        print("new Mail!!!")
    def sendMail(self,subject,To,content):
        self.loadMail(subject,To,content)
        self.sender.sendMail()
        print("success sending")
        self.mainWindow.changeFrame.setCurrentIndex(0)
        self.mainWindow.resetMail()
    def downloadAttach(self,downloadPath,mail):
        mail.downloadAttachments(downloadPath)
        print(downloadPath)
        print("Downloaded")
    def loadMail(self,subject,To,content):
        self.sender.loadMail(subject,To,content)

