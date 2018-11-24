# Lahman.py

# Convert to/from web native JSON and Python/RDB types.
import json

# Include Flask packages
from flask import Flask
from flask import request
import copy

from api import people

# The main program that executes. This call creates an instance of a
# class and the constructor starts the runtime.
app = Flask(__name__)

# Return the index page as HTML. This is not part of the API
@app.route('/static/lahman')
def root():
    fn = "index.html"
    print("Trying to send file: ", fn)
    return app.send_static_file(fn)


# Retrieve metadata about people.
@app.route('/people/metadata')
def people_fields():
    result = people.retrieve_metadata("people")
    result = json.dumps(result)
    return result, 200, {'Content-Type': 'application/json; charset=utf-8'}

# Get metadata to help populate search and data entry forms.
def retrieve_metadata(table):
    cursor = cnx.cursor()
    q = "SHOW FIELDS FROM " + table + ";"
    print("Query = ", q)
    cursor.execute(q)
    r = cursor.fetchall()
    return r


if __name__ == '__main__':
    app.run()




