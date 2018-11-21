import pymysql
import csv
import logging
import json

class ColumnDefinition:
    """
    Represents a column definition in the CSV Catalog.
    """

    # Allowed types for a column.
    column_types = ("text", "number")

    def __init__(self, column_name, column_type="text", not_null=False):
        """
        :param column_name: Cannot be None.
        :param column_type: Must be one of valid column_types.
        :param not_null: True or False
        """
        if column_name == None:
            raise ValueError("The column_name cannot be None!")
        if column_type not in self.column_types:
            raise ValueError("The column_type is invalid!")
        
        self.column_name = column_name
        self.column_type = column_type
        self.not_null = str(not_null)

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

    def to_json(self):
        """
        :return: A JSON object, not a string, representing the column and it's properties.
        """
        json_obj = {}
        json_obj['column_name'] = self.column_name
        json_obj['column_type'] = self.column_type
        json_obj['not_null'] = self.not_null
        
        return json_obj


class IndexDefinition:
    """
    Represents the definition of an index.
    """
    index_types = ("PRIMARY", "UNIQUE", "INDEX")

    def __init__(self, column_names, index_name, index_type):
        """
        :param column_names: Name of the column for the Index
        :param index_names: Name for index. Must be unique name for table.
        :param index_types: Valid index type.
        """
        if column_names == None or index_name == None or index_type == None:
            raise ValueError("all 3 index init inputs must not be None!")
        if index_type not in self.index_types:
            raise ValueError("Index type is not valid!")

        self.index_type = index_type
        self.column_names = column_names
        self.index_name = index_name

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

    def to_json(self):
        """
        :return: A JSON object, not a string, representing the column and it's properties.
        """
        json_obj = {}
        json_obj['index_name'] = self.index_name
        json_obj['column_names'] = self.column_names
        json_obj['index_type'] = self.index_type

        return json_obj


class TableDefinition:
    """
    Represents the definition of a table in the CSVCatalog.
    """

    def __init__(self, t_name=None, csv_f=None, column_definitions=None, 
                 index_definitions=None, cnx=None, load=False):
        """
        :param t_name: Name of the table.
        :param csv_f: Full path to a CSV file holding the data.
        :param column_definitions: List of column definitions to use from file. Cannot contain invalid column name.
            May be just a subset of the columns.
        :param index_definitions: List of index definitions. Column names must be valid.
        :param cnx: Database connection to use. If None, create a default connection.
        """
        if t_name == None:
            raise ValueError("The table name can't be None")
        self.table_name = t_name
        self.column_definitions = []
        self.index_definitions = []
        self.valid_column_names = []
        self.csv = ""
        self.cnx = cnx
        if cnx == None:
            try:
                self.cnx = pymysql.connect("localhost", "dbuser", "dbuser", "CSVCatalog", charset='utf8mb4', 
                cursorclass=pymysql.cursors.DictCursor)
            except:
                print( "Can't connect to the database" )

        self.cursor = self.cnx.cursor()
        
        if load == True:
            self.__load_core_definition__()
            self.__load_columns__()
            self.__load_indexes__()
            valid_column_names = ""
            try:
                with open(self.csv_f) as f:
                    reader = csv.reader(f, delimiter=';')
                    for i in reader:
                        valid_column_names = i[0]
                        break
                f.close()
            except IOError:
                raise ValueError("The CSV file doens't exit!")
                
            self.valid_column_names = valid_column_names.split(",")
        else:
            self.csv_f = csv_f
            
            if column_definitions != None:
                self.column_definitions = column_definitions
            
            if index_definitions != None:
                self.index_definitions = index_definitions
            
            valid_column_names = ""
            try:
                with open(csv_f) as f:
                    reader = csv.reader(f, delimiter=';')
                    for i in reader:
                        valid_column_names = i[0]
                        break
                f.close()
            except IOError:
                raise ValueError("The CSV file doens't exit!")
                
            self.valid_column_names = valid_column_names.split(",")

            if column_definitions != None:
                for i in column_definitions:
                    if i.column_name not in self.valid_column_names:
                        raise ValueError("The column_definitions contains invalid column names!")

            if index_definitions != None:
                for i in index_definitions:
                    for j in i.column_names:
                        if j not in self.valid_column_names:
                            raise ValueError("The index_definitions contains invalid column names!")

            q = "INSERT INTO csvcatalog.table (table_name, file_name) VALUES ('" +t_name+"','" + csv_f + "');"
            try:
                self.cursor.execute(q)
                self.cnx.commit()
            except Exception as e:
                raise e

            if column_definitions != None:
                for i in column_definitions:
                    q = "INSERT INTO csvcatalog.column (table_name, column_name, column_type, not_null) \
                    VALUES ('" +t_name+"','" + i.column_name + "','" + i.column_type +"','"+i.not_null+ "');"
                    try:
                        self.cursor.execute(q)
                        self.cnx.commit()
                    except Exception as e:
                        raise e
            
            if index_definitions != None:
                for i in index_definitions:
                    if not self.__check_index_unique__(i.index_name,i.index_type):
                        raise ValueError("Duplicated index name for a same table!!")
                    for j in i.column_names:
                        q = "INSERT INTO csvcatalog.index (table_name, index_name, column_name, index_type) \
                        VALUES ('" +t_name+"','" + i.index_name + "','" + j +"','"+i.index_type+ "');"
                        try:
                            self.cursor.execute(q)
                            self.cnx.commit()
                        except Exception as e:
                            raise e

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

    def __check_index_unique__(self,index_name,index_type):
        q = "SELECT * FROM csvcatalog.index WHERE table_name='" + self.table_name + "';"
        self.cursor.execute(q)
        result = self.cursor.fetchall()
        for r in result:
            if r['index_name']  == index_name and r['index_type'] != index_type:
                return False
        return True

    def __load_columns__(self):
        q = "SELECT * FROM csvcatalog.column WHERE table_name='" + self.table_name + "' ORDER BY column_name;"
        self.cursor.execute(q)
        result = self.cursor.fetchall()

        for r in result:
            new = ColumnDefinition(r['column_name'], r['column_type'], r['not_null'])
            self.column_definitions.append(new)

    def __load_core_definition__(self):
        q = "SELECT * FROM csvcatalog.table WHERE table_name='" + self.table_name + "';"
        self.cursor.execute(q)
        r = self.cursor.fetchall()
        # q = "SELECT * FROM csvcatalog.table;"
        # self.cursor.execute(q)
        # c = self.cursor.fetchall()
        # print(c)
        self.csv_f = r[0]['file_name']

    def __load_indexes__(self):
        q = "SELECT * FROM csvcatalog.index WHERE table_name='" + self.table_name + "';"
        self.cursor.execute(q)
        result = self.cursor.fetchall()
        temp_dict = {}
        for r in result:
            if r['index_name'] in temp_dict:
                temp_dict[r['index_name']]['column_names'].append(r['column_name'])
            else:
                temp_dict[r['index_name']] = {}
                temp_dict[r['index_name']]['column_names'] = []
                temp_dict[r['index_name']]['column_names'].append(r['column_name'])
                temp_dict[r['index_name']]['index_type'] = r['index_type']
                
        for key, value in temp_dict.items():   
            new = IndexDefinition(value['column_names'], key, value['index_type'])
            self.index_definitions.append(new)

    def add_column_definition(self, c):
        """
        Add a column definition.
        :param c: New column. Cannot be duplicate or column not in the file.
        :return: None
        """
        if c.column_name not in self.valid_column_names:
            raise ValueError("The column_definitions contains invalid column names!")
        
        q = "INSERT INTO csvcatalog.column (table_name, column_name, column_type, not_null) \
        VALUES ('" +self.table_name+"','" + c.column_name + "','" + c.column_type +"','"+c.not_null+ "');"
        try:
            self.cursor.execute(q)
            self.cnx.commit()
        except Exception as e:
            raise e
    
        self.column_definitions.append(c)

    def drop_column_definition(self, c):
        """
        Remove from definition and catalog tables.
        :param c: Column name (string)
        :return:
        """
        q = "DELETE FROM csvcatalog.column WHERE column_name ='" + c + "';" 
        try:
            self.cursor.execute(q)
            self.cnx.commit()
        except Exception as e:
            raise e

        for i in self.column_definitions:
            if i.column_name == c:
                self.column_definitions.remove(i)
                for j in self.index_definitions:
                    if c in j.column_names:
                        self.drop_index(j.index_name)


    def to_json(self):
        """
        :return: A JSON representation of the table and it's elements.
        """
        json_obj = {}
        temp = {}
        temp['name'] =  self.table_name
        temp['path'] = self.csv_f
        json_obj['definition'] = temp

        temp = []
        for i in self.column_definitions:
            temp.append(i.to_json())
        json_obj['columns'] = temp

        temp = {}
        for i in self.index_definitions:
            temp[i.index_name] = i.to_json()
        json_obj['indexes'] = temp

        return json_obj

    def define_primary_key(self, columns):
        """
        Define (or replace) primary key definition.
        :param columns: List of column values in order.
        :return:
        """
        for i in columns:
            if i not in self.valid_column_names:
                raise ValueError("The columns contains invalid column names!")
        for i in columns:
            q = "INSERT INTO csvcatalog.index (table_name, index_name, column_name, index_type) \
            VALUES ('"+self.table_name+"','PRIMARY','" + i +"','PRIMARY') ON DUPLICATE KEY UPDATE \
            index_name='PRIMARY', column_name='" + i + "';"
            try:
                self.cursor.execute(q)
                self.cnx.commit()
            except Exception as e:
                raise e

        for i in self.index_definitions:
            if i.index_name == 'PRIMARY':
                self.index_definitions.remove(i)

        temp = IndexDefinition(columns,'PRIMARY','PRIMARY')
        self.index_definitions.append(temp)

    def define_index(self, index_name, columns, kind="INDEX"):
        """
        Define or replace and index definition.
        :param index_name: Index name, must be unique within a table.
        :param columns: Valid list of columns.
        :param kind: One of the valid index types.
        :return:
        """
        if not self.__check_index_unique__(index_name,kind):
            raise ValueError("Duplicated index name for a same table!!")
        for i in columns:
            if i not in self.valid_column_names:
                raise ValueError("The columns contains invalid column names!")
        for i in columns:
            q = "INSERT INTO csvcatalog.index (table_name, index_name, column_name, index_type) \
            VALUES ('"+self.table_name+"','" + index_name + "','" + i +"','" + kind +"') ON DUPLICATE KEY UPDATE \
            index_name='"+ index_name +"', column_name='" + i + "';"
            try:
                self.cursor.execute(q)
                self.cnx.commit()
            except Exception as e:
                raise e

        for i in self.index_definitions:
            if i.index_name == index_name:
                self.index_definitions.remove(i)

        temp = IndexDefinition(columns,index_name,kind)
        self.index_definitions.append(temp)

    def drop_index(self, index_name):
        """
        Remove an index.
        :param index_name: Name of index to remove.
        :return:
        """
        q = "DELETE FROM csvcatalog.index WHERE index_name ='" + index_name + "';" 
        try:
            self.cursor.execute(q)
            self.cnx.commit()
        except Exception as e:
            raise e

        for i in self.index_definitions:
            if i.index_name == index_name:
                self.index_definitions.remove(i)

    def get_index_selectivity(self, index_name):
        """
        :param index_name:
        :return:
        """    
        try:
            with open(self.csv_f,mode = 'r') as f:
                reader = csv.reader(f, delimiter=';')
                row_count = sum(1 for row in reader) - 1
            f.close()
        except IOError:
            raise ValueError("The CSV file doens't exit!")

        q = "SELECT * FROM csvcatalog.index WHERE table_name='" + self.table_name +\
        "' AND index_name='" +index_name+"';"
        self.cursor.execute(q)
        result = self.cursor.fetchall()
        if len(result) == 0: 
            raise ValueError("The index_name is invalid, it doesn't exist in catalog!")
        
        list_columns = [] #using a list of sets to store each columns distinct value
        for r in result:
            list_columns.append(r['column_name'])

        
        distinct_for_each = set()
        try:
            with open(self.csv_f,mode = 'r') as f:
                csv_reader = csv.DictReader(f)
                for i in csv_reader:
                    temp = ""
                    for j in list_columns:
                        temp += i[j]
                    distinct_for_each.add(temp)
                f.close()
        except IOError:
            raise ValueError("The CSV file doens't exit!")

        return len(distinct_for_each) / row_count 

    def describe_table(self):
        """
        Simply wraps to_json()
        :return: JSON representation.
        """
        json_obj = self.to_json()
        return json_obj


class CSVCatalog:

    def __init__(self, dbhost="localhost", dbport="somedefault",
                 dbname="CSVCatalog", dbuser="dbuser", dbpw="dbuser", debug_mode=None):
        try:
            self.cnx = pymysql.connect(dbhost, dbuser, dbpw, dbname, charset='utf8mb4', 
            cursorclass=pymysql.cursors.DictCursor)
            self.cursor = self.cnx.cursor()
        except:
            print( "Can't connect to the database" )

    def create_table(self, table_name, file_name, column_definitions=None, index_definitions=None):
        try:
            res = TableDefinition(table_name,file_name,column_definitions,index_definitions,cnx=self.cnx)
        except Exception as e:
            raise e
        return res

    def drop_table(self, table_name):
        q = "DELETE FROM csvcatalog.table WHERE table_name = '"+ table_name + "';"
        try:
            self.cursor.execute(q)
            self.cnx.commit()
        except Exception as e:
            raise e

    def get_table(self, table_name):
        """
        Returns a previously created table.
        :param table_name: Name of the table.
        :return:
        """
        result = TableDefinition(t_name=table_name, load=True, cnx=self.cnx)
        return result
