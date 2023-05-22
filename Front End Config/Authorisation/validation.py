import re

class Eamil_validation : 

    def __init__(self, email = '' ):
        self.email  = email
        self.message = '' 

    def email_validation(self) : 
        if(self.email.strip() == ''):
            self.message = 'Email cannot be blank'
            return False 

        elif(self.email.find('@') == -1):
            self.message = 'Email must have @'
            return False 
            
        elif(self.email.find('.in') == -1 ):
            self.message = 'Email must end with .in'
            return False 
            
        elif(self.email.find('bajajfinserv') == -1 ):
            self.message = 'Email must contain bajajfinserv'
            return False

        elif(self.email.find('.') == -1 ):
            self.message = 'Email must have atleast one .'
            return False
        
        elif( not self.email.islower() ): 
            self.message = 'Email must have all lower case characters .'
            return False 
        
        else : 
            return True 

class Password_validation : 

    def __init__(self , password = '') :
        self.password = password
        self.message = '' 

    def password_validation(self) : 
        
        if(self.password.strip() == ''):
            self.message = 'Password cannot be blank'
            return False 
        
        elif (len(self.password)<=8):
            self.message = 'Password must have more than 8 characters'
            return False 

        elif not re.search("[a-z]", self.password):
            self.message = 'Password must have atleast one lower case'
            return False 
        
        elif not re.search("[A-Z]", self.password):
            self.message = 'Password must have atleast one upper case'
            return False 
        
        elif not re.search("[0-9]", self.password):
            self.message = 'Password must have atleast one numeric letter'
            return False 
        
        elif not re.search("[^A-Za-z0-9]" , self.password):
            self.message = 'Password must have atleast one special character'
            return False 
        
        elif re.search("\s" , self.password):
            self.password = 'Password cannot have space in between'
            return False 
        else:
            return True
        
        


