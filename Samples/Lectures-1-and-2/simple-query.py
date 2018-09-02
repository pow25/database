
import csv
import json

data_dir = "/Users/donaldferguson/Dropbox/ColumbiaCourse/Courses/Fall2018/W4111/Data/"

def findByPlayerID(id):
    with open(data_dir + "People.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['playerID'] == id:
                result = row
                return result
        else:
            return None


def templateToWhereClause(t):
    s = ""
    for (k,v) in t.items():
        if s != "":
            s += " AND "
        s += k + "='" + v + "'"

    if s != "":
        s = "WHERE " + s;

    return s



t = { "nameLast" : "Williams", "nameFirst": "Ted"}
print(templateToWhereClause(t))


def test1():
    playerID = input("Enter a player's ID: ")
    print("The player is ", json.dumps(findByPlayerID(playerID), indent=3))