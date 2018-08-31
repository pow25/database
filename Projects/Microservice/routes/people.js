var express = require('express');
var router = express.Router();

var peoplebo = require('../services/bos/peoplebo');
var logging = require('../lib/logging');
var routerutils = require('./routerutils');

/* GET home page. */
router.get('/', function(req, res, next) {

    var q = req.query;
    logging.debug_message("Query = ", q);
    var template = routerutils.queryParamsToTemplate(q);
    logging.debug_message("Template = ", template);

    peoplebo.findByTemplate(template).then(
        function(result) {
            if (result == null) {
                res.status(404).send("Not found");
            }
            else {
                res.status(200).json(result);
            }
        },
        function(error) {
            res.status(500).send("Internal error.");
        }
    );
});

router.get('/:id', function(req, res, next) {
    peoplebo.findByPrimaryKey(req.params.id).then(
        function(result) {
            if (result == null) {
                res.status(404).send("Not found");
            }
            else {
                res.status(200).json(result);
            }
        },
        function(error) {
            res.status(500).send("Internal error.");
        }
    );
});

router.post('/', function(req, res, next) {
    logging.debug_message("Body = ", req.body);
    res.status(501).send("Not implemented.");
});

router.delete('/:id', function(req, res, next) {
    res.status(501).send("Not implemented.");
});

router.put('/:id', function(req, res, next) {
    res.status(501).send("Not implemented.");
});

module.exports = router;
