# Importing Modules
#============================================================================
import os 
import sys
import pickle
from cryptography.fernet import Fernet
sys.path.insert(0,'../FRONT END CONFIG')
from Configurations.database_creds import *
from Database.database import MySQL_Database
from Authorisation.validation import Password_validation , Eamil_validation
#=============================================================================

class Registration : 

    '''
    This module is responsible to onboard new users.

    Language : Python
    Developed by : Bajaj health
    Developer Name : Santosh Saxena
    Date : 07/05/2023 11:36 PM IST
    Delivery of Logs : False. 
    On Failures : Print. 
    Version : 1

    '''


    def __init__(self , email , password , confirm_password):

        """
        Initialization
        ==============

        Functionality 
        -------------
        This method is responsible to initialize the necessary class variables

        Parameters
        ----------
        1. self : Class variables
        2. email : string data type, Email
        3. password : string data type, Password

        Constraints
        -----------
        Nan 

        Asymptotic Analysis
        -------------------
        1. Time Complexity : Theta(c) where c belongs to constant. 
        2. Space Complexity : Theta(c) where c belongs to constant. 
        3. Auxiliary Space Complexity : Theta(c) where c belongs to constant. 

        """

        try : 
            self.email = email 
            self.password = password 
            self.confirm_password = confirm_password 
            self.result = True
            self.status = True
            self.message = '' 
        
        except Exception as e : 
            self.status = False 
            print(e)
            # Error Mailing Functionality 
 
    def input_validation(self) : 
        """
        Input Validation
        ================

        Functionality 
        -------------
        This mehod is responsible to validate the input passed by the user. 

        Parameters
        ----------
        1. self : Class variables

        Constraints
        -----------
        Nan

        Asymptotic Analysis
        -------------------
        1. Time Complexity : Theta(c) where c belongs to constant. 
        2. Space Complexity : Theta(c) where c belons to constant. 
        3. Auxiliary Space Complexity : Theta(c) where c belongs to constant. 

        """
        try :

            email_validatior = Eamil_validation(self.email)
            result = email_validatior.email_validation()
            if not result : 
                self.message = email_validatior.message 
                return result
            
            password_validator = Password_validation(self.password)
            result = password_validator.password_validation()
            if not result : 
                self.message = password_validator.message
                return result 
            
            if(self.password != self.confirm_password):
                self.message = 'Password does not match'
                return False 
            

            return True

            
        except Exception as e :
            self.status = False 
            print(e) 
    
    def encryption_initialization(self) : 
        try : 
            self.key = pickle.load(open(os.getcwd() + '/Configurations/authorisation_key' , 'rb'))
            self.fernet = Fernet(self.key) 
        except Exception as e : 
            self.status = False 
            print(e)
        
    def onboarding(self):
        """
        Onboarding 
        ==========

        Functionality 
        -------------
        This method is responsible to add a record into database. 

        Parameters
        ----------
        1. self : Class variables

        Constraints
        -----------
        Nan 

        Asymptotic Analysis
        -------------------
        1. Time Complexity : Theta(c) where c belongs to constant. 
        2. Space Complexity : Theta(c) where c belongs to constant. 
        3. Auxiliary Space Complexity : Theta(c) where c belongs to constant. 

        """
        try : 
            self.db = MySQL_Database(config_credentials , logger_flag=False)
            self.db.connection_attempt() 

            # Checking if the user is existing or not 
            self.query = '''select count(1) from {} where `Mail Id` = '{}'; '''.format( user_details ,self.email)
            print(self.query)
            count = self.db.sql_query(self.query)[0][0]
            if(count > 0):
                self.message = 'Account already exists'
                return False
            
            self.query = '''insert into {} ( `Name`, `Mail Id`, `Password`, `Access` ) VALUES ('{}', '{}', '{}', 'Read');'''.format(user_details , ' '.join(self.email.split('@')[0].split('.')).lower() , self.email , self.fernet.encrypt(self.password.encode()).decode())
            print(self.query)
            self.db.update_query(self.query)
            self.db.close_connection()

            return True

        except Exception as e : 
            self.status = False
            print(e)


    def pipeline(self) : 
        """
        Pipeline
        ========

        Functionality
        -------------
        This method is responsible to combine all the necessary method to form an entire process 

        Parameters
        ----------
        1. self : Class variables 

        Constraints
        -----------
        Nan

        Asymptotic Analysis
        -------------------
        1. Time Complexity : Theta(c) where c belongs to constant. 
        2. Space Complexity : Theta(c) where c belongs to constant. 
        3. Auxiliary Space Complexity : Theta(c) where belongs to constant. 
        """
        try : 
            result = self.input_validation()
            if(not result):
                return False 
            self.encryption_initialization()
            result = self.onboarding()
            if(not result):
                return False 
            
            return True 


        except Exception as e : 
            self.status = False 
            print(e) 


    
        
