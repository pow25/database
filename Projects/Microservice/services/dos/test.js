/**
 * Created by donaldferguson on 8/16/18.
 */

var peopledo = require('./peopledo');
var logging = require(
    "/Users/donaldferguson/Dropbox/ColumbiaCourse/Courses/Fall2018/W4111/Projects/Microservice/lib/logging"
);
var dao = require('./dao');

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

d = new dao.thedao(peopleCollection);
d.retrieveByTemplate({ last_name: "Williams", throws: "L"}).then(
    function(result) {
        logging.debug_message("Result = ", result);
    }
);