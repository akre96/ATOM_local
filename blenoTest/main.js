var bleno = require('bleno');
var BNO055 = require('./BNO055')

var PrimaryService = bleno.PrimaryService;
var Orientation = require('./Orientation');
var CollectData = require('./CollectData');

console.log('Bleno – Orientation');

bleno.on('stateChange', function(state) {
    console.log('on -> stateChange: '+ state);

    if (state === 'poweredOn' ) {
        bleno.startAdvertising('CollectData', ['fff6']);
    }
    else {
        bleno.stopAdvertising();
    }
});

bleno.on('advertisingStart', function(error) {
    console.log('on -> advertisingStart: ' + (error ? 'error ' + error : 'success' ));

    if (!error) {
        bleno.setServices([
            new PrimaryService({
                uuid: 'fff6',
                characteristics: [ new CollectData() ]
                })
            ]);
        }
});
