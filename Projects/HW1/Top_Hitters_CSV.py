import csv
import json
from CSVTable import CSVTable
import sys,os

rel_path = os.path.realpath('./data')
rel_path += '/'

csvt_batting = CSVTable("Batting", "Batting.csv",["playerID"])
csvt_batting.load()

csvt = CSVTable("People", "PeopleSmall.csv", ["playerID"])
csvt.load()

player_set = csvt_batting.find_by_template_top()
player_dict = {}
for i in player_set:
    string_set =[]
    string_set.append((i))
    r = csvt_batting.find_by_primary_key(string_set,["AB","H"])
    total_ab = 0
    total_h = 0
    for j in r:
        total_ab += int(j["AB"])
        total_h += int(j["H"]) 
    player_dict[i] = float(total_h)/total_ab

player_dict_sorted = sorted(player_dict.items(),key = lambda x:x[1],reverse = True)

final_result = []
for i in player_dict_sorted:
    string_set = []
    string_set.append(i[0])
    r = csvt.find_by_primary_key(string_set)
    final_result.append(r)
    
    if len(final_result) == 10:
        break

print(json.dumps(final_result, indent=2))