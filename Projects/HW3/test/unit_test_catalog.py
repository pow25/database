import sys
sys.path.insert(0, '../src')

import CSVCatalog

import time
import json

def cleanup():
    """
    Deletes previously created information to enable re-running tests.
    :return: None
    """
    cat = CSVCatalog.CSVCatalog()
    cat.drop_table("people")
    cat.drop_table("batting")
    cat.drop_table("teams")

def print_test_separator(msg):
    print("\n")
    lot_of_stars = 20*'*'
    print(lot_of_stars, '  ', msg, '  ', lot_of_stars)
    print("\n")

def test_create_table_0():
    """
    Creates a table that includes several column and index definitions.
    :return:
    """
    print_test_separator("Starting test_create_table_0")
    cleanup()
    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    ids = []
    ids.append(CSVCatalog.IndexDefinition(["playerID"], "PRIMARY", "PRIMARY"))
    t = cat.create_table("people", "../data/People.csv",cds,ids)
    print("People table", json.dumps(t.describe_table(), indent=2))
    print_test_separator("Complete test_create_table_0")

def test_create_table_0_fail():
    """
    Creates a table that includes several column and duplicated index.
    :return:
    """
    print_test_separator("Starting test_create_table_0_fail")
    cleanup()
    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    ids = []
    ids.append(CSVCatalog.IndexDefinition(["playerID","nameLast"], "PRIMARY", "PRIMARY"))
    ids.append(CSVCatalog.IndexDefinition(["playerID","nameFirst"], "PRIMARY", "PRIMARY"))
    try:
        t = cat.create_table("people", "../data/People.csv",cds,ids)
    except Exception as e:
        print("created_0 failed with e = ", e)
        print("create_0 should fail.")
        print_test_separator("Successful end for test_create_table_0_fail")
        return
    print_test_separator("INCORRECT end for  test_create_table_0_fail")

def test_create_table_0_fail2():
    """
    Creates a table that includes several column and duplicated index name.
    :return:
    """
    print_test_separator("Starting test_create_table_0_fail2")
    cleanup()
    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    ids = []
    ids.append(CSVCatalog.IndexDefinition(["playerID","nameLast"], "PRIMARY", "PRIMARY"))
    ids.append(CSVCatalog.IndexDefinition(["nameFirst"], "PRIMARY", "INDEX"))
    try:
        t = cat.create_table("people", "../data/People.csv",cds,ids)
    except Exception as e:
        print("created_0 failed with e = ", e)
        print("create_0 should fail.")
        print_test_separator("Successful end for test_create_table_0_fail2")
        return
    print_test_separator("INCORRECT end for  test_create_table_0_fail2")

def test_create_table_1():
    """
    Simple create of table definition. No columns or indexes.
    :return:
    """
    cleanup()
    print_test_separator("Starting test_create_table_1")
    cat = CSVCatalog.CSVCatalog()
    t = cat.create_table("people", "../Data/People.csv")
    print("People table", json.dumps(t.describe_table()))
    print_test_separator("Complete test_create_table_1")


def test_create_table_2_fail():
    """
    Creates a table, and then attempts to create a table with the same name. Second create should fail.
    :return:
    """
    print_test_separator("Starting test_create_table_2_fail")
    cleanup()
    cat = CSVCatalog.CSVCatalog()
    t = cat.create_table("people", "../data/People.csv")

    try:
        t = cat.create_table("people",
             "../data/People.csv")
    except Exception as e:
        print("Second created failed with e = ", e)
        print("Second create should fail.")
        print_test_separator("Successful end for  test_create_table_2_fail")
        return

    print_test_separator("INCORRECT end for  test_create_table_2_fail")



def test_create_table_3():
    """
    Creates a table that includes several column definitions.
    :return:
    """
    print_test_separator("Starting test_create_table_3")
    cleanup()
    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))

    t = cat.create_table("people", "../data/People.csv",cds)
    print("People table", json.dumps(t.describe_table(), indent=2))
    print_test_separator("Complete test_create_table_3")


def test_create_table_3_fail():
    """
    Creates a table that includes several column definitions. This test should fail because one of the defined
    columns is not in the underlying CSV file.
    :return:
    """
    print_test_separator("Starting test_create_table_3_fail")
    cleanup()
    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    cds.append(CSVCatalog.ColumnDefinition("canary"))

    try:
        t = cat.create_table("people", "../data/People.csv",cds)
        print_test_separator("FAILURE test_create_table_3")
        print("People table", json.dumps(t.describe_table(), indent=2))
    except Exception as e:
        print("Exception e = ", e)
        print_test_separator("Complete test_create_table_3_fail successfully")

def test_create_table_3_fail2():
    """
    Creates a table that includes several column definitions. This test should fail because contains duplicated
    columns.
    :return:
    """
    print_test_separator("Starting test_create_table_3_fail2")
    cleanup()
    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))

    try:
        t = cat.create_table("people", "../data/People.csv",cds)
        print_test_separator("FAILURE test_create_table_3")
        print("People table", json.dumps(t.describe_table(), indent=2))
    except Exception as e:
        print("Exception e = ", e)
        print_test_separator("Complete test_create_table_3_fail2 successfully")

def test_create_table_4_fail2():
    """
    Creates a table that includes several column definitions. This test should fail because we are trying
    to insert duplicated columns.
    :return:
    """
    print_test_separator("Starting test_create_table_4_fail2")
    cleanup()
    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))

    try:
        t = cat.create_table("people", "../data/People.csv",cds)
        t.add_column_definition(CSVCatalog.ColumnDefinition("playerID", "text", True))
        print_test_separator("FAILURE test_create_table_4")
        print("People table", json.dumps(t.describe_table(), indent=2))
    except Exception as e:
        print("Exception e = ", e)
        print_test_separator("Complete test_create_table_4_fail2 successfully")

def test_create_table_4():
    """
        Creates a table that includes several column definitions.
        :return:
        """
    print_test_separator("Starting test_create_table_4")
    cleanup()
    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", column_type="text", not_null=True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))
    cds.append(CSVCatalog.ColumnDefinition("H", column_type="number", not_null=False))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number", not_null=False))


    t = cat.create_table("batting","../data/Batting.csv",cds)

    t.define_primary_key(['playerID', 'teamID', 'yearID', 'stint'])
    print("People table", json.dumps(t.describe_table(), indent=2))
    print_test_separator("Complete test_create_table_4")

def test_create_table_4_fail():
    """
    Creates a table that includes several column definitions and a primary key.
    The primary key references an undefined column, which is an error.
    """
    print_test_separator("Starting test_create_table_4_fail")
    cleanup()
    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", column_type="text", not_null=True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))
    cds.append(CSVCatalog.ColumnDefinition("H", column_type="number", not_null=False))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number", not_null=False))


    t = cat.create_table("batting","../data/Batting.csv",cds)
    try:
        t.define_primary_key(['playerID', 'teamID', 'yearID', 'HR'])
        print("Batting table", json.dumps(t.describe_table(), indent=2))
        print_test_separator("FAILURES test_create_table_4_fail")
    except Exception as e:
        print("Exception e = ", e)
        print_test_separator("SUCCESS test_create_table_4_fail should fail.")


def test_create_table_5_prep():
    """
    Creates a table that includes several column definitions and a primary key.
    :return:
    """
    print_test_separator("Starting test_create_table_5_prep")
    cleanup()
    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", column_type="text", not_null=True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))
    cds.append(CSVCatalog.ColumnDefinition("H", column_type="number", not_null=False))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number", not_null=False))

    t = cat.create_table("batting","../data/Batting.csv", cds)

    t.define_primary_key(['playerID', 'teamID', 'yearID', 'stint'])
    print("Batting table", json.dumps(t.describe_table(), indent=2))

    print_test_separator("Completed test_create_table_5_prep")

def test_create_table_5():
    """
    Modifies a preexisting/precreated table definition.
    :return:
    """
    print_test_separator("Starting test_create_table_5")

    # DO NOT CALL CLEANUP. Want to access preexisting table.
    cat = CSVCatalog.CSVCatalog()
    t = cat.get_table("batting")
    print("Initial status of table = \n", json.dumps(t.describe_table(), indent=2))
    t.add_column_definition(CSVCatalog.ColumnDefinition("HR", "number"))
    t.add_column_definition(CSVCatalog.ColumnDefinition("G", "number"))
    t.define_index("team_year_idx", ['teamID', 'yearID'])
    print("Modified status of table = \n", json.dumps(t.describe_table(), indent=2))
    print_test_separator("Success test_create_table_5")

def test_create_table_6():
    """
    test both drop column and drop index
    """
    print_test_separator("Starting test_create_table_6")
    cleanup()
    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", column_type="text", not_null=True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))
    cds.append(CSVCatalog.ColumnDefinition("H", column_type="number", not_null=False))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number", not_null=False))

    t = cat.create_table("batting","../data/Batting.csv", cds)

    t.define_primary_key(['playerID', 'teamID', 'yearID', 'stint'])
    print("Batting table", json.dumps(t.describe_table(), indent=2))
    print_test_separator("After Dropping")
    t.drop_column_definition("playerID")
    t.drop_index("PRIMARY")
    print("Batting table", json.dumps(t.describe_table(), indent=2))
    print_test_separator("Completed test_create_table_6")

def test_create_table_7():
    """
    test get_index_selectivity
    """
    print_test_separator("Starting test_create_table_7")
    cleanup()
    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", column_type="text", not_null=True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))
    cds.append(CSVCatalog.ColumnDefinition("H", column_type="number", not_null=False))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number", not_null=False))

    t = cat.create_table("batting","../data/Batting.csv", cds)

    t.define_primary_key(['playerID', 'teamID', 'yearID', 'stint'])
    t.define_index("team_year_idx", ['teamID', 'yearID'])
    r1 = t.get_index_selectivity("PRIMARY")
    r2 = t.get_index_selectivity("team_year_idx")
    print("The index selectivity for PRIMARY:",r1)
    print("The index selectivity for team_year_idx:",r2)
    print_test_separator("Completed test_create_table_7")

def test_create_table_8():
    """
    test get_index_selectivity
    """
    print_test_separator("Starting test_create_table_8")
    cleanup()
    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))

    t = cat.create_table("people","../data/People.csv", cds)

    t.define_index("full_name", ['nameFirst', 'nameLast'])
    r2 = t.get_index_selectivity("full_name")
    print("The index selectivity for full_name:",r2)
    print_test_separator("Completed test_create_table_8")

def test_drop_table_9():
    """
    test drop_index,drop_column_defintion
    """
    print_test_separator("Starting test_drop_table_9")
    cleanup()
    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))

    t = cat.create_table("people","../data/People.csv", cds)

    t.define_index("full_name", ['nameFirst', 'nameLast'])
    print(json.dumps(t.describe_table(),indent=2))
    
    print_test_separator("Drop the index")
    t.drop_index('full_name')
    print(json.dumps(t.describe_table(),indent=2))

    print_test_separator("Completed test_drop_table_9")

def test_drop_table_10():
    """
    test drop_index by drop_column_defintion
    """
    print_test_separator("Starting test_drop_table_10")
    cleanup()
    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))

    t = cat.create_table("people","../data/People.csv", cds)

    t.define_index("full_name", ['nameFirst', 'nameLast'])
    print(json.dumps(t.describe_table(),indent=2))
    
    print_test_separator("Drop the column:nameLast, the index should also be dropped")
    t.drop_column_definition('nameLast')
    print(json.dumps(t.describe_table(),indent=2))

    print_test_separator("Completed test_drop_table_10")

def test_load_table_11():
    """
    test load table
    """
    print_test_separator("Starting test_load_table_11")
    cleanup()
    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))

    t = cat.create_table("people","../data/People.csv", cds)

    t.define_index("full_name", ['nameFirst', 'nameLast'])
    print(json.dumps(t.describe_table(),indent=2))
    
    print_test_separator("Drop the index and load the table")
    t.drop_index('full_name')
    b = cat.get_table('people')
    print(json.dumps(b.describe_table(),indent=2))

    print_test_separator("Completed test_load_table_11")

test_create_table_0()
test_create_table_0_fail()
test_create_table_0_fail2()
test_create_table_1()
test_create_table_2_fail()
test_create_table_3()
test_create_table_3_fail()
test_create_table_3_fail2()
test_create_table_4()
test_create_table_4_fail()
test_create_table_4_fail2()
test_create_table_5_prep()
test_create_table_5()
test_create_table_6()
test_create_table_7()
test_create_table_8()
test_drop_table_9()
test_drop_table_10()
test_load_table_11()