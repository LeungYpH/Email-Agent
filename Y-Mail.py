


from Controller import *
import sys

class Run():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ctrl = Controller()
    def runYMail(self):
        self.ctrl.runLogin()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    run=Run()
    run.runYMail()
