#!/usr/bin/python
import re
from Printer import Printer


class MenuBox(object):

    def __init__(self, name, logPath, withexitopt=1):
        self.__Name = name
        self.logObj = Printer(logPath)
        self.optionList = []
        self.withExit = withexitopt

    def addOption(self, optionText):
        self.optionList.append(optionText)

    def addOptions(self, optionslist):
        self.optionList += optionslist

    def dispMenu(self):
        counter = 1
        self.logObj.printer(self.__Name)
        self.logObj.printer("-" * len(self.__Name))
        for i in self.optionList:
            self.logObj.printer(str(counter) + ": " + i)
            counter += 1
        if self.withExit == 1:
            self.logObj.printer(str(counter) + ": " + "Exit")
       
    def simulate(func):
        def wrapper(self, option=0): return func(self, 1)
        return wrapper  
    
    def getoptioncount(self):      
        return len(self.optionList) + self.withExit

    #@simulate
    def runMenu(self, option=0):
        if option != 0:
            self.dispMenu()
            self.logObj.printer("\nAutomatic selection of option #%d" % option)
            return option
        else:
            selection = 0
            while selection == 0:
                self.dispMenu()
                inp = raw_input("Select an option: ")
                self.logObj.printer("")
                matchObj = re.match(r'^(\d+)$', inp, re.M | re.I)
                if matchObj:
                    if 1 <= int(matchObj.group(1)) <= (len(self.optionList) + self.withExit):
                        selection = int(inp)
                        self.logObj.printer("You selected option #%s" % inp)
                    else:
                        self.logObj.printer("You entered %s, please enter valid option." % inp)
                else:
                    self.logObj.printer("You entered %s, please enter valid option." % inp)
            return selection       
