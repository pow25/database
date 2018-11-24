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

def parse_url(url):
 
    a = url.find("offset", 0)
    b = url.find("&", a)
    if b != -1:
        temp = url[:a] + url[b+1:]
    else:
        temp = url[:a-1]

    a = temp.find("limit",0)
    b = temp.find("&", a)
    if b != -1:
        result = temp[:a] + temp[b+1:]
    else:
        result = temp[:a-1]
    
    return result


@app.route('/api/roster', methods=['GET'])
def roster():
    in_args, fields, body, limit, offset = parse_and_print_args()
    url = request.url
    url_res = []
    url_res.append({"current":url })
    if offset != None and limit != None:
        url = parse_url(url)
        offset = (int)(offset[0])
        limit = (int)(limit[0])
        if limit > 10:
            limit = 10
    else:
        limit = 10
        offset = 0
    
    if request.method == 'GET':
        try:
            result = SimpleBO.roster(in_args)
        except Exception as e:
            return "Got Exception:" + str(e) +" ", 501, {"content-type": "text/plain; charset: utf-8"}    
    

        if len(result) > limit:
            result = result[offset:limit+offset]
            offset += limit
            url_res.append({"next":url + "&offset=" + str(offset) + "&limit=" + str(limit) })
        
        if len(result) > 0:
            result.append(url_res)
        else:
            result = url_res
            
        return json.dumps(result), 200, \
               {"content-type": "application/json; charset: utf-8"}    
    else:
        return "Method " + request.method + " on roster" + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}


@app.route('/api/people/<playerid>/career_stats', methods=['GET'])
def career_stats(playerid):

    in_args, fields, body, limit, offset = parse_and_print_args()
    url = request.url
    url_res = []
    url_res.append({"current":url })
    if offset != None and limit != None:
        url = parse_url(url)
        offset = (int)(offset[0])
        limit = (int)(limit[0])
        if limit > 10:
            limit = 10
    else:
        limit = 10
        offset = 0

    if request.method == 'GET':
        try:
            result = SimpleBO.career_stats(playerid)
        except Exception as e:
            return "Got Exception:" + str(e) +" ", 501, {"content-type": "text/plain; charset: utf-8"}    
        
        if len(result) > limit:
            result = result[offset:limit+offset]
            offset += limit
            url_res.append({"next":url + "&offset=" + str(offset) + "&limit=" + str(limit) })
        
        if len(result) > 0:
            result.append(url_res)
        else:
            result = url_res

        return json.dumps(result), 200, \
               {"content-type": "application/json; charset: utf-8"}    
    else:
        return "Method " + request.method + " on career stats" + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}


@app.route('/api/teammates/<playerid>', methods=['GET'])
def teammates(playerid):

    in_args, fields, body, limit, offset = parse_and_print_args()
    url = request.url
    url_res = []
    url_res.append({"current":url })
    if offset != None and limit != None:
        url = parse_url(url)
        offset = (int)(offset[0])
        limit = (int)(limit[0])
        if limit > 10:
            limit = 10
    else:
        limit = 10
        offset = 0

    if request.method == 'GET':
        try:
            result = SimpleBO.teammate(playerid)
        except Exception as e:
            return "Got Exception:" + str(e) +" ", 501, {"content-type": "text/plain; charset: utf-8"}    
        
        if len(result) > limit:
            result = result[offset:limit+offset]
            offset += limit
            url_res.append({"next":url + "&offset=" + str(offset) + "&limit=" + str(limit) })
        
        if len(result) > 0:
            result.append(url_res)
        else:
            result = url_res

        return json.dumps(result), 200, \
               {"content-type": "application/json; charset: utf-8"}    
    else:
        return "Method " + request.method + " on teammates" + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}


@app.route('/api/<resource>/<primary_key>/<related_resource>', methods=['GET', 'POST'])
def dependent_resource(resource, primary_key, related_resource):
    in_args, fields, body, limit, offset = parse_and_print_args()
    url = request.url
    url_res = []
    url_res.append({"current":url })
    if offset != None and limit != None:
        url = parse_url(url)
        offset = (int)(offset[0])
        limit = (int)(limit[0])
        if limit > 10:
            limit = 10
    else:
        limit = 10
        offset = 0

    try:
        template = SimpleBO.parse_primary_key(resource,primary_key)
    except Exception as e:
        return "Got Exception:" + str(e) +" ", 501, {"content-type": "text/plain; charset: utf-8"}
    
    if request.method == 'GET':
        try:
            result_temp = SimpleBO.find_by_template(resource, template)
            
            if not bool(result_temp):
                return "Find noting by primarykey", 200, {"content-type": "application/json; charset: utf-8"}
            
            relate = SimpleBO.get_foreign_key(resource,result_temp)
            result = SimpleBO.find_by_template(related_resource, relate, fields)

        except Exception as e:
            return "Got Exception:" + str(e) +" ", 501, {"content-type": "text/plain; charset: utf-8"}

        if len(result) > limit:
            result = result[offset:limit+offset]
            offset += limit
            url_res.append({"next":url + "&offset=" + str(offset) + "&limit=" + str(limit) })
        
        if len(result) > 0:
            result.append(url_res)
        else:
            result = url_res

        return json.dumps(result), 200, \
               {"content-type": "application/json; charset: utf-8"}
    
    elif request.method == 'POST':
        try:
            SimpleBO.insert(related_resource,body)
        except Exception as e:
            return "Got Exception:" + str(e) +" ", 501, {"content-type": "text/plain; charset: utf-8"}
        
        return "Update Finished", 200, {"content-type": "text/plain; charset: utf-8"}

    else:
        return "Method " + request.method + " on resource " + resource + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}


@app.route('/api/<resource>/<primary_key>', methods=['GET', 'PUT', 'DELETE'])
def get_resource_primary_key(resource,primary_key):
    in_args, fields, body, limit, offset = parse_and_print_args()
    url = request.url
    url_res = []
    url_res.append({"current":url })
    if offset != None and limit != None:
        url = parse_url(url)
        offset = (int)(offset[0])
        limit = (int)(limit[0])
        if limit > 10:
            limit = 10
    else:
        limit = 10
        offset = 0

    try:
        template = SimpleBO.parse_primary_key(resource,primary_key)
    except Exception as e:
        return "Got Exception:" + str(e) +" ", 501, {"content-type": "text/plain; charset: utf-8"}

    if request.method == 'GET':
        try:
            result = SimpleBO.find_by_template(resource, template, fields)
        except Exception as e:
            return "Got Exception:" + str(e) +" ", 501, {"content-type": "text/plain; charset: utf-8"}
        
        if len(result) > limit:
            result = result[offset:limit+offset]
            offset += limit
            url_res.append({"next":url + "&offset=" + str(offset) + "&limit=" + str(limit) })
        
        if len(result) > 0:
            result.append(url_res)
        else:
            result = url_res
       
        return json.dumps(result), 200, \
               {"content-type": "application/json; charset: utf-8"}
    
    elif request.method == 'PUT':
        try:
            SimpleBO.update(resource,template,body)
        except Exception as e:
            return "Got Exception:" + str(e) +" ", 501, {"content-type": "text/plain; charset: utf-8"}
        
        return "Update Finished", 200, {"content-type": "text/plain; charset: utf-8"}
    
    elif request.method == 'DELETE':
        try:
            SimpleBO.delete(resource,template)
        except Exception as e:
            return "Got Exception:" + str(e) +" ", 501, {"content-type": "text/plain; charset: utf-8"}
        
        return "Delete Finished", 200, {"content-type": "text/plain; charset: utf-8"} 
    else:
        return "Method " + request.method + " on resource " + resource + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}


@app.route('/api/<resource>', methods=['GET', 'POST'])
def get_resource(resource):
    in_args, fields, body, limit, offset = parse_and_print_args()
    url = request.url
    url_res = []
    url_res.append({"current":url })
    if offset != None and limit != None:
        url = parse_url(url)
        offset = (int)(offset[0])
        limit = (int)(limit[0])
        if limit > 10:
            limit = 10
    else:
        limit = 10
        offset = 0

    if request.method == 'GET':
        try:
            result = SimpleBO.find_by_template(resource, in_args, fields)
        except Exception as e:
            return "Got Exception:" + str(e) +" ", 501, {"content-type": "text/plain; charset: utf-8"}
        
        if len(result) > limit:
            result = result[offset:limit+offset]
            offset += limit
            url_res.append({"next":url + "&offset=" + str(offset) + "&limit=" + str(limit) })
        
        if len(result) > 0:
            result.append(url_res)
        else:
            result = url_res
        
        return json.dumps(result), 200, \
               {"content-type": "application/json; charset: utf-8"}
    
    elif request.method == 'POST':
        try:
            SimpleBO.insert(resource,body)
        except Exception as e:
            return "Got Exception:" + str(e) +" ", 501, {"content-type": "text/plain; charset: utf-8"}
        
        return "Insert Finished", 200, {"content-type": "text/plain; charset: utf-8"}
    else:
        return "Method " + request.method + " on resource " + resource + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}


if __name__ == '__main__':
    app.run()