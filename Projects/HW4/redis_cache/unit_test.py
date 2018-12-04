import sys
sys.path.insert(0, '../')
from redis_cache import data_cache

t = {"playerID": "willite01", "nameLast": "Williams", "bats": "R"}
r = data_cache.compute_key("people", {"playerID": "willite01", "nameLast": "Williams", "bats": "R"}, \
                           ['nameLast', "birthCity"])

def test1():
    print("********************test1**************************")
    print("The value is:", t)
    print("The key computed is:", r)
    data_cache.add_to_cache(r, t)

def test2():
    print("********************test2**************************")
    result = data_cache.get_from_cache(r)
    print("Result = ", result)

def test3():
    print("********************test3**************************")
    print("We try to find the value in redis with wrong-key")
    result = data_cache.get_from_cache("WRONG_KEY")
    print("Result = ", result)

query_result = [{"nameLast":"Williams", "birthCity":"San Diego"}]

def test4():
    print("********************test4**************************")
    print("Test about check_query_cache")
    print("Try to find the value that doesn't exist in redis")
    result = data_cache.check_query_cache("people", {"playerID": "willite01", "nameLast": "Williams", "bats": "R"}, \
                     ['nameLast', "birthCity"])
    print("Result = ",result)

def test5():
    print("********************test5**************************")
    print("first call add_to_query_cache to add the query result into redis")
    print("Query result:",query_result)
    print("Then call check_quer_cache to see the result returned")
    key = data_cache.add_to_query_cache("people", {"playerID": "willite02", "nameLast": "Williams", "bats": "R"}, \
                                        ['nameLast', "birthCity"], query_result)
    result = data_cache.check_query_cache("people", {"playerID": "willite02", "nameLast": "Williams", "bats": "R"}, \
                     ['nameLast', "birthCity"])
    print("Result = ",result)
    print("The key is:",key)

def test6():
    print("********************test6**************************")
    print("same as test5, but now query result has two iterms")
    query_result =  [{"nameLast":"Williams", "birthCity":"San Diego"},\
                     {"nameLast":"Williams", "birthCity":"Chicago"}]
    print("Query result:",query_result)
    key = data_cache.add_to_query_cache("people", {"playerID": "willite01", "nameLast": "Williams", "bats": "R"}, \
                                        ['nameLast', "birthCity"], query_result)
    result = data_cache.check_query_cache("people", {"playerID": "willite01", "nameLast": "Williams", "bats": "R"}, \
                     ['nameLast', "birthCity"])
    print("Result = ",result)
    print("The key is:",key)

test6()
