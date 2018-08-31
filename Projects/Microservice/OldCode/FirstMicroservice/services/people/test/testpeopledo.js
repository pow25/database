/**
 * Created by donaldferguson on 8/15/18.
 */

var peopledo = require('../dos/peopledo')
var logging = require('/Users/donaldferguson/Dropbox/ColumbiaCourse/Courses/Fall2018/lib/logging');

p.getByQ({"last_name": "Williams"}).then(
    function(d) {
        "use strict";
        logging.debug_message("D = ", d);
        config.adapters.db.teardown(null,
            function(error, message) {
                logging.debug_message("Teardown said ...", message);
            });
    }
);

peopledo.getByQ({"last_name": "Williams"}).then(
    function(d) {
        "use strict";
        logging.debug_message("D = ", d);
        config.adapters.db.teardown(null,
            function(error, message) {
                logging.debug_message("Teardown said ...", message);
            });
    }
);


/*
 getAssetCollection().then(getAll).then(
 console.log
 ).
 catch(function(err) {
 logging.debug_message("Boom", err);
 });
 */

/*
 var getAllAssets = function() {
 return getAssetCollection().then(
 function (r) {
 "use strict";
 //console.log("r = ", r);
 return r.find()
 });
 };

 getAllAssets()
 .then(
 function(r2) {
 console.log(r2);
 }
 ).catch(function(err) {
 logging.debug_message("Boom", err);
 });*/








/*
 // Tease out fully initialized models.
 var asset = ontology.collections.asset_types;


 // Since we're using `await`, we'll scope our selves an async IIFE:
 (async ()=>{
 // First we create a user
 var nasset = await asset.create({
 assetTypeId: 'foo',
 assetSubtypeId: 'bar',
 assetTypeDescription: 'cat'
 });
 })()
 .then(()=>{
 // All done.
 })
 .catch((err)=>{
 console.error(err);
 });


 });
 */


