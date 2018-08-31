/**
 * Created by donaldferguson on 8/12/18.
 */

let path_base = "/Users/donaldferguson/Dropbox/ColumbiaCourse/Courses/Fall2018/E6156/Projects/FirstMicroservice/";
let logging = require(path_base + "lib/logging");
var mysql = require('promise-mysql');

mysql.createConnection({
    host: 'localhost',
    user: 'dbuser',
    password: 'dbuser'
}).then(function(conn){
    var result = conn.query('select * from e6156.customers');
    conn.end();
    return result;
}).then(function(rows){
    // Logs out a list of hobbits
    console.log(rows);
});

