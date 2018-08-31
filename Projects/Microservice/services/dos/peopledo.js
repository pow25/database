
var Waterline = require('waterline');
var dbAdaptor = require('sails-mysql');
var newdao = require('./dao');

var logging = require(
    "/Users/donaldferguson/Dropbox/ColumbiaCourse/Courses/Fall2018/W4111/Projects/Microservice/lib/logging"
);


var peopleCollection = {
    identity: 'people',
    datastore: 'default',
    primaryKey: 'id',

    attributes: {
        id: {type: 'string', required: true, columnName: "playerid"},
        last_name: {type: 'string', required: true, columnName: "nameLast"},
        first_name: {type: 'string', required: true, columnName: "nameFirst"},
        throws: {type: 'string', required: true}
    }
};

newdao.registerCollection(peopleCollection);

exports.getByQ = function(q) {
    return newdao.getByQ("people", q)
};
exports.getByPrimaryKey = function(k) {
    return newdao.getByQ("people", {id: k})
};
exports.create = function(d) {
    return newdao.create("people", d);
};





