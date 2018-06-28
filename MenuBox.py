#!/usr/bin/python
import re
from Printer import Printer


class MenuBox(object):

    def __init__(self, name, logPath, withexitopt=1):
        self.__Name = name
        self.logObj = Printer(logPath)
        self.optionList = []
        self.withExit = withexitopt

    def getMenuBoxType(self):
        return self.withExit

    def addOption(self, optionText):
        self.optionList.append(optionText)

    def addOptions(self, optionslist):
        self.optionList += optionslist

    def dispMenu(self):
        counter = 1
        self.logObj.printer(self.__Name)
        self.logObj.printer("-"*len(self.__Name))
        for i in self.optionList:
            self.logObj.printer(str(counter) + ": " + i)
            counter += 1
        if self.getMenuBoxType() == 1:
            self.logObj.printer(str(counter) + ": " + "Exit")

    def getoptioncount(self):
        if self.getMenuBoxType() == 1:
            return len(self.optionList) + 1
        else:
            return len(self.optionList)

    def runMenu(self):
        a = 0
        selection = 0
        while a == 0:
            self.dispMenu()
            inp = raw_input("Select an option: ")
            self.logObj.printer("")
            matchObj = re.match(r'^(\d+)$', inp, re.M | re.I)
            if matchObj:
                if 1 <= int(matchObj.group(1)) <= self.getoptioncount():
                    a = 1
                    selection = int(inp)
                    self.logObj.printer("You selected option #%s" % inp)
                else:
                    self.logObj.printer("You entered %s, please enter valid option." % inp)
            else:
                self.logObj.printer("You entered %s, please enter valid option." % inp)
        return selection

    def auto_runMenu(self, option):
        a = 0
        selection = 0
        while (a == 0):
            self.dispMenu()
            inp = str(option)
            self.logObj.printer("")
            matchObj = re.match(r'^(\d+)$', inp, re.M | re.I)
            if matchObj:
                if 1 <= int(matchObj.group(1)) <= self.getoptioncount():
                    a = 1
                    selection = int(inp)
                    self.logObj.printer("You selected option #%s" % inp)
                else:
                    self.logObj.printer("You entered %s, please enter valid option." % inp)
            else:
                self.logObj.printer("You entered %s, please enter valid option." % inp)
        return selection