var bleno = require('bleno');
var BNO055 = require('./BNO055');
var Descriptor = bleno.Descriptor;
var descriptor = new Descriptor({
   uuid: '2901',
   value: 'value' // static value, must be of type Buffer or string if set
});

var Characteristic = bleno.Characteristic;
var Chara = function() {
    Chara.super_.call(this,{
     uuid: 'fff1',
     properties: [ 'read' ],
     value: 'ff', // optional static value, must be of type Buffer
     descriptors: [ descriptor ],
        
    });
}
Chara.prototype.onReadRequest = function(offset, callback) {
        console.log('We got an onReadRequest!');
        callback(Characteristic.RESULT_ATTR_NOT_LONG, null);
        };
var characteristic = new Chara()

var PrimaryService = bleno.PrimaryService;
var primaryService = new PrimaryService({
     uuid: 'fffffffffffffffffffffffffffffff0',
     characteristics: [ characteristic ]
});
var services = [ primaryService ];
bleno.on('advertisingStart', function(error) {
     bleno.setServices( services );
});
bleno.on('stateChange', function(state) {
     console.log('BLE stateChanged to: ' + state);
     if (state === 'poweredOn') {
        bleno.startAdvertising('MyDevice',['fffffffffffffffffffffffffffffff0']);
     } else {
        bleno.stopAdvertising();
     }
});

