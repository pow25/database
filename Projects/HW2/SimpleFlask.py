# Lahman.py

# Convert to/from web native JSON and Python/RDB types.
import json

# Include Flask packages
from flask import Flask
from flask import request
import copy

import SimpleBO

# The main program that executes. This call creates an instance of a
# class and the constructor starts the runtime.
app = Flask(__name__)

def parse_and_print_args():

    fields = None
    in_args = None
    limit = None
    offset = None
    if request.args is not None: #there may include offset, limit, fields(fields handling below)
        in_args = dict(copy.copy(request.args))
        fields = copy.copy(in_args.get('fields', None)) #we get fields
        limit = copy.copy(in_args.get('limit', None))
        offset = copy.copy(in_args.get('offset', None))
        if fields:
            del(in_args['fields']) #then we delete it from the original args, becasue we don't need that anymore
        if limit:
            del(in_args['limit'])
        if offset:
            del(in_args['offset'])
    try:
        if request.data:
            body = json.loads(request.data)
        else:
            body = None
    except Exception as e:
        print("Got exception = ", e)
        body = None

    print("Request.args : ", json.dumps(in_args))
    return in_args, fields, body, limit, offset

@app.route('/api/<roster>', methods=['GET'])
def roaster(roster):
    in_args, fields, body, limit, offset = parse_and_print_args()
    # if request.method == 'GET':



@app.route('/api/<resource>', methods=['GET', 'POST'])
def get_resource(resource):

    in_args, fields, body, limit, offset = parse_and_print_args()

    if request.method == 'GET':
        try:
            result = SimpleBO.find_by_template(resource, \
                                           in_args, limit, offset,fields)
        except Exception as e:
            return "Got Exception:" + e +" ", 501, {"content-type": "text/plain; charset: utf-8"}
        
        return json.dumps(result), 200, \
               {"content-type": "application/json; charset: utf-8"}
    
    elif request.method == 'POST':
        try:
            SimpleBO.insert(resource,body)
        except Exception as e:
            return "Got Exception:" + e +" ", 501, {"content-type": "text/plain; charset: utf-8"}
        
        return "Insert Finished", 200, {"content-type": "text/plain; charset: utf-8"}
    else:
        return "Method " + request.method + " on resource " + resource + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}




if __name__ == '__main__':
    app.run()

