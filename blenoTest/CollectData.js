var bleno = require('bleno');
var BNO055 = require('./BNO055');
var os = require('os');
var util = require('util')
var async = require('async');
var fs = require('fs');
var BlenoDescriptor = bleno.Descriptor;
var gpio = require('onoff').Gpio

var rLED = new gpio(17,'out');
var gLED = new gpio(27,'out');
var bLED = new gpio(22,'out');

var RGB = {
    "r": rLED,
    "g": gLED,
    "b": bLED
}

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
    this._streaming = null;
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
        
        var startCollection = data.toString('utf8');
        if(startCollection != "0"){
            var filename = startCollection + ".txt";
            var header = ["qw1","qx1","qy1","qz1","ax1","ay1","az1","lax1","lay1","laz1","grx1","gry1","grz1","gyrx1","gyry1","gyrz1","qw2","qx2","qy2","qz2","ax2","ay2","az2","lax2","lay2","laz2","grx2","gry2","grz2","gyrx2","gyry2","gyrz2"]
            var newfile = true;
            if(fs.existsSync(filename)){
                newfile = false;
            }
            
            var dataStream = fs.createWriteStream(filename, {'flags':'a+'});

            dataStream.on('open', function(){
            
                    if(newfile) {
                        console.log("Writing to New File");
                        dataStream.write(header.join(', ')+'\n');
                    }

                    if (startCollection == 0) {
                        console.log('Ending Data Collection');
                    }
                    else {
                        async.series(InitOperations, function(err, results) {
                            if(err){
                                console.log(err);
                                changeColor("r");
                                callback(this.RESULT_UNLIKELY_ERROR);
                            }
                        
                            console.log("Starting Data Collection");
                            changeColor("g");
                            
                            this._streaming = setInterval( function(){
                            
                                async.series(ReadOperations, function(err, results) {
                                    if(err)
                                    {
                                        console.log(err);
                                        changeColor("r");
                                    }
                                    else
                                    {
                                        changeColor("g");
                                        var formatData = formatBNOData(results);
                                        dataStream.write(formatData.join(', ')+'\n');
                                    }
                                });

                            },100);
                            });
                        }
                });
            }
            else{
                console.log("ending data stream");
                clearInterval(this._streaming);
                changeColor("b");
            }
        }

    
    callback(this.RESULT_SUCCESS,this._value);
};


// Turn output of BNO055s to usable form
function formatBNOData(data) {
    var header = ["qw1","qx1","qy1","qz1","ax1","ay1","az1","lax1","lay1","laz1","grx1","gry1","grz1","gyrx1","gyry1","gyrz1","qw2","qx2","qy2","qz2","ax2","ay2","az2","lax2","lay2","laz2","grx2","gry2","grz2","gyrx2","gyry2","gyrz2"]
    var q1=data[0];
    var a1=data[1];
    var la1=data[2];
    var gr1=data[3];
    var gyr1=data[4];
    var q2=data[5];
    var a2=data[6];
    var la2=data[7];
    var gr2=data[8];
    var gyr2=data[9];
    output=[q1.w,q1.x,q1.y,q1.z,a1.x,a1.y,a1.z,la1.x,la1.y,la1.z,gr1.x,gr1.y,gr1.z,gyr1.x,gyr1.y,gyr1.z,q2.w,q2.x,q2.y,q2.z,a2.x,a2.y,a2.z,la2.x,la2.y,la2.z,gr2.x,gr2.y,gr2.z,gyr2.x,gyr2.y,gyr2.z];
    return output
}

// Functions to initialize the BNO055

function initBNO_1(callback) {
    bno055_1.beginNDOF(function(err,res) {
        console.log('bno1 began succesffuly? ' + res)
        callback(err,res);
    });
};
function initBNO_2(callback) {
    bno055_2.beginNDOF(function(err,res) {
        console.log('bno2 began succesffuly? ' + res)
        callback(err,res);
    });
};

// Functions to read data from BNO055 1 and 2
function getQuaternion_1(callback) { 
    bno055_1.getQuaternion(function(err,res) {
      if (err) return callback(err);
      callback(null,res);
  })};
function getAccelerometer_1(callback) { 
    bno055_1.getAccelerometer(function(err,res) {
      if (err) return callback(err);
      callback(null,res);
  })};

function getLinearAcceleration_1(callback) { 
    bno055_1.getLinearAcceleration(function(err,res) {
      if (err) return callback(err);
      callback(null,res);
  })};

function getGravity_1(callback) { 
    bno055_1.getGravity(function(err,res) {
      if (err) return callback(err);
      callback(null,res);
  })};

function getGyroscope_1(callback) { 
    bno055_1.getGyroscope(function(err,res) {
      if (err) {
        console.log(err);
        return callback(err)
        };
      callback(null,res);
  })};

function getQuaternion_2(callback) { 
    bno055_2.getQuaternion(function(err,res) {
      if (err) return callback(err);
      callback(null,res);
  })};
function getAccelerometer_2(callback) { 
    bno055_2.getAccelerometer(function(err,res) {
      if (err) return callback(err);
      callback(null,res);
  })};

function getLinearAcceleration_2(callback) { 
    bno055_2.getLinearAcceleration(function(err,res) {
      if (err) return callback(err);
      callback(null,res);
  })};

function getGravity_2(callback) { 
    bno055_2.getGravity(function(err,res) {
      if (err) return callback(err);
      callback(null,res);
  })};

function getGyroscope_2(callback) { 
    bno055_2.getGyroscope(function(err,res) {
      if (err) return callback(err);
      callback(null,res);
  })};


function changeColor(color){

   for (led in RGB) {
        if (RGB[led].readSync() === 0){
            if (color == led){
                RGB[led].writeSync(1);
            }
        }
        else{
            RGB[led].writeSync(0);
        }
   }
}

module.exports = CollectData;
