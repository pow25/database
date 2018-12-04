import sys
sys.path.insert(0, '../')
from dbservice import dataservice
import utils.utils as ut
import json

ut.set_debug_mode(False)
dataservice.set_config()

template = {
    "nameLast": "Williams",
    "nameFirst": "Ted"
}

fields = ['playerID', 'nameFirst', 'bats', 'birthCity']


def test_get_resource():
    print("template is:",template)
    print("fields is:",fields)
    print("Run retrieve_by_template 3 times:\n")
    for i in range(0,3):
        result = dataservice.retrieve_by_template("people", template, fields)
        print("Result = ", json.dumps(result, indent=2))

def test_get_resource_different_fields():
    print("template is the same:", template)
    fields_new = ['playerID', 'nameFirst', 'birthCity']
    print("different fields:",fields_new)
    print("it should cause MISS!")
    result = dataservice.retrieve_by_template("people", template, fields_new)
    print("Result = ", json.dumps(result, indent=2))

def test_get_resource_multiple_result():
    print("Instead of just one query result, now it will return multiple, limit = 5")
    new_template =  {"nameLast": "Williams"}
    print("template is:",new_template)
    print("fields is:",fields)
    print("Run retrieve_by_template 3 times:\n")
    for i in range(0,3):
        result = dataservice.retrieve_by_template("people", new_template, fields, limit=5)
        print("Result = ", json.dumps(result, indent=2))

# test_get_resource()
# test_get_resource_different_fields()
# test_get_resource_multiple_result()