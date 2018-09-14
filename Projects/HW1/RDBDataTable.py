import pymysql


class RDBDataTable():
    def __init__(self, host, user, password, db ):
        # Your code goes here
        cnx = pymysql.connect(host= host,
                                user= user,
                                password= password,
                                db=db,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
        self.cursor = cnx.cursor()
    
    # Pretty print the CSVTable and its attributes.
    def __str__(self):
        # Your code goes here.
        # Optional
        pass

    def find_by_primary_key(self, string_set, fields=None):
        

    # The input is:
    # t: The template to match. The result is a list of rows
    # whose attribute/value pairs exactly match the template.
    # fields: A subset of the fields to include for each result.
    # Raises an exception if the template or list of fields contains
    # a column/attribute name not in the file.
    def find_by_template(self, t, fields=None):
        # Your code goes here
        

    
    # Inserts the row into the table. 
    # Raises on duplicate key or invalid columns.
    def insert(self, r):
        # Your code goes here
        

       
    # t: A template.
    # Deletes all rows matching the template.
    def delete(self, t):
        # Your code goes here.
        
