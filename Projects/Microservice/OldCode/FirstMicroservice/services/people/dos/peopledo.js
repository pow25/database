
var Waterline = require('waterline');
var dbAdaptor = require('sails-mysql');
var logging = require('/Users/donaldferguson/Dropbox/ColumbiaCourse/Courses/Fall2018/lib/logging');

var d = require(
    "/Users/donaldferguson/Dropbox/ColumbiaCourse/Courses/Fall2018/W4111/Projects/Microservice/OldCode/FirstMicroservice/lib/wdao"
);
var dbAdaptor = require('sails-mysql');
var config = {
    adapters: {
        'db': dbAdaptor
    },

    datastores: {
        default: {
            adapter: 'db',
            url: 'mysql://dbuser:dbuser@localhost:3306/lahman2017'
        }
    }
};

var peopleCollection = {
    identity: 'people',
    datastore: 'default',
    primaryKey: 'playerid',

    attributes: {
        playerid: {type: 'string', required: true},
        last_name: {type: 'string', required: true, columnName: "nameLast"},
        first_name: {type: 'string', required: true, columnName: "nameFirst"},
        throws: {type: 'string', required: true}
    }

};

var theDao = new d.wdao(config, peopleCollection, "people");


theDao.getByQ({last_name: "Williams"}).then(
    function(result) {
        console.log(result);
    }
);