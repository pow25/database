# Lahman.py

# Convert to/from web native JSON and Python/RDB types.
import json

# Include Flask packages
from flask import Flask
from flask import request

from api import people

# The main program that executes. This call creates an instance of a
# class and the constructor starts the runtime.
app = Flask(__name__)


# Annotation that attaches a new method to the app specifying which URL it handles.
# This one handles just the "/" URL.
@app.route('/api')
def hello_world():
    print(request.query_string)
    return 'Hello World! Maybe you should ask questions about People or Batting?'

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

# Add a function to handle a URL of the form /people/id, e.g. /people/willite01
# The functions parameter playerid will be set to the <playerid> part of the URL.
@app.route('/api/people/<playerid>')
def people_by_id(playerid):
    # Call the database access later to get data.
    result = people.retrieve(playerid)
    # Convert to JSON
    result = json.dumps(result)

    # 200 means OK.
    # We have to add logic to handle not found, errors, etc.
    # But this is not a web app development class.
    return result, 200, {'Content-Type': 'application/json; charset=utf-8'}


# Same basic idea but returns a JSON object of the form
# {
#   player: { playerifo },
#   batting: [{ batting year }, { batting year } ... ]
@app.route('/api/people/<playerid>/batting')
def people_batting(playerid):
    result = people.retrieve_batting(playerid)
    result = json.dumps(result)
    return result, 200, {'Content-Type': 'application/json; charset=utf-8'}


# This is one is a little freaky.
# It converts a query string to a template and then queries by template.
# Looking for a person could use a query string like
# /people?nameLast=Williams&throws=l?fields=x,y,z
# This finds a player with nameLast=Willians and throws=l, and gets fields x, y and z.
@app.route('/api/<resource_name>')
def get_resource(resource_name):
    # This is a SERIOUSLY icky segment of code.
    # I was lazy. There are much better approaches.

    # The basic idea is:
    # I need to get fields and the query parameters out of the URL.
    #
    # I then need to reconstruct the original URL but add new offset and limit
    # query parameters.

    # Get the arguments from the path and query.
    template = dict(request.args)

    # Get the "fields=..." query parameters if it exists.
    original_fields = template.get("fields", None)

    if original_fields is not None:
        # I need to remove "fields=..." from the code that will format
        # where clause.
        del (template['fields'])

        # This is the string that follows SELECT to choose fields.
        fields = "".join(original_fields)

        # Will need the original format to but back into URLs for next, previous, etc.
        original_fields = "fields=" + fields
    else:
        fields = " * "
        original_fields = None

    # Get the limit if it exists.
    # Remove from query template because does not go into where clause.
    # Pick a default limit
    limit = template.get("limit", None)
    if limit is not None:
        limit = int(limit[0])
        del (template['limit'])
    else:
        # Default
        limit = 10

    # Make sure we do not exceed maximum limit.
    if limit > 10:
        limit = 10

    # Similar logic for offset.
    offset = template.get("offset", None)
    if offset is not None:
        offset = int(offset[0])
        del (template['offset'])
    else:
        offset = 0

    # Recompute the original query string, but without offset, limit or fields.
    original_q = None
    for k, v in template.items():
        if original_q is None:
            original_q = ''
        else:
            original_q += "&"
        original_q += k + "=" + str(v[0])

    # Add in the API prefix and resource name preceeding the query string.
    original_url = '/api/' + resource_name

    new_suffix = ''

    # If there is no query string, there WILL be an offset and limit.
    # So, we need to insert a ?
    if original_q is None:
        new_suffix = '?'
    else:
        new_suffix = '?' + original_q

    # Add fields back into query string.
    if original_fields is not None:
        if new_suffix == '?':
            new_suffix += original_fields
        else:
            new_suffix += "&" + original_fields

    # We are going to insert offset and limit. So, we need a "&"
    if new_suffix != '':
        new_suffix = new_suffix + "&"

    # Finally, we call the database.
    data = people.retrieve_by_template(resource_name, template, fields, limit, offset)

    # Compute the next and previous links.
    next_offset = offset + limit
    previous_offset = offset - limit

    # More fun trying to reconstruct original query.
    if original_q is None:
        original_q = "?"
    else:
        original_q = original_q + "&"
    original_url = original_url + new_suffix

    # This is a URL/link to the CURRENT page. This is not quite correct.
    # I should only add offsets if necessary.
    current_link = {"current": original_url + "offset=" + str(offset) + "&limit=" + str(limit)}
    links = [current_link]

    # Are there more, that is did the database return a full page implying that there may be more
    # records matching the query.
    if len(data) == limit:
        next_link = {"next": original_url + "offset=" + str(next_offset) + "&limit=" + str(limit)}
        links.append(next_link)

    # Is there a preceeding page?
    if previous_offset >= 0:
        previous_link = {"previous": original_url + "offset=" + str(previous_offset) + "&limit=" + str(limit)}
        links.append(previous_link)

    result = {"data": data, "links": links}
    result = json.dumps(result)

    return result, 200, {'Content-Type': 'application/json; charset=utf-8'}


# Retrieve metadata about people.
@app.route('/api/people/metadata')
def people_fields():
    result = people.retrieve_metadata("people")
    result = json.dumps(result)
    return result, 200, {'Content-Type': 'application/json; charset=utf-8'}


if __name__ == '__main__':
    app.run()




