from Configurations.process_doc import * 
from Configurations.database_creds import *
from flask import Flask, render_template, request, redirect, flash, url_for
from Authorisation.user import Login , Get_access
from Authorisation.registration import Registration
from db_operation  import DB_Operations , DB_Logging
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret key"

db = DB_Operations()
log = DB_Logging()


@app.route('/' , methods = ['GET' , 'POST'])
def login_page():
    return render_template('login.html' , message = '' , type = '')


@app.route('/login' , methods = ['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    obj = Login(email,password)
    result = obj.pipeline()
    if( not obj.status) :
        raise(Exception('Code Failed in Login'))
    else : 
        if(result) : 
            token = obj.token
            del obj
            return redirect( url_for('home' , token = token)) 
        else :
            message = obj.message 
            del obj
            flash(message)
            return render_template('login.html', message = message , type = 'failed')


@app.route('/registration' , methods = ['GET' , 'POST'])
def registration_page():
    return render_template('registration.html' , message = '' , type = '')

@app.route('/register' , methods = ['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    obj = Registration(email , password, confirm_password)
    result = obj.pipeline()
    print(result)
    print(obj.message)
    if(not obj.status) :
        raise(Exception('Code Failed in Registration'))
    else : 
        if(result):
            flash('Account Created Successfully')
            message = 'Account Created Successfully'
            del obj
            return render_template('login.html' , messaage = message , type = 'success')
        else :
            flash(obj.message)
            message = obj.message
            del obj 
            return render_template('registration.html' , message = message , type = 'failed')
            
            
@app.route('/home/<string:token>' , methods = ['GET','POST'])
def home(token = '') : 

    if( token == '') : 
        return render_template('/login.html' , message = 'Login In required', type = 'failed')
    
    if(request.method == 'POST'):
        table_name = request.form['table_name']
        
        # Get Table Details 
        db.get_columns(table_name)
        column_names = db.result
        db.select(table_name)
        data = db.result

        # Get Access of the token
        obj = Get_access( token )
        read,write,update,delete,admin = obj.get_access()


        # Logging
        log.add_logs(token, 'Read' , table_name , db.query)
        
        return render_template('home.html', objects = db.objects , column = column_names , row = data , process_list = process_list.keys() , token = token , read = read, write = write, update = update , delete = delete)
    else : 
        obj = Get_access( token )
        read,write,update,delete,admin = obj.get_access()
        # return render_template('home.html') 
        db.refresh_objects()
        return render_template('home.html', objects = db.objects , process_list = process_list.keys() , token = token , read = read, write = write, update = update , delete = delete)


@app.route('/insert/<string:token>' , methods = ['POST'])
def insert(token = ''):
    if(token == ''):
        return render_template('/login.html' , message = 'Login In required', type = 'failed')
    
    table_name = request.form['table_name']
    db.non_derived_columns(table_name)
    
    columns = db.result
    db.get_columns(table_name)
    
    schema = db.result
    db.select(table_name)
    
    data = db.result
    return render_template('insert.html' , table_name = table_name , column_list = columns , schema = schema, row = data , token = token)


@app.route('/insert_record/<string:token>' , methods = ['POST'])
def insert_record(token):
    table_name = request.form['object_name']
    print(table_name)

    # Access Validation
    obj = Get_access(token)
    read,write,update,delete,admin = obj.get_access()

    if(write or admin):
        pass
    else : 
        message = 'You do not have Write Access'
        flash(message)
        return render_template('home.html' , objects = db.objects , type = 'failed' , message = message , process_list = process_list.keys() , token = token , read = read, write = write, update = update , delete = delete)    


    db.non_derived_columns(table_name)
    columns = db.result
    values = []

    for i in columns:
        value = request.form[i]
        values.append(value)
    
    print(columns , values)
    
    db.refresh_objects()

    db.insert(table_name , columns , values)

    print('This is the insert query',db.query)

    # Logging
    log.add_logs(token, 'Write' , table_name , db.query)
    
    if(db.e == ''):
        message = 'Insertion Successful'
        flash(message)
        # db.log_entry(token , db.query, table_name)
        return render_template('home.html' , message = message , objects = db.objects , type = 'success' , process_list = process_list.keys() , token = token , read = read, write = write, update = update , delete = delete) 
    
    else : 
        flash(db.e)
        return render_template('home.html' , message = db.e , objects = db.objects , type = 'failed', process_list = process_list.keys(), token = token , read = read, write = write, update = update , delete = delete)


@app.route('/delete/<string:token>' , methods = ['POST'])
def delete(token):

    # Fetch Details
    table_name = request.form['table_name']
    id = request.form['Id']
    
    
    # Access Validation
    obj = Get_access(token)
    read,write,update,delete,admin = obj.get_access()

    if(delete or admin):
        pass 
    else : 
        message = 'You do not have Delete Access'
        flash(message)
        return render_template('home.html' , objects = db.objects , type = 'failed' , message = message , process_list = process_list.keys() , token = token , read = read, write = write, update = update , delete = delete)    

    
    print(table_name)
    print(id)
    db.delete(table_name , id)

    # Logging
    log.add_logs(token, 'Delete' , table_name , db.query)
    

    if(db.e == ''):
        message = 'Deletion Successful'
        flash(message)
        # db.log_entry(token , db.query, table_name)
        return render_template('home.html' , message = message , type = 'success' , objects = db.objects , process_list = process_list.keys() , token = token , read = read, write = write, update = update , delete = delete)
    else : 
        message = db.e
        flash(message)
        return render_template('home.html' , message = message , type = 'failed' , objects = db.objects , process_list = process_list.keys() , token = token , read = read, write = write, update = update , delete = delete)


@app.route('/update/<string:token>' , methods = ['POST'])
def update(token):

    # Fetch Details
    table_name = request.form['table_name']
    id = request.form['Id']
    

    # Access Validation
    obj = Get_access(token)
    read,write,update,delete,admin = obj.get_access()
    
    db.get_columns(table_name)
    columns = db.result
    
    db.get_record(table_name , id)
    previous_values = db.result
    
    print(previous_values)
    
    db.get_columns(table_name)
    column_names = db.result
    
    db.select(table_name)
    data = db.result

    return render_template('update.html' , table_name = table_name , id = id , columns = columns , len = len(columns) , previous_values = previous_values , schema = column_names , row = data , token = token)


@app.route('/update_record/<string:token>' , methods = ['POST'])
def update_record(token):

    table_name = request.form['table_name']
    id = request.form['Id']
    print(table_name)
    
    # Access Validation
    obj = Get_access(token)
    read,write,update,delete,admin = obj.get_access()

    if(update or admin):
        pass 
    else : 
        message = 'You do not have Update Access'
        flash(message)
        return render_template('home.html' , objects = db.objects , type = 'failed' , message = message , process_list = process_list.keys() , token = token , read = read, write = write, update = update , delete = delete)    

    
    db.get_columns(table_name)
    columns = db.result
    
    db.get_record(table_name , id)
    previous_values = db.result
    
    latest_values = []
    for i in columns:
        latest_values.append(request.form[i])
    
    db.refresh_objects()
    db.update_record(table_name, id , columns , previous_values, latest_values)
    
    print(db.query)

    # Logging
    log.add_logs(token, 'Update' , table_name , db.query)
    
    
    if(db.e == ''):
        message = 'Update Successful'
        flash(message)
        # db.log_entry(token , db.query, table_name)
        return render_template('home.html' , message = message , type = 'success' , objects = db.objects , process_list = process_list.keys() , token = token , read = read, write = write, update = update , delete = delete)
    else : 
        return render_template('home.html' , message = message , type = 'failed' , objects = db.objects , process_list = process_list.keys() , token = token , read = read, write = write, update = update , delete = delete)


@app.route('/process/<string:token>' , methods = ['POST'])
def process_ingestion(token):
    process = request.form['table_name']
    details = process_list[process]
    
    print(process , details)
    print(len(details['schema']))
    
    return render_template('process.html' , process = process , count = len(details['schema']), table_name = details['table_name'] , schema = details['schema'] , options = details['options'] , comments = details['comments'] , token = token )

@app.route('/process_entry/<string:token>', methods = ['POST'])
def process_entry(token):

    # Access Validation
    obj = Get_access(token)
    read,write,update,delete,admin = obj.get_access()
    
    db.refresh_objects()

    table_name = request.form['table_name']
    process_name = request.form['process_name']
    
    columns = []
    values = []
    
    for i in process_list[process_name.strip()]['schema']:
        columns.append(i)
        values.append(request.form[i])
        print(request.form[i].strip())
    db.insert(table_name , columns , values)

    # Logging
    log.add_logs(token, 'Write' , table_name , db.query)
    
    
    if(db.e == ''):
        # db.log_entry(token , db.query)
        message = 'Insertion Successful'
        flash(message)
        return render_template('home.html' , message = message , objects = db.objects , type = 'success' , process_list = process_list.keys() , token = token , read = read, write = write, update = update , delete = delete) 
    else : 
        flash(db.e)
        return render_template('home.html' , message = db.e , objects = db.objects , type = 'failed', process_list = process_list.keys() , token = token , read = read, write = write, update = update , delete = delete)


@app.route('/sql_editor/<string:token>' , methods = ['GET','POST'])
def sql_editor(token):
    db.refresh_objects()
    return render_template('sql_editor.html', token = token , objects = db.objects , query = '')

@app.route('/sql_editor_object/<string:token>' , methods = ['GET','POST'])
def sql_editor_object(token):
    table_name = request.form['table_name']
    db.get_columns(table_name)
    result = db.result
    column_list =  '\n,'.join(list(map(lambda i : '`' + i + '`' , result)))
    query = 'SELECT \n\n' + column_list + '\n\nFROM {}'.format(table_name)
    
    db.refresh_objects()
    return render_template('sql_editor.html', token = token , objects = db.objects , query = query)

@app.route('/sql_query/<string:token>' , methods = ['POST'])
def sql_query(token):

    # Access Validation
    obj = Get_access(token)
    read,write,update,delete,admin = obj.get_access()
    
    db.refresh_objects()

    query = request.form['query'].replace('\n',' ').replace('\t' , ' ')
    db_conn = mysql.connector.connect(
            host = database_credentials['host']
            ,user = database_credentials['user']
            ,password = database_credentials['password']
            ,database = database_credentials['database']
            )
    cursor = db_conn.cursor()
    message = ''
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        
        # Logging
        log.add_logs(token, 'Manual' , 'Manual' , query)
    
    except Exception as e:
        message = e
        print(e)
        flash(message)
        return render_template('home.html' , objects = db.objects , type = 'failed' , message = message , process_list = process_list.keys() , token = token , read = read, write = write, update = update , delete = delete)


    if(result == []):
        db_conn.commit()
        cursor.close()
        db_conn.close()
        # db.log_entry(token , query)
        message = 'Query Executed Successfully'
        flash(message)
        return render_template('home.html', objects = db.objects, type = 'success' , message = message , process_list = process_list.keys() , token = token , read = read, write = write, update = update , delete = delete)    
    else : 
        columns = list(map(lambda x: x[0], cursor.description))
        db_conn.commit()
        cursor.close()
        db_conn.close()
        message  = 'Query Executed Successfully'
        flash(message)
        return render_template('home.html', objects = db.objects , type = 'success' , message = message ,column = columns , row = result , process_list = process_list.keys() , token = token , read = read, write = write, update = update , delete = delete) 

        
    



app.run(debug = True)

