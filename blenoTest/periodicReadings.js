var BNO055 = require('./BNO055');
var async = require('async');
var bno055;
var options = {
    'address': 0x28
}
var options_2 = {
    'address': 0x29
}
bno055_1 = new BNO055(options);
bno055_2 = new BNO055(options_2);


readAll = function() {

  async.series({
  getQuaternion: function(callback) { 
    bno055.getQuaternion(function(err,res) {
      if (err) return callback(err);
      console.log('quaternion: ' + JSON.stringify(res));
      callback(null,res);
  })},
  getAccelerometer: function(callback) { 
    bno055.getAccelerometer(function(err,res) {
      if (err) return callback(err);
      console.log('accelerometer: ' + JSON.stringify(res));
      callback(null,res);
  })},
  getLinearAcceleration: function(callback) { 
    bno055.getLinearAcceleration(function(err,res) {
      if (err) return callback(err);
      console.log('linear acceleration: ' + JSON.stringify(res));
      callback(null,res);
  })},
  getGravity: function(callback) { 
    bno055.getGravity(function(err,res) {
      if (err) return callback(err);
      console.log('gravity: ' + JSON.stringify(res));
      callback(null,res);
  })},
  getGyroscope: function(callback) { 
    bno055.getGyroscope(function(err,res) {
      if (err) return callback(err);
      console.log('gyroscope: ' + JSON.stringify(res));
      callback(null,res);
  })}
  }, function(err,res) {
    if (err)
      throw (err)
    console.log("\n\n");
  });
}

readStatus = function() {

  async.series({

  getCalibrationStatus: function(callback) {
    bno055.getCalibrationStatus(function(err,res) {
      if (err) return callback(err);
      console.log('calibration status: ' + JSON.stringify(res));
      callback(null,res);
  })},
  getSystemStatus: function(callback) {
    bno055.getSystemStatus(function(err,res) {
      if (err) return callback(err);
      console.log('system status: ' + JSON.stringify(res));
      callback(null,res);
  })}
  }, function(err,res) {
    if (err)
      throw (err)
    console.log("\n\n");
  });
}

async.series({
  begin: function(callback) { 
    bno055.beginNDOF(function(err,res) {
      console.log('began successfully? ' + res);
      callback(err, res);
  })},
  setInterval: function(callback) {
    var interval = setInterval(readAll, 500);
    callback(null, interval);
  }}, 
  function(err,res) {
    if (err) throw (err)
    console.log("\n\n");
  }
);
