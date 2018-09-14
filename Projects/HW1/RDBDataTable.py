class RDBDataTable():
    def __init__(self, t_name, t_file, key_columns):
        # Your code goes here
        pass

    
    # Pretty print the CSVTable and its attributes.
    def __str__(self):
        # Your code goes here.
        # Optional
        pass

    # loads the data from the file into the class instance data.
    # You decide how to store and represent the rows from the file.
    def load(self):
        # Your code goes here
        pass
    
    # Obvious
    def save(self):
        pass

    def find_by_primary_key(self, string_set, fields=None):
        pass

    # The input is:
    # t: The template to match. The result is a list of rows
    # whose attribute/value pairs exactly match the template.
    # fields: A subset of the fields to include for each result.
    # Raises an exception if the template or list of fields contains
    # a column/attribute name not in the file.
    def find_by_template(self, t, fields=None):
        # Your code goes here
        pass

    
    # Inserts the row into the table. 
    # Raises on duplicate key or invalid columns.
    def insert(self, r):
        # Your code goes here
        pass

       
    # t: A template.
    # Deletes all rows matching the template.
    def delete(self, t):
        # Your code goes here.
        pass
