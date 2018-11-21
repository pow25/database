import csv  # Python package for reading and writing CSV files.
import CSVCatalog
import json

max_rows_to_print = 10

class CSVTable:
    # Table engine needs to load table definition information.
    __catalog__ = CSVCatalog.CSVCatalog()

    def __init__(self, t_name, load=True):
        """
        Constructor.
        :param t_name: Name for table.
        :param load: Load data from a CSV file. If load=False, this is a derived table and engine will
            add rows instead of loading from file.
        """
        if t_name == None:
            raise ValueError("The table name can't be None!")
        self.__table_name__ = t_name

        # Holds loaded metadata from the catalog. You have to implement  the called methods below.
        self.__description__ = None
        if load:
            self.__load_info__()  # Load metadata
            self.__rows__ = None
            self.__load__()  # Load rows from the CSV file.

            # Build indexes defined in the metadata. We do not implement insert(), update() or delete().
            # So we can build indexes on load.
            self.__build_indexes__()
        else:
            self.__file_name__ = "DERIVED"

    def __load_info__(self):
        """
        Loads metadata from catalog and sets __description__ to hold the information.
        :return:
        """
        self.__description__ = self.__catalog__.get_table(self.__table_name__)
        

    # Load from a file and creates the table and data.
    def __load__(self):

        try:
            fn = self.__get_file_name__()
            with open(fn, "r") as csvfile:
                # CSV files can be pretty complex. You can tell from all of the options on the various readers.
                # The two params here indicate that "," separates columns and anything in between " ... " should parse
                # as a single string, even if it has things like "," in it.
                reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')

                # Get the names of the columns defined for this table from the metadata.
                column_names = self.__get_column_names__()

                # Loop through each line (well dictionary) in the input file.
                for r in reader:
                    # Only add the defined columns into the in-memory table. The CSV file may contain columns
                    # that are not relevant to the definition.
                    projected_r = self.project([r], column_names)[0]
                    self.__add_row__(projected_r)
                
        except IOError:
            raise ValueError("The file can't be opened, something wrong")

    def __add_row__(self, new_row):
        if self.__rows__ is None:
            self.__rows__ = []
        self.__rows__.append(new_row)

    def __get_file_name__(self):
        return self.__description__.csv_f

    def __get_column_names__(self):
        res = []
        if self.__description__ is not None:
            r = self.__description__.column_definitions
            for i in r:
                res.append(i.column_name)
        else:
            if self.__rows__ is not None:
                res = list(self.__rows__[0].keys())
        return res

    def __form_odict(self,l): #help print a row from a table
        result = ""
        temp = list(l)
        for i in range(len(temp)):
            result += "{:<15}".format(temp[i])
        return result

    def get_row_list(self):
        return self.__rows__
    
    def __str__(self):
        """
        You can do something simple here. The details of the string returned depend on what properties you
        define on the class. So, I cannot provide a simple implementation.
        :return:
        """
        if self.__description__ is not None:
            result = "Name: " + self.__table_name__ + " File:" + self.__get_file_name__() + "\n"
            result += "Row count: " + str(self.__get_row_count__()) + "\n"
            json_desc = self.__description__.to_json()
            result += json.dumps(json_desc, indent=2)

            result += "\n Index Information: "
            idxes = self.__description__.index_definitions
            if idxes is not None:
                for i in idxes:
                    result +="\n"
                    result += "Name: " + i.index_name + ", Columns: " + ",".join(i.column_names)
                    idx_entry = self.__indexes__[i.index_name] 
                    result += ", No. of entries: " + str(len(idx_entry.keys()))
            else:
                result += "No indexes"
        else:
            result = "Name: " + self.__table_name__ + "File: " + self.__file_name__ + "\n"
            result += "Row count: " + str(self.__get_row_count__()) + "\n"
        l = self.__get_row_count__()

        result += "\n\nSample rows:"

        if l > 0:
            # if there exist a lot of rows, just the first few and last few
            n = min (l, max_rows_to_print)
            if n < max_rows_to_print:
                first_n = n
                second_n = 0
            else:
                first_n = int(max_rows_to_print/2)
                second_n = l - first_n
        if first_n == 0:
            first_n = 1

        result += "\n"

        cn = self.__get_column_names__()
        result += self.__form_odict(cn)
        result += "\n"
        the_rows = self.get_row_list()

        for i in range(first_n):
            temp_r = the_rows[i]
            result += self.__form_odict(temp_r.values()) + "\n"

        if second_n > 0:
            middle_row = ["..."] * len(self.__get_column_names__())
            result += self.__form_odict(middle_row) + "\n"
            for i in range(l-1, second_n-1, -1):
                temp_r = the_rows[i]
                result += self.__form_odict(temp_r.values()) + "\n"
        return result

    def __get_row_count__(self):
        return len(self.__rows__)

    def __get_index_value__(self, row, index_name):
        idx_elements = []

        for i in self.__description__.index_definitions:
            if i.index_name == index_name:
                columns = i.column_names

        for c in columns:
            idx_elements.append(row[c])

        result = "_".join(idx_elements)
        
        return result

    def __build_index__(self, index_name, columns):
        new_index = {}
        for r in self.__rows__:
            idx_value = self.__get_index_value__(r,index_name) #compute the hash key for each row
            idx_entry = new_index.get(idx_value,[]) #attention here, it is not just a dict, but a dict of list
            idx_entry.append(r)                     # so that, new_index['Williams'] will return a list of rows 
            new_index[idx_value] = idx_entry        # that the Lastname of each of them is Williams
        return new_index

    def __build_indexes__(self):
        self.__indexes__ = {}
        defined_indexes = self.__description__.index_definitions
        for i in defined_indexes:
            new_idx = self.__build_index__(i.index_name, i.column_names)
            self.__indexes__[i.index_name] = new_idx
        
    def __get_access_path__(self, tmp):
        """
        Returns best index matching the set of keys in the template.

        Best is defined as the most selective index, i.e. the one with the most distinct index entries.

        An index name is of the form "colname1_colname2_coluname3" The index matches if the
        template references the columns in the index name. The template may have additional columns, but must contain
        all of the columns in the index definition.
        :param tmp: list of Query template keys.
        :return: Index or None
        """
        if self.__indexes__ is None or tmp is None:
            return None,None
        else:
            result = None
            count = None

        temp_set = set(tmp)       
        
        for i in self.__description__.index_definitions:
            columns = set(i.column_names)
            
            if columns.issubset(temp_set):
                if result is None: 
                    result = i.index_name
                    count = len(self.__indexes__[result])
                else:
                    if count < len(self.__indexes__[i.index_name]): #choose the one with biggest selectivity
                        result = i.index_name
                        count = len(self.__indexes__[result])
        
        return result,count


    def matches_template(self, row, t):
        """

        :param row: A single dictionary representing a row in the table.
        :param t: A template
        :return: True if the row matches the template.
        """

        # Basically, this means there is no where clause.
        if t is None:
            return True

        try:
            c_names = list(t.keys())
            for n in c_names:
                if row[n] != t[n]:
                    return False
            else:
                return True
        except Exception as e:
            raise (e)

    def project(self, rows, fields):
        """
        Perform the project. Returns a new table with only the requested columns.
        :param fields: A list of column names.
        :return: A new table derived from this table by PROJECT on the specified column names.
        """
        try:
            if fields is None:  # If there is not project clause, return the base table
                return rows  # Should really return a new, identical table but am lazy.
            else:
                result = []
                for r in rows:  # For every row in the table.
                    tmp = {}  # Not sure why I am using range.
                    for j in range(0, len(fields)):  # Make a new row with just the requested columns/fields.
                        v = r[fields[j]]
                        tmp[fields[j]] = v
                    else:
                        result.append(tmp)  # Insert into new table when done.

                return result

        except KeyError:
            # happens if the requested field not in rows.
            raise ValueError("Invalid field in Project")

    def __find_by_template_scan__(self, t, fields=None):
        """
        Returns a new, derived table containing rows that match the template and the requested fields if any.
        Returns all row if template is None and all columns if fields is None.
        :param t: The template representing a select predicate.
        :param fields: The list of fields (project fields)
        :return: New table containing the result of the select and project.
        """
        # If there are rows and the template is not None
        if self.__rows__ is not None:

            result = []

            # Add the rows that match the template to the newly created table.
            for r in self.__rows__:
                if self.matches_template(r, t):
                    result.append(r)

            result = self.project(result, fields)
        else:
            result = None

        return result

    def __find_by_template_index__(self, t, idx_name, fields=None):
        """
        Find using a selected index
        :param t: Template representing a where clause
        :param idx: Name of index to use.
        :param fields: Fields to return.
        :return: Matching tuples.
        """

        key_values = self.__get_index_value__(t,idx_name)
        the_index = self.__indexes__[idx_name]
        tmp_result = the_index.get(key_values,None)
        result = None

        if tmp_result is not None:
            result = []
            for r in tmp_result:
                if self.matches_template(r,t):
                    result.append(r)
            result = self.project(result,fields)

        return result

    def find_by_template(self, t, fields=None):
        # 1. Validate the template values relative to the defined columns.
        # 2. Determine if there is an applicable index, and call __find_by_template_index__ if one exists.
        # 3. Call __find_by_template_scan__ if not applicable index.
        if t is not None:
            access_index,_ = self.__get_access_path__(list(t.keys()))
        else:
            access_index = None
        
        if access_index is None:
            self.__used_index_find_by_template__ = None
            return self.__find_by_template_scan__(t,fields=fields)
        else:
            self.__used_index_find_by_template__ = access_index
            result = self.__find_by_template_index__(t,access_index,fields)
            return result

    def print_used_index_during_find_by_template(self):
        return self.__used_index_find_by_template__

    def __choose_scan_probe_table__(self, right_r, on_fields):
        left_path, left_count = self.__get_access_path__(on_fields)
        right_path, right_count = right_r.__get_access_path__(on_fields)

        if left_path is None and right_path is None:
            return self, right_r
        elif left_path is None and right_path is not None:
            return self, right_r
        elif left_path is not None and right_path is None:
            return right_r, self
        elif right_count < left_count:
            return self,right_r
        else:
            return right_r, self

    def __get_sub_where_template(self, where_template):
        result = {}
        if where_template is None:
            return None
        keys = where_template.keys()
        for j in self.__description__.column_definitions:
            if j.column_name in keys:
                result[j.column_name] = where_template[j.column_name]
        
        if result:
            return result
        else:
            return None

    def __get_on_template__(self, row, on_fields):
        on_template = {}

        for i in on_fields:
            on_template[i] = row[i]

        return on_template

    def __join_rows__(self, l, r, on_fields):
        result_rows = []
        for lr in l:
            on_template = self.__get_on_template__(lr,on_fields)
            for rr in r:
                if self.matches_template(rr,on_template):
                    new_r = {**lr, **rr}
                    result_rows.append(new_r)

        return result_rows

    def __table_from_rows__(self, name, rows):
        result = CSVTable(name,load=False)
        if rows is None:
            return result
        new_rows = []
        for i in range(len(rows)):
            new_rows.append(rows[i])
        result.__rows__ = new_rows

        return result

    def join(self, right_r, on_fields, where_template=None, project_fields=None):
        """
        Implements a JOIN on two CSV Tables. Support equi-join only on a list of common
        columns names.
        :param left_r: The left table, or first input table
        :param right_r: The right table, or second input table.
        :param on_fields: A list of common fields used for the equi-join.
        :param where_template: Select template to apply to the result to determine what to return.
        :param project_fields: List of fields to return from the result.
        :return: List of dictionary elements, each representing a row.
        """
        # If not optimizations are possible, do a simple nested loop join and then apply where_clause and
        # project clause to result.
        #
        # At least two vastly different optimizations are be possible. You should figure out two different optimizations
        # and implement them.
        #
        scan_table, probe_table = self.__choose_scan_probe_table__(right_r,on_fields)
        scan_sub_template = scan_table.__get_sub_where_template(where_template)
        probe_sub_template = probe_table.__get_sub_where_template(where_template)

        if scan_table is not self:
            print("Swapping scan and probe tables.")

        print("Before pushing down, scan table size is:", len(scan_table.get_row_list()))
        scan_rows = scan_table.find_by_template(scan_sub_template)
        print("After pushing down, scan table size is:", len(scan_rows))

        join_result = []

        for l_r in scan_rows:
            on_template = scan_table.__get_on_template__(l_r,on_fields)

            if probe_sub_template is not None:
                probe_where = {**on_template, **probe_sub_template}  #join two dict to one
            else:
                probe_where = on_template
             
            current_right_row = probe_table.find_by_template(probe_where)
            
            if current_right_row is not None and len(current_right_row) > 0:
                new_rows = self.__join_rows__([l_r], current_right_row, on_fields)
                join_result.extend(new_rows)
        
        final_rows = []
        for r in join_result:
            if self.matches_template(r,where_template):
                r = self.project([r],fields = project_fields)
                final_rows.append(r[0])

        join_result = self.__table_from_rows__( "JOIN(" + self.__table_name__ + "," + right_r.__table_name__ + ") ",
                      final_rows)
        
        return join_result