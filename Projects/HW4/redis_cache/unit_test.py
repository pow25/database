import sys
sys.path.insert(0, '../')
from redis_cache import data_cache

t = {"playerID": "willite01", "nameLast": "Williams", "bats": "R"}
r = data_cache.compute_key("people", {"playerID": "willite01", "nameLast": "Williams", "bats": "R"}, \
                           ['nameLast', "birthCity"])

def test1():
    data_cache.add_to_cache(r, t)

def test2():
    result = data_cache.get_from_cache(r)
    print("Result = ", result)

def test3():
    result = data_cache.get_from_cache("WRONG_KEY")
    print("Result = ", result)

query_result = [{"nameLast":"Williams", "birthCity":"San Diego"}]

def test4():
    result = data_cache.check_query_cache("people", {"playerID": "willite01", "nameLast": "Williams", "bats": "R"}, \
                     ['nameLast', "birthCity"])
    print("Result = ",result)

def test5():
    key = data_cache.add_to_query_cache("people", {"playerID": "willite02", "nameLast": "Williams", "bats": "R"}, \
                                        ['nameLast', "birthCity"], query_result)
    result = data_cache.check_query_cache("people", {"playerID": "willite02", "nameLast": "Williams", "bats": "R"}, \
                     ['nameLast', "birthCity"])
    print(result)

# test5()
