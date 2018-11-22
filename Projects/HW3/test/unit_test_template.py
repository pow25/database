import sys
sys.path.insert(0, '../src')
import CSVCatalog
import CSVTable
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

def test_find_by_template():

    cleanup()
    print_test_separator("Starting test_find_by_template")

    cat = CSVCatalog.CSVCatalog()
    cds = []

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCity", "text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCountry", "text"))
    cds.append(CSVCatalog.ColumnDefinition("throws", column_type="text"))


    t = cat.create_table("people", "../data/People.csv", cds)
    t.define_index("id_idx", ['nameLast'], "INDEX")
    print("People table metadata = \n", json.dumps(t.describe_table(), indent=2))


    people_tbl = CSVTable.CSVTable("people")
    print("Loaded people table = \n", people_tbl)

    tries = 1000
    start_time = time.time()
    templ = { "nameLast": "Williams"}
    print("Starting test on find using indexed field, tmpl = ", json.dumps(templ))
    for i in range(0, tries):
        result = people_tbl.find_by_template(templ, ['playerID', 'nameLast', 'nameFirst'])
        if i == 0:
            print("Sample result = ", result)
    end_time = time.time()
    print("Elapsed time for ", tries, "lookups = ", end_time-start_time)

    tries = 1000
    start_time = time.time()
    templ = {"nameFirst": "Ted"}
    print("\n\nStarting test on find using NON-indexed field, tmpl = ", json.dumps(templ))
    for i in range(0, tries):
        result = people_tbl.find_by_template(templ, ['playerID', 'nameLast', 'nameFirst'])
        if i == 0:
            print("Sample result = ", result)
    end_time = time.time()
    print("Elapsed time for ", tries, "lookups = ", end_time - start_time)

    print_test_separator("Complete test_finf_by_template")

def test_find_by_template_fail():
    #the program should fail because the table name is incorrect
    cleanup()
    print_test_separator("Starting test_find_by_template_fail")

    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCity", "text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCountry", "text"))
    cds.append(CSVCatalog.ColumnDefinition("throws", column_type="text"))
    cds.append(CSVCatalog.ColumnDefinition("birthYear", "number"))

    t = cat.create_table("people", "../data/People.csv", cds)
    t.define_index("id_idx1", ['nameLast'], "INDEX")
    t.define_index("id_idx2", ['nameFirst'], "INDEX")
    t.define_index("id_idx3", ['playerID'], "INDEX")

    try:
        CSVTable.CSVTable("people_error")
    except Exception as e:
        print("The program raise error normally:",e)
        print_test_separator("Complete test_finf_by_template_fail")
        return
    print("!!!The program should raise a error!") 

def test_find_by_template2():
    '''
    try to test whether the program will choose the optimal index for find_by_template
    '''
    cleanup()
    print_test_separator("Starting test_find_by_template2")

    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCity", "text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCountry", "text"))
    cds.append(CSVCatalog.ColumnDefinition("throws", column_type="text"))
    cds.append(CSVCatalog.ColumnDefinition("birthYear", "number"))

    t = cat.create_table("people", "../data/People.csv", cds)
    t.define_index("id_idx1", ['nameLast'], "INDEX")
    t.define_index("id_idx2", ['nameFirst'], "INDEX")
    t.define_index("id_idx3", ['playerID'], "INDEX")
    print("People table metadata = \n", json.dumps(t.describe_table(), indent=2))
    print("The idx selectivity for id_idx1:",t.get_index_selectivity('id_idx1') )
    print("The idx selectivity for id_idx2:",t.get_index_selectivity('id_idx2') )
    print("The idx selectivity for id_idx3:",t.get_index_selectivity('id_idx3') )

    people_tbl = CSVTable.CSVTable("people")
    print("Loaded people table = \n", people_tbl)

    tries = 1000
    start_time = time.time()
    templ = { "nameLast": "Williams", "nameFirst":"Mike", "playerID":"willimi03"}
    print("Starting test on find using indexed field, tmpl = ", json.dumps(templ))
    for i in range(0, tries):
        result = people_tbl.find_by_template(templ, ['playerID', 'nameLast', 'nameFirst', 'birthCity'])
        if i == 0:
            print("Sample result = ", result)
    end_time = time.time()
    print("The index used for find by template is:",people_tbl.print_used_index_during_find_by_template())
    print("Elapsed time for ", tries, "lookups = ", end_time-start_time)
    
    print_test_separator("Now we drop the id_idx3:playerID")
    t.drop_index('id_idx3')
    
    people_tbl2 = CSVTable.CSVTable("people")
    print("Loaded people table = \n", people_tbl2)
    
    tries = 1000
    start_time = time.time()
    templ = { "nameLast": "Williams", "nameFirst":"Mike", "playerID":"willimi03"}
    print("Starting test on find using indexed field, tmpl = ", json.dumps(templ))
    for i in range(0, tries):
        result = people_tbl2.find_by_template(templ, ['playerID', 'nameLast', 'nameFirst', 'birthCity'])
        if i == 0:
            print("Sample result = ", result)
    end_time = time.time()
    print("The index used for find by template is:",people_tbl2.print_used_index_during_find_by_template())
    print("Elapsed time for ", tries, "lookups = ", end_time-start_time)
    print_test_separator("Complete test_finf_by_template2")

test_find_by_template()
test_find_by_template_fail()
test_find_by_template2()