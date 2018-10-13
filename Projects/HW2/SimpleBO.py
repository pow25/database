import pymysql
import json

cnx = pymysql.connect(host='localhost',
                              user='root',
                              password='zhangchi25',
                              db='lahman2017raw',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

def run_q(q, args, fetch=False):
    cursor = cnx.cursor()
    try:
        cursor.execute(q, args)
    except Exception as e:
        raise e
    
    if fetch:
        result = cursor.fetchall()
    else:
        result = None
    cnx.commit()
    return result

def template_to_where_clause(t):
    s = ""
    if t is None:
        return s

    for (k, v) in t.items():
        if s != "":
            s += " AND "
        s += k + "='" + v[0] + "'"

    if s != "":
        s = "WHERE " + s

    return s

def templateToInsertClause(t):
    if t is None:
        return ""
    
    s = "("
    keys = t.keys()
    count = 0
    for i in keys:
        s += i
        count += 1
        if count != len(keys):
            s += ","
    
    s += ") VALUES ("
    count = 0
    for i in keys:
        s += "'" + t[i] + "'"
        count += 1
        if count != len(keys): 
            s += ","
    s+= ")"

    return s


def find_by_template(table, t, limit=None, offset=None, fields=None): 
    if t == None or table == None:
        raise ValueError("The table or input template is empty")
    
    w = template_to_where_clause(t)

    if fields == None:
        q = "SELECT * FROM " + table + " " + w
    else:        
        fields_string = ""
        for i in fields:
            fields_string += i + ","
        fields_string = fields_string[:-1]

        q = "SELECT " + fields_string + " FROM " + table + " " + w 

    if limit == None and offset == None:
        q += ";"
    elif limit != None and offset == None:
        q += "LIMIT " + str(limit) + ";"
    elif limit == None and offset != None:
        q += "LIMIT " + str(10) + "OFFSET " + str(offset) + ";"
    else:
        q += "LIMIT " + str(limit) + "OFFSET " + str(offset) + ";"
    
    try:
        result = run_q(q, None, True)
    except Exception as e:
        raise e
    
    return result


def insert(table, t):

    if t == None or table == None:
        raise ValueError("The table or input template is empty")

    w = templateToInsertClause(t)
    q = "INSERT INTO " + table + " " + w + ";"
    try:
        run_q(q, None)
    except Exception as e:
        raise e


def delete(table, t):

    if t == None or table == None:
        raise ValueError("The table or input template is empty")

    w = template_to_where_clause(t)
    q = "DELETE FROM " + table + " " + w + ";"
    
    try:
        run_q(q, None)
    except Exception as e:
        raise e