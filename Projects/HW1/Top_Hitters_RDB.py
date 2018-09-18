import pymysql
import json

cnx = pymysql.connect(host= "localhost",
                      user= "root",
                      password= "zhangchi25",
                      db="lahman2017n",
                      charset='utf8mb4',
                      cursorclass=pymysql.cursors.DictCursor)
cursor = cnx.cursor()
q = "ELECT \
Batting.playerID, \
(SELECT People.nameFirst FROM People WHERE People.playerID=Batting.playerID) as first_name, \
(SELECT People.nameLast FROM People WHERE People.playerID=Batting.playerID) as last_name, \
sum(Batting.h)/sum(batting.ab) as career_average, \
sum(Batting.h) as career_hits, \
sum(Batting.ab) as career_at_bats,\
min(Batting.yearID) as first_year, \
max(Batting.yearID) as last_year \
FROM \
Batting \
GROUP BY \
playerId \
HAVING \
career_at_bats > 200 AND last_year >= 1960 \
ORDER BY \
career_average DESC \
LIMIT 10;"

cursor.execute(q)
r = cursor.fetchall()
print(json.dumps(r, indent=2))