"""
Database Module
===============

This module is supposed to manage all the database operations


Language : Python
Developed by : Bajaj Health
Developer Name : Santosh Saxena
Date : 11/12/2022 : 1:43 AM IST 
Delivery of Logs : print function.
On Failures : Email Logging
Version : 1

"""

# Module Declaration
#---------------------
import sys
import mysql.connector
#---------------------

class MySQL_Database:

    def __init__(self, credentials = '' ,raw_logger = '' , method_logger = '' , error_logger = '' ,time_taken = '', logger_flag = True):
        """
        Initialization Method
        =====================

        Functionality
        -------------
        This metohod is supposed to connect with the database with the help of provided credentials. 

        Parameters
        ----------
        1. self : Class variable. 
        2. credentials : dictonary data type. key value pair of credentials to connect database.
        3. raw_logger : Object data type, raw_logger object to track raw level logging.
        4. method_logger : Object data type, method_logger object for method level logging. 
        5. error_logger : Object data type, error_logger object for error level logging. 
        6. logger_flag : Boolean data type, It is used to enable or disable logs.  

        Constraints
        -----------
        1. datatype of the credentials passed by the user should match with the data types documented in the parameters section.  

        Asymptotic Analysis
        -------------------
        1. Time Complexity : Theta(c) where c belongs to constant 
        2. Space Complexity : Theta(c) where c belongs to constant. 
        3. Auxiliary Space Complexity : Theta(c) where c belongs to constant. 
        """
        try:
            time_taken.start_ts() if logger_flag else ''

            raw_logger.add_logs('MySQL_Database' , 'init' , 'BEGIN') if logger_flag else ''

            raw_logger.add_logs('MySQL_Database' , 'init' , 'Constraints validation') if logger_flag else '' 
            
            constraint_result = type(credentials) != dict or (logger_flag and raw_logger == '' and method_logger == '' and time_taken == '')

            if(constraint_result):
                raw_logger.add_logs('MySQL_Database' , 'init' , 'Constraint condition FAILED') if logger_flag else ''
                raise Exception('Constraints condition failed')

            raw_logger.add_logs('MySQL_Database' , 'init' , 'Constraint condition PASSED') if logger_flag else ''
            
            
            raw_logger.add_logs('MySQL_Database' , 'init' , 'Initializing classs variables') if logger_flag else ''
            self.time_taken = time_taken
            self.raw_logger = raw_logger
            self.method_logger = method_logger
            self.logger_flag = logger_flag
            self.credentials = credentials 
            self.error_logger = error_logger
            raw_logger.add_logs('MySQL_Database' , 'init' , 'Class variables initialized') if logger_flag else '' 

            
            self.raw_logger.add_logs('MySQL_Database' , 'init' , 'PASSED') if logger_flag else ''
            self.time_taken.end_ts() if self.logger_flag else ''
            self.method_logger.add_logs('MySQL_Database','init' , time_taken.start.strftime('%H:%M:%S') , time_taken.end.strftime('%H:%M:%S') ,time_taken.milli_seconds() , status = True) if logger_flag else ''
            


        except Exception as e:
            self.raw_logger.add_logs('MySQL_Database' , 'init' , 'FAILED') if logger_flag else ''
            self.raw_logger.add_logs('MySQL_Database' , 'init' , 'Line No : {}'.format(sys.exc_info()[-1].tb_lineno)) if logger_flag else ''
            self.time_taken.end_ts() if logger_flag else ''
            self.method_logger.add_logs('MySQL_Database','init' , time_taken.start.strftime('%H:%M:%S') , time_taken.end.strftime('%H:%M:%S') ,time_taken.milli_seconds() , status = False) if logger_flag else ''
            self.error_logger.add_logs('MySQL_Database' , 'init', str(sys.exc_info()[-1].tb_lineno) , e) if logger_flag else '' 
            
        
            

    def connection_attempt(self):

        """
        Connection Attempt
        ==================
        
        Functionality
        -------------
        This function is responsible for connecting with the database. 

        Parameters
        ----------
        1.  self : Class variable

        Constraints
        -----------
        1. Connection should be succeessfull. 

        Asymptotic Analysis
        -------------------
        1. Time Complexity : Theta(c) where c belongs to constant. 
        2. Space Complexity : Theta(c) where c belongs to constant. 
        3. Auxiliary Space Complexity : Theta(c) where c belongs to constant. 
        """
        try:
            # Process Evaluation started
            self.time_taken.start_ts() if self.logger_flag else  '' 

            self.raw_logger.add_logs('MySQL_Database' , 'connection_attempt' , 'BEGIN') if self.logger_flag else ''
            self.db = mysql.connector.connect(
                host = self.credentials['host']
                ,user = self.credentials['user']
                ,password = self.credentials['password']
                ,database = self.credentials['database']
                )
            
            if(self.db):
                self.raw_logger.add_logs('MySQL_Database' , 'connection_attempt' , 'Connection SUCCESS') if self.logger_flag else ''
            else:
                self.raw_logger.add_logs('MySQL_Database' , 'connection_attempt' , 'Connection FAILED') if self.logger_flag else ''
                raise Exception('Constraints condition failed')
            
            self.cursor = self.db.cursor()
            self.raw_logger.add_logs('MySQL_Database' , 'connection_attempt' , 'Cursor Initialized') if self.logger_flag else ''

            # process evaliation ended
            self.raw_logger.add_logs('MySQL_Database' , 'connection_attempt' , 'PASSED') if self.logger_flag else ''
            self.time_taken.end_ts() if self.logger_flag else ''
            self.method_logger.add_logs('MySQL_Database','connection_attempt' , self.time_taken.start.strftime('%H:%M:%S') , self.time_taken.end.strftime('%H:%M:%S') ,self.time_taken.milli_seconds()) if self.logger_flag else ''
            
        except Exception as e:
            self.raw_logger.add_logs('MySQL_Database' , 'connection_attempt' , 'FAILED') if self.logger_flag else ''
            self.raw_logger.add_logs('MySQL_Database' , 'connection_attempt' , 'Line No : {}'.format(sys.exc_info()[-1].tb_lineno)) if self.logger_flag else ''
            self.time_taken.end_ts() if self.logger_flag else ''
            self.method_logger.add_logs('MySQL_Database', 'connection_attempt' , self.time_taken.start.strftime('%H:%M:%S') , self.time_taken.end.strftime('%H:%M:%S') ,self.time_taken.milli_seconds() , status = False) if self.logger_flag else ''
            self.error_logger.add_logs('MySQL_Database' , 'connection_attempt' , str(sys.exc_info()[-1].tb_lineno) , str(e))  if self.logger_flag else ''          
            

    def sql_query(self, query = ''):
        """
        SQL Query
        =========

        Functionality
        -------------
        This method is responsible for executing the query and providing result to the database. 

        Parameters
        ----------
        1. self : Class variable
        2. query : string data type, query that needs to be executed in  mysql to get the database. 

        Constraints 
        -----------
        1. Query should be string. 
        2. Query should not be null. 

        Asymptotic Analysis
        -------------------
        1. Time Complexity
        2. Space Complexity
        3. Auxiliary Space Complexity

        """
        try:
            self.time_taken.start_ts() if self.logger_flag else '' 
            self.raw_logger.add_logs('MySQL_Database' , 'sql_query' , 'BEGIN') if self.logger_flag else ''

            constraint_result = type(query) != str or query == ''
            if(constraint_result):
                self.raw_logger.add_logs('MySQL_Database' , 'sql_query' , 'Constraint condition FAILED') if self.logger_flag else ''
                raise Exception('Constraint condition failed')
            
            self.raw_logger.add_logs('MySQL_Database' , 'sql_query' , 'Constraint condition PASSED') if self.logger_flag else ''

            self.cursor.execute(query)
            self.raw_logger.add_logs('MySQL_Database' , 'sql_query' , 'Query Executed') if self.logger_flag else ''
            result = self.cursor.fetchall()
            self.db.commit()
            self.raw_logger.add_logs('MySQL_Database' , 'sql_query' , 'PASSED') if self.logger_flag else ''
            self.time_taken.end_ts() if self.logger_flag else ''
            self.method_logger.add_logs('MySQL_Database','sql_query' , self.time_taken.start.strftime('%H:%M:%S') , self.time_taken.end.strftime('%H:%M:%S') ,self.time_taken.milli_seconds()) if self.logger_flag else ''

            return result
            
        except Exception as e:
            self.raw_logger.add_logs('MySQL_Database' , 'sql_query' , 'FAILED') if self.logger_flag else ''
            self.raw_logger.add_logs('MySQL_Database' , 'sql_query' , 'Line No : {}'.format(sys.exc_info()[-1].tb_lineno)) if self.logger_flag else ''
            self.time_taken.end_ts() if self.logger_flag else ''
            self.method_logger.add_logs('MySQL_Database','sql_query' , self.time_taken.start.strftime('%H:%M:%S') , self.time_taken.end.strftime('%H:%M:%S') ,self.time_taken.milli_seconds() , status = False) if self.logger_flag else ''
            self.error_logger.add_logs('MySQL_Database' , 'sql_query', str(sys.exc_info()[-1].tb_lineno) , str(e)) if self.logger_flag else ''
            


    def update_query(self , query = ''):
        """
        Update Query
        =========

        Functionality
        -------------
        This method is responsible for executing the query which doed not repeat an output such as Update and Insert. 

        Parameters
        ----------
        1. self : Class variable
        2. query : string data type, query that needs to be executed in  mysql to get the database. 

        Constraints 
        -----------
        1. Query should be string. 
        2. Query should not be null. 

        Asymptotic Analysis
        -------------------
        1. Time Complexity : Theta(c) where c belongs to constant. 
        2. Space Complexity :  Theta(c) where c belongs to constant. 
        3. Auxiliary Space Complexity : Theta(c) where c belongs to constant. 

        """
        try:
            self.time_taken.start_ts() if self.logger_flag else '' 
            self.raw_logger.add_logs('MySQL_Database' , 'update_query' , 'BEGIN') if self.logger_flag else ''

            constraint_result = type(query) != str or query == ''
            if(constraint_result):
                self.raw_logger.add_logs('MySQL_Database' , 'update_query' , 'Constraint condition FAILED') if self.logger_flag else ''
                raise Exception('Constraint condition failed')
            
            self.raw_logger.add_logs('MySQL_Database' , 'update_query' , 'Constraint condition PASSED') if self.logger_flag else ''

            self.cursor.execute(query)
            self.raw_logger.add_logs('MySQL_Database' , 'update_query' , 'Query Executed') if self.logger_flag else ''
            
            self.db.commit()
            self.raw_logger.add_logs('MySQL_Database' , 'update_query' , 'PASSED') if self.logger_flag else ''
            self.time_taken.end_ts() if self.logger_flag else ''
            self.method_logger.add_logs('MySQL_Database','sql_query' , self.time_taken.start.strftime('%H:%M:%S') , self.time_taken.end.strftime('%H:%M:%S') ,self.time_taken.milli_seconds()) if self.logger_flag else ''


        except Exception as e:
            self.raw_logger.add_logs('MySQL_Database' , 'update_query' , 'FAILED') if self.logger_flag else ''
            self.raw_logger.add_logs('MySQL_Database' , 'update_query' , 'Line No : {}'.format(sys.exc_info()[-1].tb_lineno)) if self.logger_flag else ''
            self.time_taken.end_ts() if self.logger_flag else ''
            self.method_logger.add_logs('MySQL_Database','update_query' , self.time_taken.start.strftime('%H:%M:%S') , self.time_taken.end.strftime('%H:%M:%S') ,self.time_taken.milli_seconds() , status = False) if self.logger_flag else ''
            self.error_logger.add_logs('MySQL_Database' , 'update_query', str(sys.exc_info()[-1].tb_lineno) , str(e)) if self.logger_flag else ''
            

    
    def close_connection(self):
        """
        CLOSE CONNECTION
        ================
        
        Functionality
        -------------
        This method will close the connection and commit the query changes into the database. 

        Parameters
        ---------
        1. self : Class variable

        Constraints
        -----------
        Nan

        Asymptotic Analysis
        --------------------
        1. Time Complexity
        2. Space Complexity
        3. Auxiliary Space Complexity
        """
        try:
            self.time_taken.start_ts() if self.logger_flag else ''
            self.raw_logger.add_logs('MySQL_Database' , 'close_connection' , 'BEGIN') if self.logger_flag else ''
            self.cursor.close()
            self.raw_logger.add_logs('MySQL_Database' , 'close_connection' , 'Cursor Closed') if self.logger_flag else ''
            self.db.close()
            self.raw_logger.add_logs('MySQL_Database' , 'close_connection' , 'Database connection closed') if self.logger_flag else ''
            self.time_taken.end_ts() if self.logger_flag else ''
            self.method_logger.add_logs('MySQL_Database','closed_connection' , self.time_taken.start.strftime('%H:%M:%S') , self.time_taken.end.strftime('%H:%M:%S') ,self.time_taken.milli_seconds()) if self.logger_flag else ''

        except Exception as e:
            self.raw_logger.add_logs('MySQL_Database' , 'sql_query' , 'FAILED') if self.logger_flag else ''
            self.raw_logger.add_logs('MySQL_Database' , 'sql_query' , 'Line No : {}'.format(sys.exc_info()[-1].tb_lineno)) if self.logger_flag else ''
            self.time_taken.end_ts() if self.logger_flag else '' 
            self.method_logger.add_logs('MySQL_Database','closed_connection' , self.time_taken.start.strftime('%H:%M:%S') , self.time_taken.end.strftime('%H:%M:%S') ,self.time_taken.milli_seconds() , status = False) if self.logger_flag else ''
            self.error_logger.add_logs('MySQL_Database' , 'sql_query', str(sys.exc_info()[-1].tb_lineno) ,str(e)) if self.logger_flag else ''   
            