/**
 * Created by donaldferguson on 8/16/18.
 */
// jshint node: true

var Waterline = require('waterline');
var dbAdaptor = require('sails-mysql');
var logging = require('/Users/donaldferguson/Dropbox/ColumbiaCourse/Courses/Fall2018/lib/logging');

var waterline = new Waterline();
var ontology = null;

var global_config = {
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


var registerCollection = function(c) {
    var wCollection = Waterline.Collection.extend(c);
    waterline.registerModel(wCollection);
};



var getOntology = function() {
    "use strict";
    return new Promise(function (resolve, reject) {
        if (ontology != null) {
            Promose.resolve(ontology);
        }
        else {
            waterline.initialize(global_config, function (err, result) {
                if (err) {
                    logging.error_message("Error =", err);
                    reject(err);
                }
                else {
                    ontology = result;
                    resolve(ontology);
                }
            });
        }
    });
};

var getCollection =   function(id) {

    return new Promise(function(resolve, reject) {
        getOntology(global_config).then(
            function (result) {
                "use strict";
                console.log("Collection identity = " + id);
                resolve(result.collections[id]);
            },
            function (err) {
                "use strict";
                logging.error_message("Error = ", err);
                reject(err);
            });
    });
};

var getAll = function(id) {
    return new Promise(function (resolve, reject) {
        getCollection(id).then(
            function (result) {
                resolve(result.find());
            },
            function (error) {
                reject(error)
            });
    });
};

var getByQ = function(id, q) {
    return new Promise(function (resolve, reject) {
        getCollection(id).then(
            function (result) {
                resolve(result.find(q));
            },
            function (error) {
                reject(error)
            });
    });
};

var create = function(id, d) {
    return new Promise(function (resolve, reject) {
        getCollection(id).then(
            function (result) {
                resolve(result.create(d));
            },
            function (error) {
                reject(error)
            });
    });
};

var thedao = function(collection) {
    this.collection = collection;
    registerCollection(this.collection);

    this.retrieveById = function(id) {
        s = this.collection.primaryKey;
        return getByQ(this.collection.identity, { [s]: id});
    };

    this.retrieveByTemplate = function(t) {
        s = this.collection.primaryKey;
        return getByQ(this.collection.identity, t);
    }

};

exports.registerCollection = registerCollection;
exports.getCollection = getCollection;
exports.getAll = getAll;
exports.getByQ = getByQ;
exports.create = create;
exports.thedao = thedao;


