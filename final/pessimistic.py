import pymysql.cursors
import json
import uuid

pymysql_exceptions = (
    pymysql.err.IntegrityError,
    pymysql.err.MySQLError,
    pymysql.err.ProgrammingError,
    pymysql.err.InternalError,
    pymysql.err.DatabaseError,
    pymysql.err.DataError,
    pymysql.err.InterfaceError,
    pymysql.err.NotSupportedError,
    pymysql.err.OperationalError)

default_db_params = {
    "dbhost": "localhost",                    # Changeable defaults in constructor
    "port": 3306,
    "dbname": "classiccars",
    "dbuser": "dbuser",
    "dbpw": "dbuser",
    "cursorClass": pymysql.cursors.DictCursor,        # Default setting for DB connections
    "charset":  'utf8mb4'                             # Do not change
}


def get_new_connection(params=default_db_params):
    cnx = pymysql.connect(
        host=params["dbhost"],
        port=params["port"],
        user=params["dbuser"],
        password=params["dbpw"],
        db=params["dbname"],
        charset=params["charset"],
        cursorclass=params["cursorClass"])
    return cnx


def run_q(cnx, q, args, fetch=False, commit=True, cursor=None):
    """
    :param cnx: The database connection to use.
    :param q: The query string to run.
    :param args: Parameters to insert into query template if q is a template.
    :param fetch: True if this query produces a result and the function should perform and return fetchall()
    :return:
    """
    #debug_message("run_q: q = " + q)
    #ut.debug_message("Q = " + q)
    #ut.debug_message("Args = ", args)
    
    result = None

    try:
        if cursor is None:
            cnx = get_new_connection()
            cursor = cnx.cursor()

        result = cursor.execute(q, args)
        if fetch:
            result = cursor.fetchall()
        if commit:
            cnx.commit()
    except pymysql_exceptions as original_e:
        #print("dffutils.run_q got exception = ", original_e)
        raise(original_e)

    return result

def get_account(id, cursor=None):
    """
    Same logic as above. Normally, there would be a single function that returned data based on
    requested fields instead of two different functions.
    """

    if cursor is None:
        cnx = get_new_connection()
        cur = cnx.cursor()
        cursor_created = True
    else:
        cursor_created = False
        cnx = None

    q = "select * from w4111final.banking_account where id=%s"
    result = run_q(cnx, q, id, fetch=True, commit=False, cursor = cursor)

    if cursor_created:
        cnx.commit()
        cnx.close()

    return result[0]

def update_balance(id, amount, cursor=None):
    cnx = None
    
    if cursor is None:
        cnx = get_new_connection()
        cursor = cnx.cursor()
        cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
        cursor_created = True
    else:
        cursor_created = False
    
    new_version = str(uuid.uuid4())
    
    q = "update w4111final.banking_account set balance=%s, version=%s where id=%s"
    result = run_q(cnx,q,(amount, new_version, id), fetch = True, commit = False, cursor = cursor)
    
    if cursor_created:
        cnx.commit()
        cnx.close()

def get_balance(id, cursor=None):
    cnx = None
    
    if cursor is None:
        cnx = get_new_connection()
        cursor = cnx.cursor()
        cursor_created = True
    else:
        cursor_created = False
    
    q = "select * from w4111final.banking_account where id=%s"
    result = run_q(cnx, q, id, fetch = True, commit = False, cursor = cursor)
    
    if cursor_created:
        cnx.commit()
        cnx.close()
    
    return result[0]['balance']

def transfer_pessimistic():
    print("transfer_pessimistic running!!!!!!")
    cnx = get_new_connection()
    cursor = cnx.cursor()
    try:
        cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
        source_id = input("Source account ID: ")
        source_b = get_balance(source_id, cursor = cursor)
        cont = input("Source balance = " + str(source_b) + ". Continue (y/n)")
        
        if cont == 'y':
            target_id = input("Target account ID:")
            target_b = get_balance(target_id, cursor = cursor)
            input("Target balance = "+ str(target_b) + ". Continue (y/n)")
            
            if cont == 'y':
                amount = input ("Amount: ")
                amount = float(amount)
                
                new_source = source_b - amount
                new_target = target_b + amount
                
                update_balance(source_id, new_source, cursor = cursor)
                update_balance(target_id, new_target, cursor = cursor)
                
                cnx.commit()
                cnx.close()
    
    except Exception as e:
        print("Exception:",e)
        cnx.rollback()
        cnx.close()
    return

transfer_pessimistic()