import pymysql
import json

cnx = pymysql.connect(host='localhost',
                              user='dbuser',
                              password='dbuser',
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

def body_to_update_clause(t):
    s = ""
    if t is None:
        return s

    for (k, v) in t.items():
        if s != "":
            s += ", "
        s += k + "='" + v + "'"

    if s != "":
        s = " SET " + s

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

def parse_primary_key(table,inputs):
    return_dict = {}
    q = "SHOW KEYS FROM " + table + " WHERE Key_name = 'PRIMARY';"

    inputs_primary_keys = inputs.split('_')
    try:
        result = run_q(q, None, True)
    except Exception as e:
        raise e
    
    if len(inputs_primary_keys) != len(result):
        raise ValueError("The primary key's number dosen't match the database")

    for i in range(len(inputs_primary_keys)):
        return_dict[result[i]['Column_name']] = [inputs_primary_keys[i]]
    
    return return_dict

def get_foreign_key(table,inputs):
    referene_column_name = []
    q = "SELECT TABLE_NAME,COLUMN_NAME,CONSTRAINT_NAME, REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME FROM \
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME = '" + table + "' ;"
    print(q)
    try:
        result = run_q(q, None, True)
    except Exception as e:
        raise e
    inputs = inputs[0]
    inputs =  {k.lower(): v for k, v in inputs.items()}

    for i in result:
        if i['REFERENCED_TABLE_NAME'] != None:
            referene_column_name.append(i['REFERENCED_COLUMN_NAME'])


    result_dict = {}

    for i in referene_column_name:

        result_dict[i] = [inputs[i]]

    return result_dict

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


def update(table, t, body):
    if t == None or table == None:
        raise ValueError("The table or input template is empty")
    
    w = template_to_where_clause(t)
    v = body_to_update_clause(body)
    q = "UPDATE " + table + v + " " + w +";"
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

def career_stats(inputs):
    q = "CREATE OR REPLACE VIEW career_stats AS \
    select batting.playerID, batting.teamID, batting.yearID, G_all, H as hits, AB as ABs, A, E as Errors \
    from batting join fielding on batting.playerid = fielding.playerid and batting.yearID = fielding.yearID and batting.teamID = fielding.teamID \
    join appearances on appearances.playerid = batting.playerid and appearances.yearID = batting.yearID and appearances.teamID = batting.teamID;"
    try:
        run_q(q, None)
    except Exception as e:
        raise e

    q = "SELECT playerID, teamID, yearID, G_all, hits, sum(A) as Assists, Errors from career_stats where playerID = '" + inputs + "' group by yearID;"
    try:
        res = run_q(q, None,True)
    except Exception as e:
        raise e
    return res

def teammate(inputs):
    q = "with team as (select distinct teamID from Appearances where playerID='" + inputs + "'), \
    years as (select distinct yearID from Appearances where playerID='" + inputs + "'), \
    teammates(teammateID,t_yearID) as (select playerID,yearID from Appearances \
    where teamID in (select * from team) and yearID in (select * from years)) \
    select '" + inputs + "' as playerID, teammateID, min(t_yearID) as first_year, \
    max(t_yearID) as last_year , count(t_yearID) as seasons from teammates group by teammateID order by teammateID;"
    
    try:
        res = run_q(q, None,True)
    except Exception as e:
        raise e

    return res

def roster(t):

    q = "CREATE OR REPLACE VIEW roster AS \
    select nameLast, nameFirst, people.playerID, appearances.teamID, appearances.yearID, G_all, H as hits, AB as abs, A, E \
    from people join appearances on people.playerid = appearances.playerid \
    join batting on people.playerID = batting.playerID and batting.yearID = appearances.yearID and appearances.teamID = batting.teamID \
    join fielding on people.playerID = fielding.playerID and batting.yearID = fielding.yearID and batting.teamID = fielding.teamID \
    order by playerID;"
    
    try:
        run_q(q, None)
    except Exception as e:
        raise e
    w = template_to_where_clause(t)
    
    q = "select nameLast, nameFirst, playerID, teamID, yearID, G_all, hits, abs, sum(A) as attempts, sum(E) as errors from roster " \
    + w + " group by playerID;" 
    
    try:
        res = run_q(q, None,True)
    except Exception as e:
        raise e
    
    return res