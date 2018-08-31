/**
 * Created by donaldferguson on 8/16/18.
 */

var peopledo = require('../dos/peoplecsvdo');
var logging = require(
    "/Users/donaldferguson/Dropbox/ColumbiaCourse/Courses/Fall2018/W4111/Projects/Microservice/lib/logging"
);

var findByPrimaryKey = function(id) {
    return new Promise(function (resolve, reject) {
        d = peopledo.peopledo();
        d.findByPrimaryKey(id).then(
            function (result) {
                resolve(result);
            },
            function (error) {
                reject(error);
            });
    });
};


var findByTemplate = function(t) {
    return new Promise(function (resolve, reject) {
        d = peopledo.peopledo();
        d.findByTemplate(t).then(
            function (result) {
                resolve(result);
            },
            function (error) {
                reject(error);
            });
    });
};

exports.findByPrimaryKey = findByPrimaryKey;
exports.findByTemplate = findByTemplate;