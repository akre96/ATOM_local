var bleno = require('bleno');
var os = require('os');
var util = require('util')
var async = require('async');
var fileinput = require('fileinput');
var fs = require ('fs');
var BlenoDescriptor = bleno.Descriptor;
filename="";

var Characteristic = bleno.Characteristic;

var ReadData = function() {
    ReadData.super_.call(this, {
        uuid: 'fff7',
        properties: ['read','notify','write','writeWithoutResponse'],
        descriptors:[
            new BlenoDescriptor({
                uuid: '2901',
                value: 'Stream Specific Session Data'
            })
        ]
        });


    this._value = new Buffer(0);
}


util.inherits(ReadData, Characteristic);

ReadData.prototype.onWriteRequest = function(data,offset, withoutResponse, callback) {
    if(offset){
        callback(this.RESULT_ATTR_NOT_LONG);
    }
    else{
        filename="data/"+data.toString('utf8')+'.txt';
        console.log(filename);
        callback(this.RESULT_SUCCESS,this._value);
    }
}

ReadData.prototype.onSubscribe =  function(maxSize, updateValueCallback){
    console.log('Subscribed');
    if(fs.existsSync(filename)){
        fileinput.input([filename]).on('line', function(line) {
        
           updateValueCallback(line); 
        })
        .on('end', function(){
            console.log('File Sent');
        })
    }

    
}


module.exports = ReadData;
