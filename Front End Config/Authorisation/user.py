# Importing Modules
#===============================================================
import os 
import sys
import uuid
import pickle
from cryptography.fernet import Fernet
sys.path.insert(0,'../FRONT END CONFIG')
from Configurations.database_creds import *
from Database.database import MySQL_Database
from Authorisation.validation import  Eamil_validation
#================================================================


class Login : 

    def __init__(self , email = '' , password = '') : 
        try : 
            self.status = True 
            self.result = True
            self.email = email 
            self.password = password
        except Exception as e : 
            self.status = False 
            print(e)

    def input_validation(self) : 
        try : 
            email_validatior = Eamil_validation(self.email)
            result = email_validatior.email_validation()
            if not result : 
                self.message = email_validatior.message 
                return result
        
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

    
    def user_validation(self):
        """
        User Validation
        ===============
        
        Functionality
        -------------
        This method is responsible to perform the user validation

        Parameters
        ----------
        1. self : Class variables

        Constraints
        -----------
        Nan

        Asymptotic Analysis
        -------------------
        1. Time Complexity :  Theta(c) where c belongs to constant.
        2. Space Complexity : Theta(c) where c belongs to constant. 
        3. Auxiliary Space Complexity : Theta(c) where c belongs to constant. 

        """
        try : 
            self.db = MySQL_Database(config_credentials , logger_flag=False)
            self.db.connection_attempt() 

            self.query = '''select count(1) from {} where `Mail Id` = '{}'; '''.format( user_details, self.email)
            count = self.db.sql_query( self.query)[0][0]
            if(count == 1):
                self.query = '''select `Password`, `Name`, `Mail Id`, `Access` from {} where `Mail Id` = '{}';'''.format(user_details,self.email)
                print(self.query)
                self.result = self.db.sql_query(self.query)[0]
                print(self.result)
                self.db_password = self.result[0]
                if(self.password == self.fernet.decrypt(self.db_password.encode()).decode()):
                    
                    # Token Generation Code
                    self.token = str(uuid.uuid4())
                    self.query = '''update {} set token = '{}'  where `Mail Id` = '{}' '''.format(user_details,self.token , self.email)
                    print(self.query)
                    self.db.update_query(self.query)
                    return True
                else:
                    self.message = 'Invalid Password'
                    return False

            
            elif(count == 0):
                self.message = 'Invalid Usernmae'
                return False
            
            else : 
                self.message = 'More than one user Id found'
                return False



        except Exception as e :
            self.status = False 
            print(e) 

    def pipeline(self) : 
        try : 
            result = self.input_validation() 
            if(not result):
                if( not self.status):
                    raise(Exception('Error in Input validation'))
                
                return False 
            
            self.encryption_initialization() 

            result = self.user_validation()
            if(not result) :
                if( not self.status ):
                    raise(Exception('Error in User validation'))
                return False 
            
            if(not self.status):
                raise(Exception('Error'))
            
            return True

        except Exception as e : 
            self.status = False
            print(e) 


class Get_access():
    
    def __init__(self, token) : 
        try : 
            self.status = True
            self.token = token
        except Exception as e : 
            self.status = False 
            print(e)


    def get_access(self) : 
        try : 
            self.db = MySQL_Database(config_credentials , logger_flag=False)
            self.db.connection_attempt()

            self.query = '''select Access from {} where `Token` = '{}'; '''.format( user_details, self.token)
            print(self.query)
            access = self.db.sql_query( self.query)[0][0].split(',')
            print(access)

            read = False
            write = False
            update = False 
            delete = False
            admin = False 

            for i in access : 
                if(i.lower().strip() == 'read'):
                    read = True 
                if(i.lower().strip() == 'write'):
                    write = True
                if(i.lower().strip() == 'update'):
                    update = True
                if(i.lower().strip() == 'delete'):
                    delete = True
                if(i.lower().strip() == 'admin'):
                    admin = True
                    read = True
                    write = True 
                    update = True 
                    delete = True
            
            return read, write, update, delete, admin

        except Exception as e : 
            self.status = False 
            print(e)
