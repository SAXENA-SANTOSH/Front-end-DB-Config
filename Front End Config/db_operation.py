from Database.database import MySQL_Database 
from Authorisation.user import  Get_access

from Configurations.database_creds import * 


class DB_Operations : 

    def __init__(self):
        self.table_name = '' 
        self.id = '' 

        self.db = MySQL_Database(database_credentials, logger_flag= False )
        self.db.connection_attempt()
        
    
    def refresh_objects(self) : 
        try : 
            self.e = ''
            query = 'SHOW TABLES'
            result = self.db.sql_query(query)
            self.objects = []
            for i in result:
                self.objects.append(i[0])

        except Exception as e : 
            self.e = e 
            print(self.e) 

    
    def select(self, table_name):
        try:
            self.e = ''
            self.table_name = table_name
            self.query = 'select * from {};'.format(table_name)
            self.db.cursor.execute(self.query)
            self.result = self.db.cursor.fetchall()
            self.db.db.commit() 

        except Exception as e :
            self.e = e 
            print(self.e)

    def get_columns(self, table_name):
        try : 
            self.e = ''
            self.table_name = table_name
            self.db.cursor.execute('desc {}'.format(table_name))
            temp =  self.db.cursor.fetchall()
            self.result = []
            for i in temp :
                self.result.append(i[0])
        
        except Exception as e:
            self.e = e 
            print(e)
    
    def non_derived_columns(self, table_name):
        try : 
            self.e = '' 
            self.table_name = table_name 
            self.db.cursor.execute("show columns from {} where Extra = ''; ".format(table_name))
            temp = self.db.cursor.fetchall() 
            self.result = [] 
            for i in temp:
                self.result.append(i[0])

        except Exception as e:
            self.e = e 
            print(e)


    def insert(self, table_name , columns , values ):
        try :
            self.e = ''
            columns = list(map(lambda i : "`" + str(i) + "`" , columns))
            self.columns = columns
            self.values = list(map(lambda i : "'" + str(i) + "'" if i != '' else 'NULL' , values)) 
            self.table_name = table_name
                
            self.query = 'insert into {} ({}) values ({}) ;'.format(self.table_name , ','.join(self.columns), ','.join(self.values))       
            self.db.cursor.execute(self.query)
            self.db.db.commit() 


        except Exception as e:
            self.e = e
            print(e)


    def delete(self, table_name , id):
        try : 
            self.e = ''
            self.table_name = table_name
            self.id = id
            query = "delete from {} where `id` = '{}' ;".format(table_name, id)
            self.query = query
            self.db.cursor.execute(query)
            self.db.db.commit()

        except Exception as e:
            self.e = e
            print(e) 
    
    def get_record(self, table_name , id) : 
        try : 
            self.e = ''
            self.table_name = table_name 
            self.id = id
            self.db.cursor.execute('select * from {} where `id` = {}'.format(table_name , id))
            temp = self.db.cursor.fetchall()[0]
            self.result = [] 
            for i in temp : 
                self.result.append(i)
            self.db.db.commit()
        except Exception as e: 
            self.e = e
            print(e)
    
    def get_details(self, token):
        try : 
            self.e = '' 
            query = "select  Name , `Mail Id` , Access from {} where token = '{}'".format(user_details,token)
            result = self.config_db.sql_query(query)[0]
            self.name =  result[0]
            self.email = result[1]
            self.access = result[2]
            return self.access
        except Exception as e : 
            self.e = e
            print(e)
    
    def update_record(self, table_name, id, columns , previous_values , latest_values):
        try:
            self.e = '' 
            self.table_name = table_name 
            self.id = id 
            self.columns = columns
            self.previous_values = previous_values
            self.latest_values = latest_values
            query = 'Update `{}` SET '.format(table_name.strip())
            for i in range(len(columns)):
                if(str(previous_values[i]) == str(latest_values[i])):
                    continue
                else:    
                    if(latest_values[i] == ''):
                        query += "`{}` = NULL  ,".format(columns[i] , latest_values[i])    
                    else:
                        query += "`{}` = '{}'  ,".format(columns[i] , latest_values[i])
            
            query = query[:-1]
            query += "where  `id` =  '{}';".format(str(id)) 
            self.db.cursor.execute(query)
            self.query = query
            self.db.db.commit() 
    
            
        except Exception as e: 
            self.e = e 
            print(e)
    

class DB_Logging : 

    def __init__(self) : 
        try : 
            self.db = MySQL_Database(config_credentials, logger_flag= False )
            self.db.connection_attempt() 
        except Exception as e : 
            print(e)


    def add_logs(self, token , type , table_name , query_used) : 
        try : 
            # Get Access of the token
            obj = Get_access( token )
            read,write,update,delete,admin = obj.get_access()
            
            read = '1' if read else '0'
            write = '1' if write else '0'
            update = '1' if update else '0'
            delete = '1' if delete else '0'
            admin = '1' if admin else '0'

            print(read, write, update,delete, admin)

            query = "select  `Name` , `Mail Id` from {} where token = '{}';".format(user_details,token)
            print(query)
            print(self.db.sql_query(query))
            result = self.db.sql_query(query)[0]

            self.name =  result[0]
            self.email = result[1]
            

            
            self.query = """insert into {} ({}) values ({}) ;""".format(log_table , log_columns, ','.join(["'{}'".format(token), "'{}'".format(self.name.strip()) , "'{}'".format(self.email.strip()) , "'{}'".format(read) , "'{}'".format(write) , "'{}'".format(update) , "'{}'".format(delete) , "'{}'".format(admin) , '"{}"'.format(type.strip()) ,"'{}'".format(table_name.strip()) ,"'{}'".format(query_used.strip().replace("'" , '"'))]))
            print(self.query)
            self.db.update_query(self.query) 

        except Exception as e : 
            print(e)
    
    def close_connection(self) : 
        try : 
            self.db.close_connection() 
        except Exception as e : 
            print(e)


