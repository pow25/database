import json
import sys, os
import pymysql
from RDBDataTable import RDBDataTable

def test_template(test_name, table_name, key_columns, template, fields=None):
    print("\n\n*******************************")
    print("Test name = ", test_name)
    print("Template = ", template)
    print("Fields = ", fields)

    try:
        RDBtable = RDBDataTable("localhost","root","zhangchi25","lahman2017n",
                                table_name, key_columns)

        r = RDBtable.find_by_template(template, fields)
        print("Result table:")
        print(json.dumps(r, indent=2))
        
    except ValueError as ve:
        print("Exception = ", ve)

def test_delete( test_name, table_name, key_columns, template ):
    print("\n\n*******************************")
    print("Test name = ", test_name)
    print("Template to delete = ", template)

    try:
        RDBtable = RDBDataTable("localhost","root","zhangchi25","lahman2017n",
                                table_name, key_columns)
        RDBtable.delete(template)

    except ValueError as ve:
        print("Exception = ", ve)

def test_insert(test_name, table_name, key_columns, row, show_rows=False):
    print("\n\n*******************************")
    print("Test name = ", test_name)
    print("Row to insert = ", row)

    try:
        RDBtable = RDBDataTable("localhost","root","zhangchi25","lahman2017n",
                                table_name, key_columns)

        r = RDBtable.insert(row)
        print("Result table:")
        print(json.dumps(r, indent=2))

    except ValueError as ve:
        print("Exception = ", ve)

def test_primary_key(test_name, table_name, key_columns,string_set,fields=None):
    print("\n\n*******************************")
    print("Test name = ", test_name)
    print("Primary key = ", string_set)
    try:
        RDBtable = RDBDataTable("localhost","root","zhangchi25","lahman2017n",
                                table_name, key_columns)
        r = RDBtable.find_by_primary_key(string_set,fields)
        print("Result table:")
        print(json.dumps(r, indent=2))

    except ValueError as ve:
        print("Exception = ", ve)
        

def test_templates():
    test_template("Test2", "People", ["playerID"],
                  {"birthMonth": "9", "nameLast": "Williams"}, ["nameLast", "nameFirst", "birthMonth", "birthYear"])

    test_template("Test3", "People", ["playerID"],
                  {"nameFirst": "Ted", "nameLast": "Williams"}, ["nameLast", "nameFirst", "birthMonth", "birthYear"])

    test_template("Test4", "People", ["canary"],
                  {"nameFirst": "Ted", "nameLast": "Williams"}, ["nameLast", "nameFirst", "birthMonth", "birthYear"])

    test_template("Test5", "Batting", ["playerID", "yearID", "teamID", "stint"],
                  {"playerID": "willite01"}, ["playerID", "yearID", "teamID", "AB", "H", "HR"])

    test_template("Test6", "Batting", ["playerID", "yearID", "teamID", "stint"],
                  {"playerID": "willite01", "iq": 100}, ["playerID", "yearID", "teamID", "AB", "H", "HR"])

    test_template("Test7", "Batting",  ["playerID", "yearID", "teamID", "stint"],
                  {"playerID": "willite01", "yearID": "1961"}, ["playerID", "yearID", "teamID", "AB", "H", "HR"])

    test_template("Test7", "Batting", ["playerID", "yearID", "teamID", "stint"],
                  {"playerID": "willite01", "yearID": "1960"}, ["playerID", "yearID", "teamID", "AB", "H", "HR", "Age"])


def test_inserts():

    test_insert("Insert Test 1", "peoplesmall", ["playerID"],
                {"playerID": "dff1", "nameLast": "Ferguson", "nameFirst": "Donald"})

    test_template("Find after insert 1", "peoplesmall", ["playerID"],
                  {"nameLast": "Ferguson"}, ["nameLast", "nameFirst", "birthMonth", "birthYear"])

    try:
        test_insert("Insert Test 2", "peoplesmall", ["playerID"],
                    {"playerID": "dff1", "nameLast": "Ferguson", "nameFirst": "Donald"})

        raise ValueError("That insert should not have worked!")

    except ValueError as ve:
        print("OK. Did not insert duplicate key.")


    test_insert("Insert Test 3", "battingsmall", ["playerID", "yearID", "teamID", "stint"],
                {"playerID": "dff1", "teamID": "BOS", "yearID": "2018", "stint": "1",
                    "AB": "100", "H": "100"})

    test_template("Find after insert 3", "battingsmall",  ["playerID", "yearID", "teamID", "stint"],
                  {"playerID": "dff1"}, None)


def test_deletes():
    test_delete("Delete Test 1", "peoplesmall", ["playerID"],
                {"playerID": "dff1", "nameLast": "Ferguson", "nameFirst": "Donald"})
    try:
        test_delete("Delete Test 1", "peoplesmall", ["playerID"],
                {"playerID": "dff2", "nameLast": "Ferguson", "nameFirst": "Donald"})
        raise ValueError("That delete should not have worked!")
    
    except ValueError as ve:
        print("OK. Did not delete the data which in not in the CSV FILE.")

def test_find_by_primary_key():
    test_primary_key("Primary Key Test1", "People", ["playerID"],
                      ["dff_chi"])
    
    test_primary_key("Primary Key Test2", "People", ["playerID"],
                      ["abbotji01"])