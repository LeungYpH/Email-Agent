
import sys
import qdarkstyle
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Model import *


class LoginWindow(QWidget):
    loadInfoSig=pyqtSignal(str,str)
    # loginSig=pyqtSignal()
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.initUI()
        self.setWindowTitle("Login")
    def initUI(self):
        self.welcomeLabel=QLabel("Welcome!")
        self.userLabel=QLabel("User:",self)
        self.passwordLabel=QLabel("Password",self)
        self.userText=QLineEdit(self)
        self.passwordText=QLineEdit(self)
        self.loginButton=QPushButton("Login",self)
        self.loginButton.clicked.connect(self.login)
        self.grid=QGridLayout()
        self.grid.addWidget(self.welcomeLabel,0,0)
        self.grid.addWidget(self.userLabel,1,0)
        self.grid.addWidget(self.userText,1,1)
        self.grid.addWidget(self.passwordLabel, 2, 0)
        self.grid.addWidget(self.passwordText, 2, 1)
        self.grid.addWidget(self.loginButton, 3, 2)
        self.setLayout(self.grid)
    def login(self):
        self.loadInfoSig.emit(self.userText.text(),self.passwordText.text())
        # self.loginSig.emit()
    def showConnectError(self):
        QMessageBox.information(self, "Connect Error", "Fail to connect the server, check your Server and Internet", QMessageBox.Ok)
    def showLoginError(self):
        QMessageBox.information(self, "Login Error", "Fail to login, check your ID and password as well as the Internet connection", QMessageBox.Ok)

class MainWindow(QWidget):
    basicSig=pyqtSignal(str,str,str)#subject, to, content
    attachSig=pyqtSignal(str)#filePath
    newMailSig=pyqtSignal()
    showMailSig=pyqtSignal(str)
    def __init__(self,user,mailDict):
        super().__init__()
        print("before initUI")
        self.initUI(user,mailDict)

    def initUI(self,user,mailDict):
        self.hbox = QHBoxLayout(self)

        self.initLeftPart()
        print("before initMidPart(mailDict)")
        self.initMidPart(mailDict)
        self.initRightPart(user)

        self.splitter1 = QSplitter(Qt.Horizontal)
        self.splitter1.addWidget(self.leftFrame)
        self.splitter1.addWidget(self.mailScroll)
        self.splitter1.addWidget(self.rightFrame)

        # self.setPalette(self.icon)
        self.hbox.addWidget(self.splitter1)
        self.setLayout(self.hbox)



        self.center()
        self.setWindowTitle('Y-Mail')
        # self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setGeometry(500,300,500,300)
        self.show()

    def initLeftPart(self):
        self.leftFrame = QFrame(self)
        self.leftFrame.setFrameShape(QFrame.StyledPanel)

        self.sendButton = QPushButton("+New Mail", self)
        self.receiveButton = QPushButton("Mail Box", self)
        self.sendButton.clicked.connect(self.intoNewMail)
        self.leftFrameLayout = QGridLayout()
        self.leftFrameLayout.addWidget(self.sendButton, 0, 0)
        self.leftFrameLayout.addWidget(self.receiveButton, 1, 0)
        self.leftFrame.setLayout(self.leftFrameLayout)

        self.query_result = QTableWidget()
        self.leftFrameLayout.addWidget(self.query_result, 9, 0)
        self.query_result.verticalHeader().setVisible(False)
    def initMidPart(self,mailDict):
        self.midFrame = QFrame(self)
        self.midFrame.setFrameShape(QFrame.StyledPanel)
        self.midFrameLayout = QGridLayout(self)
        # self.sendButton
        print("echo1")
        self.mailScroll = QScrollArea(self)  # widget
        # self.mailScroll.setFrameShape(QFrame.Shape)
        self.mailScroll.setWidgetResizable(True)
        scrollAreaWidgetContents = QWidget()
        vLayout = QVBoxLayout(scrollAreaWidgetContents)
        self.mailBlocks = QListWidget()
        print("echo2")
        self.mailBlocks.setObjectName("Mails")
        self.buildMailBlock(mailDict)
        print("echo3")
        '''
        key
        '''
        vLayout.addWidget(self.mailBlocks)
        # vLayout.addWidget(btntest3)  # vlayout to add widgets ???????????????qlistwiget??????vlayout
        print("echo4")

        # self.mailScroll.widgetResizable(True)
        scrollAreaWidgetContents.setLayout(vLayout)
        self.mailScroll.setWidget(scrollAreaWidgetContents)
        self.mailScroll.sizeHint()
        self.midFrameLayout.addWidget(self.mailScroll)
        self.midFrame.setLayout(self.midFrameLayout)
        self.mailBlocks.clicked.connect(self.check)  # ???????????????????????????
        '''''
            ??????????????????
            '''
        # ?????????ContextMenuPolicy?????????Qt.CustomContextMenu
        # ??????????????????customContextMenuRequested??????
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        # ??????QMenu
        self.contextMenu = QMenu(self)
        self.actionA = self.contextMenu.addAction('delete')

        # ????????????
        self.customContextMenuRequested.connect(self.showContextMenu)

        # ????????????menu
        self.contextMenu.triggered[QAction].connect(self.remove)



    def showContextMenu(self):
        #??????????????????????????????????????????
        print("click")
        items=self.mailBlocks.currentItem()

        # print()
        if items:
          self.contextMenu.show()
          self.contextMenu.exec_(QCursor.pos())  # ?????????????????????
    def remove(self,qAction):
        print(self.f)
        self.mailBlocks.removeItemWidget(self.mailBlocks.takeItem(self.f))  #??????

    def check(self,index):
        r=index.row()
        self.f=r
        r=r+1
        print(r)

        self.showMailSig.emit(str(r))
    def buildMailBlock(self,mailDict):
        print("echo5")
        for mail in mailDict.values():
            print("echo: in loop...")
            item = QListWidgetItem()  # ??????QListWidgetItem??????
            item.setText((mail.id).decode())
            item.setSizeHint(QSize(200, 80))  # ??????QListWidgetItem??????
            widget = self.get_item_widget(mail)  # ?????????????????????????????????
            print("echo:11")
            self.mailBlocks.addItem(item)  # ??????item
            self.mailBlocks.setItemWidget(item, widget)  # ???item??????widget
    def get_item_widget(self,mail):

        # print(mail)
        # print(mail.subject)
        if mail.subject is None:
            mailTitle="No Title"
        else:
            mailTitle=mail.subject

        mailFrom=mail.mailFrom

        if mail.date is None:
            mailDate="Unknown"
        else:
            mailDate=mail.date
        # ???Widget

        widget = QWidget()
        # ??????????????????
        layout_main = QHBoxLayout()
        print("echo 6")
        print(mailFrom)
        print(mailTitle)
        print(mailDate)

        layout_left = QVBoxLayout()
        print("echo 7")
        layout_left.addWidget(QLabel(str(mailFrom)))
        print("echo8")
        layout_left.addWidget(QLabel(str(mailTitle)))
        # layout_left.addWidget(QLabel(mailDate))


        # ??????????????????, ????????????????????????
        layout_main.addLayout(layout_left)
        print("echo9")
        layout_main.addWidget(QLabel(str(mailDate)))  # ?????????????????????
        print("echo 10")
        widget.setLayout(layout_main)  # ?????????wight
        return widget  # ??????wight
    def initRightPart(self,user):
        self.mailContainer=QWidget()
        self.readyContainer=QWidget()
        self.initMailWindow(user)
        self.initReadyWindow()
        self.rightFrame = QFrame(self)
        self.rightFrame.setFrameShape(QFrame.StyledPanel)
        self.changeFrame=QStackedWidget()
        self.palette = QPalette()
        self.icon=QPixmap('./readyView.jpg')
        self.palette.setBrush(self.backgroundRole(),QBrush(self.icon))
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap("./readyView.jpg")))
        self.readyContainer.setPalette(self.palette)
        self.changeFrame.addWidget(self.readyContainer)
        # self.changeFrame.setPalette(self.palette)
        self.changeFrame.addWidget(self.mailContainer)
        self.changeFrame.setCurrentIndex(0)
        self.inter=QVBoxLayout()
        self.inter.addWidget(self.changeFrame)
        self.rightFrame.setLayout(self.inter)
        self.rightFrame.setPalette(self.palette)
        self.rightFrame.setLayout(self.rightFrameLayout)
    def initReadyWindow(self):
        # self.ReadyFlag=QLabel("Readdyyyyy")

        self.readyLayout=QVBoxLayout()
        # self.readyLayout.addWidget(self.ReadyFlag)
        self.readyContainer.setLayout(self.readyLayout)


    def initMailWindow(self,user):
        self.userLabel = QLabel("From: ")
        self.userText = QLineEdit(user)
        self.userText.setEnabled(False)
        self.recvLabel = QLabel("To: ")
        self.recvText = QLineEdit()
        self.subjectLabel = QLabel("Subject: ")
        self.subjectText = QLineEdit()
        self.contentLabel = QLabel("Content: ")
        self.contentField = QTextEdit()


        self.rightFrameLayout = QGridLayout()
        self.attachButton = QPushButton("Attach")
        self.attachButton.clicked.connect(self.openfile)
        self.attachLine = QLineEdit()
        self.attachLine.setEnabled(False)
        self.deliverButton = QPushButton("Deliver")
        self.deliverButton.clicked.connect(self.emitMail)
        self.newMailLayout=QGridLayout()
        self.newMailLayout.addWidget(self.userLabel,0,0)
        self.newMailLayout.addWidget(self.userText, 0, 1)
        self.newMailLayout.addWidget(self.recvLabel, 1, 0)
        self.newMailLayout.addWidget(self.recvText, 1, 1)
        self.newMailLayout.addWidget(self.subjectLabel, 2, 0)
        self.newMailLayout.addWidget(self.subjectText, 2, 1)
        self.newMailLayout.addWidget(self.contentLabel,3,0)
        self.newMailLayout.addWidget(self.contentField,3,1,5,1)
        self.newMailLayout.addWidget(self.attachButton,9,0)
        self.newMailLayout.addWidget(self.attachLine,9,1)
        self.newMailLayout.addWidget(self.deliverButton,10,1)
        self.mailContainer.setLayout(self.newMailLayout)
    def resetMail(self):
        self.recvText.setText("")
        self.attachLine.setText("")
        self.contentField.setText("")
        self.subjectText.setText("")

    def openfile(self):
        openfile_name = QFileDialog.getOpenFileName(self,'????????????','')
        self.attachLine.setText(openfile_name[0])

        self.attachSig.emit(openfile_name[0])
        # print(openfile_name)

    def emitMail(self):
        self.basicSig.emit(self.subjectText.text(),self.recvText.text(),self.contentField.toPlainText())
    def intoNewMail(self):
        self.newMailSig.emit()
        self.changeFrame.setCurrentIndex(1)
    def center(self):
            '''
            ??????????????????
            ??????????????????
            ??????
            '''
            screen = QDesktopWidget().screenGeometry()
            size = self.geometry()
            self.move(round((screen.width() - size.width()) / 2), round((screen.height() - size.height()) / 2))

    def testPrint(self):
        print("hello world")

class MailWindow(QWidget):
    downloadSig=pyqtSignal(str,Message)
    def __init__(self,msg):
        super(MailWindow, self).__init__()
        self.initUI(msg)
        self.mail=msg
        self.setWindowTitle("Mail Content")
    def initUI(self,msg):
        self.subject=msg.subject
        if msg.subject is None:
            mailTitle="No Title"
        else:
            mailTitle=msg.subject

        mailFrom=msg.mailFrom

        if msg.date is None:
            mailDate="Unknown"
        else:
            mailDate=msg.date
        if msg.body is None:
            mailContent="No Content"
        else:
            mailContent=msg.body
        if len(msg.attachmentList)==0:
            attachment=False

        else:
            attachment=True


        self.FromLabel=QLabel(str(mailFrom))
        self.subjectLabel=QLabel(str(mailTitle))
        self.dateLabel=QLabel(str(mailDate))
        self.contentField=QTextEdit(str(mailContent))
        self.contentField
        self.contentField.adjustSize()
        self.contentField.verticalScrollBar()
        self.FromLabel.setEnabled(False)
        self.subjectLabel.setEnabled(False)
        self.dateLabel.setEnabled(False)
        self.contentField.setEnabled(False)



        self.contentGround=QScrollArea()
        self.contentGround.setWidgetResizable(True)
        self.contentGround.setWidget(self.contentField)
        self.contentGround.sizeHint()
        self.hlayout=QHBoxLayout()
        self.vlayout=QVBoxLayout()
        self.vlayout.addWidget(self.FromLabel)
        self.vlayout.addWidget(self.subjectLabel)
        self.vlayout.addWidget(self.dateLabel)
        self.vlayout.addWidget(self.contentGround)
        if attachment:
            self.downLoadButton=QPushButton("Download")
            self.downLoadButton.clicked.connect(self.download)
            self.vlayout.addWidget(self.downLoadButton)

        self.setLayout(self.vlayout)
    def download(self):
        openfile_name = QFileDialog.getExistingDirectory(None, 'select directory', '')
        self.downloadSig.emit(str(openfile_name),self.mail)
