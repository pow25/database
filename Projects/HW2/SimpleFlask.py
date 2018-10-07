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
    if request.args is not None:
        in_args = dict(copy.copy(request.args))
        fields = copy.copy(in_args.get('fields', None))
        if fields:
            del(in_args['fields'])

    try:
        if request.data:
            body = json.loads(request.data)
        else:
            body = None
    except Exception as e:
        print("Got exception = ", e)
        body = None



    print("Request.args : ", json.dumps(in_args))
    return in_args, fields, body


@app.route('/api/<resource>', methods=['GET', 'POST'])
def get_resource(resource):

    in_args, fields, body = parse_and_print_args()
    if request.method == 'GET':
        result = SimpleBO.find_by_template(resource, \
                                           in_args, fields)
        return json.dumps(result), 200, \
               {"content-type": "application/json; charset: utf-8"}
    elif request.method == 'POST':
        print("This would be a really good place to call insert()")
        print("on table ", resource)
        print("with row ", body)
        print("But there has to be some HW not written in class.")
        return "Method " + request.method + " on resource " + resource + \
            " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}
    else:
        return "Method " + request.method + " on resource " + resource + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}


if __name__ == '__main__':
    app.run()

