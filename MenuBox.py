import re
import random
import mysql.connector

class Dice(object):

    def throw_dice(self):
        out = random.randint(2, 12)
        return out
    
class Printer(object):

    def __init__(self, filename=""):
        self.LogFileName = filename

    def printer(self, inp_text):
        print inp_text
        fh = open(self.LogFileName, 'a')
        fh.write("%s\n" % inp_text)
        fh.close()

    def file_only_printer(self, inp_text):
        fh = open(self.LogFileName, 'a')
        fh.write("%s\n" % inp_text)
        fh.close()

    def set_log_file_name(self, filename, mode='w'):
        self.LogFileName = filename
        fh = open(self.LogFileName, mode)
        fh.close()

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
        self.logObj.printer("\n" + self.__Name + "\n" + "-" * len(self.__Name))
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

    # @simulate
    def runMenu(self, option=0):
        if option != 0:
            self.dispMenu()
            self.logObj.printer("\nAutomatic selection of option #%d" % option)
            return option
        else:
            selection = 0
            while selection == 0:
                self.dispMenu()
                try:
                    inp = raw_input("Select an option: ")
                    self.logObj.printer("")
                    matchObj = re.match(r'^(\d+)$', inp, re.M | re.I)
                    if matchObj:
                        if 1 <= int(matchObj.group(1)) <= (len(self.optionList) + self.withExit):
                            selection = int(inp)
                            self.logObj.printer("You selected option #%s" % inp)
                        else:
                            self.logObj.printer("Please enter valid option.")
                    else:
                        self.logObj.printer("Please enter valid option.")
                except KeyboardInterrupt:
                    self.logObj.printer("\n\nCtrl+C entered. Selecting last option as default.")    
                    return len(self.optionList) + self.withExit
            return selection       

class cursor_cm(object):

    def __init__(self, username, password, database=None):
        self.__username = username
        self.__password = password
        self.database = database

    def __enter__(self):
        self.connObj = mysql.connector.connect(user=self.__username,
                                               password=self.__password,
                                               database=self.database)
        self.cursor = self.connObj.cursor()
        return self.cursor

    def __exit__(self, *args):
        self.cursor.close()
        self.connObj.commit()
        self.connObj.close()

class DBhandler(object):
    
    def __init__(self, username, password):
        try:
            conn = mysql.connector.connect(user=username,
                                           password=password)
            conn.close()
        except mysql.connector.Error as err:
            raise ValueError
        except AttributeError as err:
            print(err)
            raise AttributeError
        else:
            self.__username = username
            self.__password = password
            self.database = None

    def isDBexist(self, database):
        try:
            cnxn = mysql.connector.connect(user=self.__username,
                                           password=self.__password,
                                           database=database)
            cnxn.close()
            return 1
        except mysql.connector.Error as err:
            return -1

    def createDB(self, database):
        if self.isDBexist(database) == 1:
            return 0
        else:
            with cursor_cm(self.__username, self.__password) as cur:
                try:
                    cur.execute("CREATE DATABASE %s" % database)
                    return 1
                except mysql.connector.Error as err:
                    DBhandler.printError(err)
                    return -1

    def dropDB(self, database):
        if self.isDBexist(database) == -1:
            return 0
        else:
            if self.database == database:
                self.database = None
            with cursor_cm(self.__username, self.__password) as cur:
                try:
                    cur.execute("DROP DATABASE %s" % database)
                    return 1
                except mysql.connector.Error as err:
                    DBhandler.printError(err)
                    return -1

    def createTable(self, database, tablename, columns, datatype):
        if self.isDBexist(database) != 1:
            return -1
        with cursor_cm(self.__username, self.__password, database) as cur:
            try:
                query1 = ", ".join([columns[i] + " " + datatype[i] for i in
                                   range(len(columns))])
                cur.execute("CREATE TABLE %s (%s)" % (tablename, query1))
                return 1
            except mysql.connector.Error as err:
                DBhandler.printError(err)
                return -1

    def queryDB(self, database, query):
        if self.isDBexist(database) != 1:
            return 
        with cursor_cm(self.__username, self.__password, database) as cur:
            try:
                cur.execute(query)
                return [row for row in cur]
            except mysql.connector.Error as err:
                DBhandler.printError(err)

    def insertintoDB(self, database, query):
        if self.isDBexist(database) != 1:
            return -1
        with cursor_cm(self.__username, self.__password, database) as cur:
            try:
                cur.execute(query)
                return 1
            except mysql.connector.Error as err:
                DBhandler.printError(err)
                return -1

    @staticmethod
    def printError(error):
        print "ERROR: (%d) %s" % (error.errno, error.msg)
