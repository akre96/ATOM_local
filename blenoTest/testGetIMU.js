//var i2c = require('i2c');
//var BNO055 = require('./BNO055');
var os = require('os');
var util = require('util')
var async = require('async');
var operations = [];
var options = {
   'address': 0x28
}

var options_2 = {
   'address': 0x29
}
//var bno055_1 = new BNO055(options);
//var bno055_2 = new BNO055(options_2);

function first(callback){
    callback(null,'first');
}

function two(callback){
    callback(null,'second');
}

operations.push(first)
operations.push(two)

async.series(operations, function(err,results) {
    console.log(results);
});
/*
Orientation.prototype.onReadRequest = function(offset, callback) {
    console.log('onReadRequest Initiated');
    bno055_1.beginNDOF(function(err,res) {
        console.log('bno1 began succesffuly? ' + res)
        callback(err,res);
    });
    bno055_2.beginNDOF(function(err,res) {
        console.log('bno1 began succesffuly? ' + res)
        callback(err,res);
    });

    bno055_1.getQuaternion(function(err,res) {
        if (err) return callback(err);
        console.log('getting Quat');
        console.log(JSON.stringify(res));
        this._value = JSON.stringify(res);
    });
    
    callback(this.RESULT_SUCCESS,this._value);
};

module.exports = Orientation;
*/
