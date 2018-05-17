var bleno = require('bleno');
var BNO055 = require('./BNO055');
var os = require('os');
var util = require('util')
var async = require('async');

var options = {
   'address': 0x28
}

var options_2 = {
   'address': 0x29
}
var bno055_1 = new BNO055(options);
var bno055_2 = new BNO055(options_2);

var Characteristic = bleno.Characteristic;

var Orientation = function() {
    Orientation.super_.call(this, {
        uuid: 'fff6',
        properties: ['read','notify'],
        onNotify:  function(){
            console.log('notify');
           }
        });


    this._value = new Buffer(0);
}


util.inherits(Orientation, Characteristic);

Orientation.prototype.onSubscribe =  function(maxSize, updateValueCallback){
    console.log('Subscribed');
    
    bno055_1.beginNDOF(function(err,res) {
        console.log(err)
        console.log('bno1 began succesffuly? ' + res)

        setInterval(function() {
        
            bno055_1.getLinearAcceleration(function(err,res) {
                console.log(JSON.stringify(res));
                var data = Buffer.from(JSON.stringify(res));
                updateValueCallback(data);
            });
         }, 10);
    });
    bno055_2.beginNDOF(function(err,res) {
        console.log('bno1 began succesffuly? ' + res)
    });

}
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
