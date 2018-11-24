
import pymysql.cursors
import pandas as pd
import json

# The database server is running somewhere in the network.
# I must specify the IP address (HW server) and port number
# (connection that SW server is listening on)
# Also, I do not want to allow anyone to access the database
# and different people have different permissions. So, the
# client must log on.



# Connect to the database over the network. Use the connection
# to send commands to the DB.
cnx = pymysql.connect(host='localhost',
                             user='dbuser',
                             password='dbuser',
                             db='lahman2017',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



# Input is a player ID. Return the database record.
# Need to add error handling.
def retrieve(playerid):
    cursor=cnx.cursor()
    q = "SELECT * FROM PEOPLE WHERE playerID='" + playerid + "';"
    print ("Query = ", q)
    cursor.execute(q);
    r = cursor.fetchone()
    return r

# Give one of our magic templates, forms a WHERE clause.
# { a: b, c: d } --> WHERE a=b and c=d. Current treats everything as a string.
# We can fix this by using MySQL connector query templayes.
def templateToWhereClause(t):
    s = ""
    for k,v in t.items():
        if s != "":
            s += " AND "
        s += k + "='" + v[0] + "'"

    if s != "":
        s = "WHERE " + s;

    return s






