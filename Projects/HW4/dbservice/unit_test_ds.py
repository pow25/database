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
    for i in range(0,3):
        result = dataservice.retrieve_by_template("people", template, fields)
        print("Result = ", json.dumps(result, indent=2))

test_get_resource()

