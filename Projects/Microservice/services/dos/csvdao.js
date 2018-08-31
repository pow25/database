/**
 * Created by donaldferguson on 8/16/18.
 */
// jshint node: true

var data_dir =
    "/Users/donaldferguson/Dropbox/ColumbiaCourse/Courses/Fall2018/W4111/Projects/Microservice/services/data";

// Support to read from file system.
var fs = require('fs');

// Node package for reading and parsing CSV files.
var parse = require('csv-parse');

// Just a little function I wrote that wraps console.log() and adds some value.
// Real solutions use something like Winston (https://github.com/winstonjs/winston) and/or
// system logging like AWS CloudWatch (https://aws.amazon.com/cloudwatch/)
var logging = require('/Users/donaldferguson/Dropbox/ColumbiaCourse/Courses/Fall2018/lib/logging');


/*
  Simple function for loading data from a CSV file and converting to JSON.
  Single input is the file name.
  Return format is
    {
        columns: names of columns,
        rows: list of data from rows.
    }
 */
var loadData = function(fn) {

    // File operations can go asynchronous. So we either need Promises or callbacks.
    // I prefer Promises.
    return new Promise(function (resolve, reject) {

        try {
            var rows = [];
            var columns = null;

            // Open a file stream and asynchronous read the file.
            // Pipe the input stream into the CSV parser.
            fs.createReadStream(fn)
                .pipe(parse())
                .on('data', function (data) {

                    // The parser extracted a row. If columns is not set,
                    // this is the first row and hence the column definitions.
                    if (columns == null) {
                        //logging.debug_message("Headers = ", data);
                        columns = data;
                    }
                    else {
                        // Data row.
                        rows.push(data);
                        //logging.debug_message("Data = ", data);
                    }
                })
                .on('end', function () {
                    // Have read all of file. Resolve Promise with information.
                    resolve({columns: columns, rows: rows});
                });
        }
        catch(ex) {
            logging.error_message("ex = ", ex);
            reject(ex);
        }
    });
};

var saveData = function(fn, header, rows) {
    const createCsvWriter = require('csv-writer').createObjectCsvWriter;

    var h = [];
    for (var i = 0; i < header.length; i++) {
        var tmp = {id: header[i], title: header[i]};
        h.push(tmp);
    }

    const csvWriter = createCsvWriter({
        path: fn,
        header: h
    });

    return csvWriter.writeRecords(rows);
}



/*
    Function input is
    1. Column names
    2. An array of values.

    Coverts to a JSON objects with the column names being the property/field names inside each JSON object.
 */
var mergeDataAndColumns =  function(d, columns) {
    var row = {}
    for (var i=0; i < d.length; i++) {
        row[columns[i]] = d[i];
    }
    return row;
};

/*
    Input:
    1. JSON object.
    2. A template, which is also a JSON object.

    Returns true if the fields in the object match the fields in the template.
 */
var matchesTemplate = function(d, t) {
    var result = true;
    var keys = Object.keys(t);
    for (i = 0; i < keys.length; i++) {
        var k = keys[i];
        if (d[k] != t[k]) {
            return false
        }
    };
    return result;
}



/*
    Generic DAO class for CSV files. Instance data determines specifics of file managed.
    The sole input is a JSON object defining some information about how to materialize the CSV
    data to the DAO using code.
 */
var Dao = function(collection) {

    // Holds the state in a single place.
    this.daoState = {
        records: [],
        columns: null,                                      // Names of columns
        collection: collection,                             // Save the configuration info in instance
        initialized: false                                  // Set to true when initialization complete.
    };

    // This acts "odd" when used inside Promises.
    var self = this;

    this.getFileName = function() {
        // Compute the name of the file from the "identity."
        // This is lazy and there should be a more general approach.
        var fn = data_dir + "/" + self.daoState.collection.identity + ".csv";
        return fn;
    };

    // Initialze the object, which basically means load the state.
    this.init = function() {

        fn = this.getFileName();

        // Load the data and return the state that results.
        return new Promise(function (resolve, reject) {
            loadData(fn).then(
                function (result) {
                    columns = result.columns;

                    // Merge the columns names and values for each row to form JSON obkects.
                    // Save in the records of the DAO state.
                    for (var i = 0; i < result.rows.length; i++) {   //Add each row.
                        var newRow = mergeDataAndColumns(result.rows[i], columns);
                        self.daoState.records.push(newRow);
                    }
                    self.daoState.columns = columns;
                    resolve(self.daoState);
                },
                function (error) {
                    // Probably need better error handling.
                    logging.error_message("Boom!");
                    reject()
                });
        });

    }

    // Wraps the state. This ensures that any operations on the object "wait" until
    // the state is loaded and the object is initialized.
    this.getState = function() {

        if (self.daoState.initialized) {
            Promise.resolve(self.daoState);
        }
        else {
            return self.init(self);
        }
    };

    // Self explanatory.
    this.findByTemplate = function(t) {

        return new Promise(function(resolve, reject) {
            self.getState().then(
                function(result) {
                    var found = false;

                    // We got the state. Scan and look for a row matching the template.
                    var pkColumnName = self.daoState.collection.primaryKey;
                    for (var i = 0; i < result.records.length; i++) {
                        if (matchesTemplate(result.records[i], t)) {
                            resolve(result.records[i])
                        }
                    }
                    if (found == false) {
                        // Not found is NOT an error from a DB perspective. It is a correct answer.
                        resolve(null)
                    }
                },
                function(error) {
                    reject(error);
                });
        });
    };

    // Self explanatory.
    this.findByPrimaryKey = function(id) {

        return new Promise(function(resolve, reject) {
            self.getState().then(
                function(result) {
                    var found = false;

                    // We got the state. Scan and look for a row with the column with the primary key name holding
                    // the requested value.
                    var pkColumnName = self.daoState.collection.primaryKey;
                    for (var i = 0; i < result.records.length; i++) {
                        if (result.records[i][pkColumnName] == id) {
                            resolve(result.records[i])
                        }
                    }
                    if (found == false) {
                        // Not found is NOT an error from a DB perspective. It is a correct answer.
                        resolve(null)
                    }
                },
                function(error) {
                    reject(error);
                });
        });
    };

    this.saveRecords = function() {

        fn = self.getFileName();
        return saveData(fn, self.daoState.columns, self.daoState.records);

    };

    this.deleteByPrimaryKey = function(id) {
        Promise.reject("Not implemented.");
    };

    this.deleteByTemplate = function(t) {
        Promise.reject("Not implemented.");
    };

    this.update = function(id, d) {
        Promise.reject("Not implemented.");
    };

    this.create = function(d) {
        Promise.reject("Not implemented.");
    };
};

exports.Dao = Dao;









