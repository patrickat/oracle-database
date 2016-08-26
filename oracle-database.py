"""
Code found on stackoverflow here: http://stackoverflow.com/a/9853319/6469907
Written by Ben (https://stackoverflow.com/users/458741/ben)
"""

import configparser
import cx_Oracle

class Oracle(object):
    def __init__(self):
        """
        Initialize the database
        """

        config = configparser.ConfigParser()
        config.read('config.ini')
        self.__connection_string = '{}/{}@{}:{}/{}'.format(
            config['Oracle'][Username],
            config['Oracle'][Password],
            config['Oracle'][Hostname],
            config['Oracle'][Port],
            config['Oracle'][Servicename]
        )

    def select(self, command):
        """
        Given a valid SELECT statement, return the results from the database
        """

        results = None

        try:
            self.__connect()
            self.__execute(command)
            results = self.__cursor.fetchall()
        finally:
            self.__disconnect()

        return results

    def __connect(self):
        """ Connect to the database. """

        try:
            self.__db = cx_Oracle.connect(self.__connection_string)
        except cx_Oracle.DatabaseError as e:
            error, = e.args

            if error.code == 1017:
                print('Please check your credentials.')
            else:
                print('Database connection error: %s'.format(e))
            # Very important part!
            raise

        # If the database connection succeeded create the cursor
        # we-re going to use.
        self.__cursor = self.__db.Cursor()
        """
        Changing arraysize changes how many rows cx_Oracle fetches from the
        database at a time.

        The following fetches 100 rows per trip
        self.__cursor.araysize = 100
        """

    def __disconnect(self):
        """
        Disconnect from the database. If this fails, for instance
        if the connection instance doesn't exist we don't really care.
        """

        try:
            self.cursor.close()
            self.db.close()
        except cx_Oracle.DatabaseError:
            pass

    def __execute(self, sql, bindvars=None, commit=False):
        """
        Execute whatever SQL statements are passed to the method;
        commit if specified. Do not specify fetchall() in here as
        the SQL statement may not be a select.
        bindvars is a dictionary of variables you pass to execute.
        """

        try:
            self.cursor.execute(sql, bindvars)
        except cx_Oracle.DatabaseError as e:
            error, = e.args

            if error.code == 955:
                print('Table already exists')
            elif error.code == 1031:
                print("Insufficient privileges")

            print(error.code)
            print(error.message)
            print(error.context)

            # Raise the exception.
            raise

        # Only commit if it-s necessary.
        if commit:
            self.db.commit()
