import os 
import sys
import uuid
import pickle
from cryptography.fernet import Fernet
sys.path.insert(0,'../FRONT END CONFIG')
from Configurations.database_creds import *
from Database.database import MySQL_Database
from Authorisation.validation import  Eamil_validation

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

            for i in access : 
                if(i.lower().strip() == 'read'):
                    read = True 
                if(i.lower().strip() == 'write'):
                    write = True
                if(i.lower().strip() == 'update'):
                    update = True
                if(i.lower().strip() == 'delete'):
                    delete = True
            
            return read, write, update, delete

        except Exception as e : 
            self.status = False 
            print(e)


Get_access('e5536703-ac8a-46d0-aabe-a3dff1261631').get_access()