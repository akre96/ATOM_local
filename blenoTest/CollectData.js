var bleno = require('bleno');
var BNO055 = require('./BNO055');
var os = require('os');
var util = require('util')
var async = require('async');
var BlenoDescriptor = bleno.Descriptor;

var options = {
   'address': 0x28
}

var options_2 = {
   'address': 0x29
}
var bno055_1 = new BNO055(options);
var bno055_2 = new BNO055(options_2);

var Characteristic = bleno.Characteristic;

var CollectData = function() {
    CollectData.super_.call(this, {
        uuid: 'fff6',
        properties: ['write','writeWithoutResponse'],
        descriptors:[
            new BlenoDescriptor({
                uuid: '2901',
                value: 'Begin collecting data from IMUs'
            })
        ]
    });
}


util.inherits(CollectData, Characteristic);

CollectData.prototype.onWriteRequest = function(data,offset, withoutResponse, callback) {
    console.log('onWriteRequest Initiated');
    if (offset) {
        callback(this.RESULT_ATTR_NOT_LONG);
    } else {
        
        var startCollection = data.readUInt8(0);
        
        if (startCollection == 1) {
            console.log("Starting Data Collection")
        } else if (startCollection == 0) {
            console.log("Ending Data Collection")    
        }
    }

    
/*
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
*/   
    callback(this.RESULT_SUCCESS,this._value);
};

module.exports = CollectData;
