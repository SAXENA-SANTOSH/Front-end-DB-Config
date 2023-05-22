process_list = {
    # "External Blob To Landing":{
    #                             "table_name" : "external_object_ingestion"
    #                             ,"schema" : ['Id' ,'src_storage_account' ,'src_container_name' ,'src_object_name' ,'tgt_storage_account' ,'tgt_container_name' ,'tgt_object_name' ,'is_active' ,'last_date' ,'date_column' ,'column_list']
    #                             ,"options" : ['' , ['landing' ,'central' ,'standard'] , ['a','b' , 'c'] , ['x','y','z'] , ['datalakelandingprd' , 'datalakecentralprd'  , 'datalakestandardprd'], ['aa' , 'bb' ,'cc'] , ['xx' , 'yy' , 'zz'] ,['0','1'] , '' , '' , ''] 
    #                             ,"comments" : ['Id' , 'Source storage account' , 'source container name' , 'source object name' , 'target storage account' , 'target container name' , 'target object name' , 'is active' , 'last date' , 'date column' , 'column list']
    #                             } 
    'Access Control':{
        'Access' : {'read' : True , 'write': True, 'update': True , 'delete': True }
        ,'table_name' : 'Config_Users'
        ,'schema':['Name' , 'Mail Id' , 'Password' , 'Access']
        ,'options':['' , '' , '' , ['Read' , 'Read,Write' , 'Read,Write,Update' , 'Read,Write,Update,Delete' , 'Admin']]
        ,'comments':['Name of the user' , 'Mail of the user' , 'Password of the user' , 'Access of the user']
    }
}






