import csv
import json
import CSVTable
import sys,os

rel_path = os.path.realpath('./data')
rel_path += '/'


csvt_people = CSVTable("People", "PeopleSmall.csv", ["playerID"])
csvt_batting = CSVTable("Batting", "BattingSmall.csv", ["playerID"])
csvt_people.load()
csvt_batting.load()


