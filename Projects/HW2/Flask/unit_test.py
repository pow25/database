import json
import SimpleBO

def test1():
    result = SimpleBO.find_people_by_primary_key('willite01')
    print("Result = ", json.dumps(result))

test1()