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

var ReadOperations=[];
var InitOperations=[];

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

InitOperations.push(initBNO_1);
InitOperations.push(initBNO_2);

ReadOperations.push(getQuaternion_1);
ReadOperations.push(getAccelerometer_1);
ReadOperations.push(getLinearAcceleration_1);
ReadOperations.push(getGravity_1);
ReadOperations.push(getGyroscope_1);
ReadOperations.push(getQuaternion_2);
ReadOperations.push(getAccelerometer_2);
ReadOperations.push(getLinearAcceleration_2);
ReadOperations.push(getGravity_2);
ReadOperations.push(getGyroscope_2);

util.inherits(CollectData, Characteristic);

CollectData.prototype.onWriteRequest = function(data,offset, withoutResponse, callback) {
    console.log('onWriteRequest Initiated');
    if (offset) {
        callback(this.RESULT_ATTR_NOT_LONG);
    } else {
        
        var startCollection = data.readUInt8(0);
        
        if (startCollection == 1) {
            async.series(InitOperations, function(err, results) {
            
                console.log("Starting Data Collection")
                
                async.series(ReadOperations, function(err, results) {
                    console.log(results); 
                });
            });
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

function initBNO_1(callback) {
    bno055_1.beginNDOF(function(err,res) {
        console.log('bno1 began succesffuly? ' + res)
        callback(err,res);
}
function initBNO_2(callback) {
    bno055_2.beginNDOF(function(err,res) {
        console.log('bno2 began succesffuly? ' + res)
        callback(err,res);
}

function getQuaternion_1(callback) { 
    bno055_1.getQuaternion(function(err,res) {
      if (err) return callback(err);
      console.log('quaternion: ' + JSON.stringify(res));
      callback(null,res);
  })};
function getAccelerometer_1(callback) { 
    bno055_1.getAccelerometer(function(err,res) {
      if (err) return callback(err);
      console.log('accelerometer: ' + JSON.stringify(res));
      callback(null,res);
  })};

function getLinearAcceleration_1(callback) { 
    bno055_1.getLinearAcceleration(function(err,res) {
      if (err) return callback(err);
      console.log('linear acceleration: ' + JSON.stringify(res));
      callback(null,res);
  })};

function getGravity_1(callback) { 
    bno055_1.getGravity(function(err,res) {
      if (err) return callback(err);
      console.log('gravity: ' + JSON.stringify(res));
      callback(null,res);
  })};

function getGyroscope_1(callback) { 
    bno055_1.getGyroscope(function(err,res) {
      if (err) {
        console.log(err);
        return callback(err)
        };
      console.log('gyroscope2: ' + JSON.stringify(res));
      callback(null,res);
  })};

function getQuaternion_2(callback) { 
    bno055_2.getQuaternion(function(err,res) {
      if (err) return callback(err);
      console.log('quaternion2: ' + JSON.stringify(res));
      callback(null,res);
  })};
function getAccelerometer_2(callback) { 
    bno055_2.getAccelerometer(function(err,res) {
      if (err) return callback(err);
      console.log('accelerometer2: ' + JSON.stringify(res));
      callback(null,res);
  })};

function getLinearAcceleration_2(callback) { 
    bno055_2.getLinearAcceleration(function(err,res) {
      if (err) return callback(err);
      console.log('linear acceleration2: ' + JSON.stringify(res));
      callback(null,res);
  })};

function getGravity_2(callback) { 
    bno055_2.getGravity(function(err,res) {
      if (err) return callback(err);
      console.log('gravity2: ' + JSON.stringify(res));
      callback(null,res);
  })};

function getGyroscope_2(callback) { 
    bno055_2.getGyroscope(function(err,res) {
      if (err) return callback(err);
      console.log('gyroscope2: ' + JSON.stringify(res));
      callback(null,res);
  })};


module.exports = CollectData;
