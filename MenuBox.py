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
            # validate the user name/password by connecting MySQL Server
            # if connection OK, then only create the object
            conn = mysql.connector.connect(user=username,
                                           password=password)
            conn.close()
        except mysql.connector.Error as err:
            raise ValueError
        except AttributeError as err:
            print(err)
            raise AttributeError
        else:
            # create the DB handling object if no exception
            self.__username = username
            self.__password = password
            # set DB name to None at initialization of object
            self.database = None

    def isDBexist(self, database):
        # make a connection with current user name/password and database
        try:
            cnxn = mysql.connector.connect(user=self.__username,
                                           password=self.__password,
                                           database=database)
            cnxn.close()
            # if connection was successful return 1
            return 1
        except mysql.connector.Error as err:
            # if any exception above print MySQL error and return -1
            # DBhandler.printError(err)
            return -1

    def createDB(self, database):
        # if DB already exists return with 0
        if self.isDBexist(database) == 1:
            return 0
        else:
            # if no such DB exist, get the connection object first
            # create a cursor object from above connection
            with cursor_cm(self.__username, self.__password) as cur:
                # Execute the SQL command to create database
                try:
                    cur.execute("CREATE DATABASE %s" % database)
                    # return 1 for successful DB creation
                    return 1
                except mysql.connector.Error as err:
                    # print the MySQL error if above raises any exception
                    DBhandler.printError(err)
                    return -1

    def dropDB(self, database):
        # if specified DB does not exist return 0
        if self.isDBexist(database) == -1:
            return 0
        else:
            # if the DB specified exists and also same is configured on the
            # DBHandler object, remove it and set database name to None
            if self.database == database:
                self.database = None
            # get the cursor object
            with cursor_cm(self.__username, self.__password) as cur:
                try:
                    # execute the command to drop the database
                    cur.execute("DROP DATABASE %s" % database)
                    # if no exception return 1
                    return 1
                except mysql.connector.Error as err:
                    # if exception above, print MySQL error and return -1
                    DBhandler.printError(err)
                    return -1

    # method for creating a table in specified database
    def createTable(self, database, tablename, columns, datatype):
        # check for database existence
        if self.isDBexist(database) != 1:
            return -1
        # create a cursor object
        with cursor_cm(self.__username, self.__password, database) as cur:
            try:
                # get the column names and their data types from function
                # arguments and write the create table MySQL command
                query1 = ", ".join([columns[i] + " " + datatype[i] for i in
                                   range(len(columns))])
                # execute the create table command
                cur.execute("CREATE TABLE %s (%s)" % (tablename, query1))
                # return 1 for successful table creation
                return 1
            except mysql.connector.Error as err:
                # print MySQL error if any exception above and return -1
                DBhandler.printError(err)
                return -1

    def queryDB(self, database, query):
        # check for database existence
        if self.isDBexist(database) != 1:
            return 
        with cursor_cm(self.__username, self.__password, database) as cur:
            try:
                # execute the query
                cur.execute(query)
                # print the query output
                return [row for row in cur]
                # if no exception in above code return 1
            except mysql.connector.Error as err:
                # if any exception print error and return -1
                DBhandler.printError(err)

    # method for modifying the specified database with insert/update command
    def insertintoDB(self, database, query):
        if self.isDBexist(database) != 1:
            return -1
        with cursor_cm(self.__username, self.__password, database) as cur:
            try:
                # execute the query
                cur.execute(query)
                # if no exception in above code return 1
                return 1
            except mysql.connector.Error as err:
                # if any exception in above code print error and return -1
                DBhandler.printError(err)
                return -1

    # static method for printing the MySQL error in more readable format
    @staticmethod
    def printError(error):
        print "ERROR: (%d) %s" % (error.errno, error.msg)
