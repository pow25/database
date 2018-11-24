import sys
sys.path.insert(0, '../src')
import CSVCatalog
import CSVTable

import time
import json

data_dir = "../data/"

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


def test_join_optimized():

    cleanup()
    print_test_separator("Starting test_optimizable_1")

    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCity", "text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCountry", "text"))
    cds.append(CSVCatalog.ColumnDefinition("throws", column_type="text"))

    t = cat.create_table(
        "people",
        data_dir + "People.csv",
        cds)
    print("People table metadata = \n", json.dumps(t.describe_table(), indent=2))

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("H", "number", True))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number"))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))

    t = cat.create_table(
        "batting",
        data_dir + "Batting.csv",
        cds)
    print("Batting table metadata = \n", json.dumps(t.describe_table(), indent=2))

    people_tbl = CSVTable.CSVTable("people")
    batting_tbl = CSVTable.CSVTable("batting")

    print("Loaded people table = \n", people_tbl)
    print("Loaded batting table = \n", batting_tbl)

    start_time = time.time()

    tmp = { "playerID": "willite01"}
    join_result = people_tbl.join(batting_tbl,['playerID'], tmp)

    end_time = time.time()

    print("Result = \n", join_result)
    elapsed_time = end_time - start_time
    print("\n\nElapsed time = ", elapsed_time)

    print_test_separator("Complete test_join_optimizable")


def test_join_optimizable_2():
    """
    Calling this with optimize=True turns on optimizations in the JOIN code.
    :return:
    """
    cleanup()
    print_test_separator("Starting test_optimizable_2")

    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCity", "text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCountry", "text"))
    cds.append(CSVCatalog.ColumnDefinition("throws", column_type="text"))

    t = cat.create_table(
        "people",
        data_dir + "People.csv",
        cds)
    print("People table metadata = \n", json.dumps(t.describe_table(), indent=2))
    t.define_index("pid_idx", ['playerID'], 'INDEX')

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("H", "number", True))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number"))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))

    t = cat.create_table(
        "batting",
        data_dir + "Batting.csv",
        cds)
    print("Batting table metadata = \n", json.dumps(t.describe_table(), indent=2))

    people_tbl = CSVTable.CSVTable("people")
    batting_tbl = CSVTable.CSVTable("batting")

    print("Loaded people table = \n", people_tbl)
    print("Loaded batting table = \n", batting_tbl)

    start_time = time.time()

    join_result = people_tbl.join(batting_tbl,['playerID'], None)

    end_time = time.time()

    print("Result = \n", join_result)
    elapsed_time = end_time - start_time
    print("\n\nElapsed time = ", elapsed_time)

    print_test_separator("Complete test_join_optimizable_2")


def test_join_optimizable_3():
    """

    :return:
    """
    cleanup()
    print_test_separator("Starting test_optimizable_3")

    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCity", "text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCountry", "text"))
    cds.append(CSVCatalog.ColumnDefinition("throws", column_type="text"))

    t = cat.create_table(
        "people",
        data_dir + "People.csv",
        cds)
    t.define_index("pid_idx", ['playerID'], "INDEX")
    print("People table metadata = \n", json.dumps(t.describe_table(), indent=2))

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("H", "number", True))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number"))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))

    t = cat.create_table(
        "batting",
        data_dir + "Batting.csv",
        cds)
    print("Batting table metadata = \n", json.dumps(t.describe_table(), indent=2))
    t.define_index("pid_idx", ['playerID'], "INDEX")

    people_tbl = CSVTable.CSVTable("people")
    batting_tbl = CSVTable.CSVTable("batting")

    print("Loaded people table = \n", people_tbl)
    print("Loaded batting table = \n", batting_tbl)

    start_time = time.time()

    tmp = {"playerID": "willite01"}
    join_result = people_tbl.join(batting_tbl,['playerID'], tmp)

    end_time = time.time()

    print("Result = \n", join_result)
    elapsed_time = end_time - start_time
    print("\n\nElapsed time = ", elapsed_time)

    print_test_separator("Complete test_join_optimizable_3")

def test_join_optimizable_4():
    """
    join batting and team
    :return:
    """
    cleanup()
    print_test_separator("Starting test_optimizable_4")

    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("H", "number", True))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number"))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))
    cds.append(CSVCatalog.ColumnDefinition("lgID", "text", True))

    t = cat.create_table( "batting", data_dir + "Batting.csv",cds)
    t.define_index("pid_idx", ['playerID'], "INDEX")
    print("Batting table metadata = \n", json.dumps(t.describe_table(), indent=2))
    


    cds = []
    cds.append(CSVCatalog.ColumnDefinition("franchID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("W", column_type="number", not_null=True))
    cds.append(CSVCatalog.ColumnDefinition("lgID", "text", True))

    t = cat.create_table( "teams", data_dir + "Teams.csv", cds)
    t.define_index("pid_idx", ['yearID','teamID'], "INDEX")
    print("Teams table metadata = \n", json.dumps(t.describe_table(), indent=2))

    batting_tbl = CSVTable.CSVTable("batting")
    team_tbl = CSVTable.CSVTable("teams")
    print("Loaded batting table = \n", batting_tbl)
    print("Loaded Teams table = \n", team_tbl)
    start_time = time.time()

    tmp = {"playerID": "willite01", "yearID":"1956"}
    join_result = batting_tbl.join(team_tbl,['yearID', 'lgID','teamID'], tmp)

    end_time = time.time()
    print("Result = \n", join_result)
    elapsed_time = end_time - start_time
    print("\n\nElapsed time = ", elapsed_time)

    print_test_separator("Complete test_join_optimizable_4")

test_join_optimized()
test_join_optimizable_2()
test_join_optimizable_3()
test_join_optimizable_4()
