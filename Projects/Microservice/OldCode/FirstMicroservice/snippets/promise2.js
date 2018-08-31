/**
 * Created by donaldferguson on 8/12/18.
 */

let path_base = "/Users/donaldferguson/Dropbox/ColumbiaCourse/Courses/Fall2018/E6156/Projects/FirstMicroservice/";
let logging = require(path_base + "lib/logging");
var mysql = require('promise-mysql');

fastC = mysql.createConnection({
    host: 'localhost',
    user: 'dbuser',
    password: 'dbuser'
});
slowC = mysql.createConnection(
    {
        host: "columbiae6156.cqgsme1nmjms.us-east-1.rds.amazonaws.com",
        user: "dbuser2",
        password: "dbuser2"
    });

y = Promise.all([fastC, slowC]).then(
    function(results) {
        "use strict";
        logging.debug_message("Both connections completed!");
        let fastA = results[0].query("select * from e6156.customers;")
        let slowA = results[1].query("select * from cloude6156.customers;");
        results[0].end();
        results[1].end();
        return Promise.all([fastA, slowA])
    }
);

y.then(
    function(results) {
        "use strict";
        for (var i = 0; i < results.length; i++) {
            logging.debug_message("Database[" + i + "] returned ", results[i]);
        }
    });