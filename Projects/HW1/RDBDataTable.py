import pymysql
import json

def templateToInsertClause(t):
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

def templateToWhereClause(t):
    s = ""
    for k,v in t.items():
        if s != "":
            s += " AND "
        s += k + "='" + v + "'"

    if s != "":
        s = "WHERE " + s

    return s

class RDBDataTable():
    def __init__(self, host, user, password, db_name, table_name, key_columns ):
        # Your code goes here
        self.cnx = pymysql.connect(host= host,
                              user= user,
                              password= password,
                              db=db_name,
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.cnx.cursor()
        self.table_name = table_name
        self.key_columns = key_columns
        self.columns = []
        
        q = "SHOW columns FROM " + table_name + ";"
        self.cursor.execute(q)
        r = self.cursor.fetchall()
        for i in r:
            self.columns.append(i["Field"])

        for i in key_columns:
            if i not in self.columns:
                raise ValueError("The key_columns dones't math the database columns type")

    def find_by_primary_key(self, string_set, fields=None):
        if len(string_set) != len(self.key_columns):
            raise ValueError("The primary keys inputed didn't match the key columns")
        
        w = ""
        for i in range(0,len(string_set)):
            if w != "":
                w += " AND "
            w += self.key_columns[i] + "='" + string_set[i] + "'"
        if w != "":
            w = "WHERE " + w

        if fields == None:
            q = "SELECT * FROM " + self.table_name + " " + w + ";"
        else:
            for j in fields:
                if j not in self.columns:
                    raise ValueError("The fields don't match the database column types")
            
            fields_string = ""
            for i in fields:
                fields_string += i + ","
            fields_string = fields_string[:-1]

            q = "SELECT " + fields_string + " FROM " + self.table_name + " " + w + ";"
        
        # print ("Query = ", q)
        self.cursor.execute(q)
        r = self.cursor.fetchall()
        return r

    # The input is:
    # t: The template to match. The result is a list of rows
    # whose attribute/value pairs exactly match the template.
    # fields: A subset of the fields to include for each result.
    # Raises an exception if the template or list of fields contains
    # a column/attribute name not in the file.
    def find_by_template(self, t, fields=None):

        t_keys = t.keys()
        for i in t_keys:
            if i not in self.columns:
                raise ValueError("Keys in templated doesn't match the database column types")

        
        
        w = templateToWhereClause(t)

        if fields == None:
            q = "SELECT * FROM " + self.table_name + " " + w + ";"
        else:
            for j in fields:
                if j not in self.columns:
                    raise ValueError("The fields don't match the database column types")
            
            fields_string = ""
            for i in fields:
                fields_string += i + ","
            fields_string = fields_string[:-1]

            q = "SELECT " + fields_string + " FROM " + self.table_name + " " + w + ";"

        # print ("Query = ", q)
        self.cursor.execute(q)
        r = self.cursor.fetchall()
        return r


    # Inserts the row into the table. 
    # Raises on duplicate key or invalid columns.
    def insert(self, t):
        t_keys = t.keys()
        for i in t_keys:
            if i not in self.columns:
                raise ValueError("Keys in templated doesn't match the database format")
        
        primary_key_string_set = []
        for i in self.key_columns:
            primary_key_string_set.append(t[i])
        
        result = self.find_by_primary_key(primary_key_string_set)
        

        if len(result) != 0:
             raise ValueError("Duplicated Primary key found, Not insert!")

        w = templateToInsertClause(t)
        q = "INSERT INTO " + self.table_name + " " + w + ";"
#         print ("Query = ", q)
        self.cursor.execute(q)
        self.cnx.commit()
       
    # t: A template.
    # Deletes all rows matching the template.
    def delete(self, t):

        t_keys = t.keys()
        for i in t_keys:
            if i not in self.columns:
                raise ValueError("Keys in templated doesn't match the database format")

        w = templateToWhereClause(t)
        q = "DELETE FROM " + self.table_name + " " + w + ";"
        # print ("Query = ", q)
        self.cursor.execute(q)

