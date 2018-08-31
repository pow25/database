
// jshint node: true

var Waterline = require('waterline');
var dbAdaptor = require('sails-mysql');
var logging = require('/Users/donaldferguson/Dropbox/ColumbiaCourse/Courses/Fall2018/lib/logging');

var waterline = new Waterline();

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


var wdao = function(config, collection, identity) {

    this.config = global_config;
  //  this.config.adapters =   {
      //  'db': dbAdaptor
  //  }
    this.config.adapters = dbAdaptor;
    this.collection = Waterline.Collection.extend(collection);
    this.identity = identity;


    waterline.registerModel(this.collection);

    this.getOntology = function() {
        "use strict";
        var c = this.config;
        return new Promise(function (resolve, reject) {
            var a = c;
            waterline.initialize(global_config, function (err, ontology) {
                if (err) {
                    console.error(err);
                    reject(error);
                }
                else {
                    resolve(ontology);
                }
            });
        });
    };

    this.getCollection =   function() {

        id = this.identity;
        go = this.getOntology();

        return new Promise(function(resolve, reject) {
            go.then(
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

    this.getByQ = function(t) {
        "use strict";

        return this.getCollection().then(
            function(r) {
                return r.find(t)
            });
    };
};

exports.wdao = function(config, collection, id) {
    return new wdao(config, collection, id)
};