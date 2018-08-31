/**
 * Created by donaldferguson on 8/20/18.
 */

// jshint node: true

var csvdao = require('./csvdao');

var logging = require('/Users/donaldferguson/Dropbox/ColumbiaCourse/Courses/Fall2018/lib/logging');

var collection = { identity: "small", primaryKey: "playerID"};

exports.peopledo = function() {
    d = new csvdao.Dao(collection);
    return d;
};

var d = new csvdao.Dao(collection);
d.findByPrimaryKey("aasedo01").then(
    function(result) {
        logging.debug_message("Loaded.")
        d.saveRecords().then(
            function(result) {
                logging.debug_message("Saved")
            },
            function(error) {
                logging.error_message("Boom")
            });
    });





