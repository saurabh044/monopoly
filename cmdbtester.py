import mysql.connector
import unittest
import subprocess
import re
import platform


class cursor_cm(object):
    '''
    This is context manager class for creating and closing the MySQL cursor
    of the connection object.

    Arguments:
    username: DB user name
    password: DB password
    database: DB name (optional, Default=None)

    '''

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
    '''
    This is DBHandler class

    Arguments:
    username: DB user name
    password: DB password
    '''

    def __init__(self, username, password):
        try:
            # validate the user name/password by connecting MySQL Server
            # if connection OK, then only create the object
            conn = mysql.connector.connect(user=username,
                                           password=password)
            conn.close()
        except mysql.connector.Error as err:
            # print the MySQL error on standard output
            DBhandler.printError(err)
            # if connection fails, raise ValueError exception
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
        '''
        This is method for checking if the specified database exist.

        Arguments:
        database (string): Database name

        '''
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

    def setDBname(self, database):
        '''
        This is method for setting database name to DBHandler object.

        Arguments:
        database (string): Database name

        '''
        # If the specified DB exist
        if self.isDBexist(database) == 1:
            # set the self.database to specified database
            self.database = database
        else:
            # print the error
            print "ERROR: Can not set database to \'%s\'" % database

    def getDBname(self):
        '''
        This is the method to get the database name from the DBHandler object

        No Arguments.

        '''
        return self.database

    def createDB(self, database):
        '''
        This is method for creating specified database.

        Arguments:
        database (string): Database name

        '''
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
        '''
        This is method for dropping specified database.

        Arguments:
        database (string): Database name

        '''
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
                    print "INFO: Database \'%s\' dropped." % database
                    # if no exception return 1
                    return 1
                except mysql.connector.Error as err:
                    # if exception above, print MySQL error and return -1
                    DBhandler.printError(err)
                    return -1

    def backupDB(self, database):
        '''
        This is method for taking backup of specified database.

        Arguments:
        database (string): Database name

        '''
        # if specified database exists
        if self.isDBexist(database) == 1:
            dbdump = subprocess.Popen(["mysqldump", '-u', self.__username,
                                       '-p%s' % self.__password,
                                       "--databases", database],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
            # run the command and get the output and error code
            (output, msg) = dbdump.communicate()
            # print warning message if any coming while running mysqldump
            print "WARN: %s" % msg
            # if no error, write the output in backup file
            if dbdump.returncode == 0:
                with open("%s.sql" % database, 'w') as bkp:
                    bkp.write(output)

    # method for creating a table in specified database
    def createTable(self, database, tablename, columns, datatype):
        '''
        This is method for creating a table in specified database.

        Arguments:
        database (string): Database name
        tablename (string): Table name to create
        columns (list): List of column's name (string)
        datatype (list): List of column's datatype in same order (string)

        '''
        # check for database existence
        if self.isDBexist(database) != 1:
            return -1
        # check for size of columns and data types list have equal
        # number of elements
        if len(columns) != len(datatype):
            print "ERROR: Columns name list and its data types list " \
                    "have different number of elements"
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

    # method for querying the specified database with select command
    def queryDB(self, database, query):
        '''
        This is method for query specified database.

        Arguments:
        database (string): Database name
        query (string): SELECT query as string

        '''
        # check for database existence
        if self.isDBexist(database) != 1:
            return -1
        # check if the query is MySQL select/SELECT command or not
        match = re.search(r'^\s*select\s.*', query, re.I)
        if match is not None:
            # create cursor object
            with cursor_cm(self.__username, self.__password, database) as cur:
                try:
                    # execute the query
                    cur.execute(query)
                    # print the query output
                    for row in cur:
                        print row
                    # if no exception in above code return 1
                    return 1
                except mysql.connector.Error as err:
                    # if any exception print error and return -1
                    DBhandler.printError(err)
                    return -1
        else:
            # if the query method is not select then return -1
            print "ERROR: Only select method is allowed for DB query"
            return -1

    # method for modifying the specified database with insert/update command
    def insertintoDB(self, database, query):
        '''
        This is method for updating the database with INSERT/UPDATE command.

        Arguments:
        database (string): Database name
        query (string): INSERT or UPDATE command as string

        '''
        if self.isDBexist(database) != 1:
            return -1
        # check if the command is MySQL INSERT/UPDATE command or not
        match = re.search(r'^\s*insert\s.*|^\s*update\s.*', query, re.I)
        if match is not None:
            # create a cursor object
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
        else:
            # if the query method is not INSERT or UPDATE then return -1
            print "ERROR: Only insert or update method is allowed in "\
                  "insertintoDB method"
            return -1

    # method to delete the DBHandler object
    def __del__(self):
        pass

    # static method for printing the MySQL error in more readable format
    @staticmethod
    def printError(error):
        print "ERROR: (%d) %s" % (error.errno, error.msg)
