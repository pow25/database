The two python files are contained in the src folder,
While the testcase python files and test results are contained in the test folder
The sql statement for creating the CSVcatalog DB are stored in sql folder
The data folder contains 3 csv files that used. 

----------------------------------------------------------------------------------------------
create.sql:
It first create a schema csvcatalog. And inside, created 3 tables:table,column,index
to hold the general information about catalog. 
The "table" contains table_name and file_name(file_path), 
    the primary key is table_name(so make sure no duplicated table_name exists)

The "column" contains table_name, column_name, column_type, and not_null,
    the primay key is table_name and column_name (for everytable, no duplicated column_name allowed)

The "index" contains table_name, index_name, index_type,
    the primay key is table_name, index_name and column_name

And for the relation, both index table and column name refers to table.table_name and DELETE CASCADE,
so that once drop a row in the table, the related rows in column, index will also be dropped, in addition,
it is not allowed to insert into either index, column if there is no specified table_name in table

What's more, for the index, it also refers to column table(table_name,column_name), and DELETE CASCADE
So, if the column was dropped, the related row in index will also be delete(it also ensured through drop_column_definition and drop_index in CSVCatalog.py), 
and index row exists only if there exists a related row in column
----------------------------------------------------------------------------------------------
SRC:
    CSVCatalog:
    the function logic is once user input some table_name, column_definitions and related index, the program will
    go to database CSVcatalog to insert related info into 3 tables(of course, if either one of them failed sanity
    check, then error raised)
    and the functions are just using prof's template, so it is self-explaining

    CSVTable:
    the functions are just using prof's template, so it is self-explaining. The logic is that it will first build CSVCatalog class and get related info(3 tables) from the DB. Then, it will read the CSV file to load all the data into its variable. Then, it will build the index with python Dict{}.
    The key name is column1_column2_....., and the values is a list of objects. Then for the find_by_template, it will first try to see the access path whether there exists a usable index, if yes, use this index to speed up the searching process, otherwise just do a for loop for all the rows. 
    For the join, first optimization is that it will try to swap the probe/scan table based on the selectivity of their corresponding index, then it will use where clause to push down to each one of them for reducing the number of rows to join, and then it will call the function find_by_template to find, which is based on index, so it is another optimization. 

-----------------------------------------------------------------------------------------------
For the 3 test case py files:

    test_catalog:
        there are a lot of test cases, basically test all the functions that should work well and how to handle
        the error case(error input, excepiton etc.)

    test_template: 
        1, it contains 3 test cases, the first one test whether the find_by_template works or not, it compares
        the time for searching one with index and one without index
        2, the second one test about the CSVTable's load function, it try to load a non-existing table, it should
        fail.
        3, the third one test about whether the program will choose the optimal index for searching
    test_join:
        all 4 test cases are test whether the join has been optimized or not, they used 3 CSV data files: People,
        Teams, Batting
