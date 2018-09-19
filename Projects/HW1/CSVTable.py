import csv          # Python package for reading and writing CSV files.
import copy         # Copy data structures.
import json

import sys,os

# You can change to wherever you want to place your CSV files.
rel_path = os.path.realpath('./data')
rel_path += '/'
class CSVTable():

    # Change to wherever you want to save the CSV files.

    def __init__(self, table_name, table_file, key_columns):
        '''
        Constructor
        :param table_name: Logical names for the data table.
        :param table_file: File name of CSV file to read/write.
        :param key_columns: List of column names the form the primary key.
        '''
        self.table_name = table_name
        self.table_file = rel_path + table_file
        self.key_columns = key_columns
        self.data = []
    
    def __str__(self):
        '''
        Pretty print the table and state.
        :return: String
        '''
        return json.dumps(self.data, indent=2)
        
    def load(self):
        '''
        Load information from CSV file.
        :return: None
        '''
        try:
            with open(self.table_file, mode = 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for i in csv_reader:
                    self.data.append(i)
        except IOError:
            print ("The datatable file doens't exit")
        
        for i in self.key_columns:
            if i not in self.data[0]:
                raise ValueError("The primary keys are invalid")

    def find_by_primary_key(self, string_set, fields=None):

        if len(string_set) != len(self.key_columns):
            raise ValueError("The primary keys inputed didn't match the key columns")
        result = []
        if fields == None:
            for i in self.data:
                count_match = 0
                for j in range(0,len(string_set)):
                    if i[self.key_columns[j]] == string_set[j]:
                        count_match += 1
                if count_match == len(self.key_columns):
                    result.append(i)
        else:
            for j in fields:
                if j not in self.data[0].keys():
                    raise ValueError("The fields don't match the database column types")
            
            unwanted = self.data[0].keys() - fields
            for i in self.data:
                count_match = 0
                for j in range(0,len(string_set)):
                    if i[self.key_columns[j]] == string_set[j]:
                        count_match += 1
                if count_match == len(self.key_columns):
                    temp = i.copy()
                    for unwanted_key in unwanted:
                        del temp[unwanted_key]
                    result.append(temp)

        return result              

    def find_by_template(self, t, fields=None):
        '''
        Return a table containing the rows matching the template and field selector.
        :param t: Template that the rows much match.
        :param fields: A list of columns to include in responses.
        :return: CSVTable containing the answer.
        '''
        t_keys = t.keys()
        for i in t_keys:
            if i not in self.data[0]:
                raise ValueError("Keys in templated doesn't match the database format")

        result = []
        if fields == None:
            keys = t.keys()
            for i in self.data:
                count_match = 0
                for key in keys:
                    if i[key] == t[key]:
                        count_match += 1
                
                if count_match == len(keys):
                    result.append(i)
        else:
            
            for j in fields:
                if j not in self.data[0].keys():
                    raise ValueError("The fields don't match the database column types")
            
            keys = t.keys()
            unwanted = self.data[0].keys() - fields
            for i in self.data:
                count_match = 0
                for key in keys:
                    if i[key] == t[key]:
                        count_match += 1
                
                if count_match == len(keys):
                    temp = i.copy()
                    for unwanted_key in unwanted:
                        del temp[unwanted_key]
                    result.append(temp)
        
        return result

    def find_by_template_top(self):
        result = set()

        for i in self.data:
            if int(i["yearID"]) >= 1960 and int(i["AB"]) >= 200:
                result.add(i['playerID'])
        
        return result

    def save(self):
        '''
        Write updated CSV back to the original file location.
        :return: None
        '''
        try:
            with open(self.table_file, mode='w', newline = '') as csv_file:
                fieldnames = self.data[0].keys()
                writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
                writer.writeheader()
                for i in self.data:
                    writer.writerow(i)
        except IOError:
            print( "Can't open the file to write" )

    def insert(self, r):
        '''
        Insert a new row into the table.
        :param r: New row.
        :return: None. Table state is updated.
        '''
        t_keys = r.keys()
        for i in t_keys:
            if i not in self.data[0]:
                raise ValueError("Keys in templated doesn't match the database format")
        
        primary_key_string_set = []

        for i in self.key_columns:
            primary_key_string_set.append(r[i])

        result = self.find_by_primary_key(primary_key_string_set)

        if result != None:
            raise ValueError("Duplicated Primary key found, Not insert!")

        self.data.append(r)


    def delete(self, t):
        '''
        Delete all tuples matching the template.
        :param t: Template
        :return: None. Table is updated.
        '''
        t_keys = t.keys()
        for i in t_keys:
            if i not in self.data[0]:
                raise ValueError("Keys in templated doesn't match the database format")
        
        keys = t.keys()
        for i in self.data:
            count_match = 0
            for key in keys:
                if i[key] == t[key]:
                    count_match += 1
            
            if count_match == len(keys):
                self.data.remove(i)