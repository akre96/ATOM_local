var bleno = require('bleno');
var BNO055 = require('./BNO055');
var gpio = require('onoff').Gpio;

var rLED = new gpio(17,'out');
var gLED = new gpio(27,'out');
var bLED = new gpio(22,'out');

var RGB = {
    "r": rLED,
    "g": gLED,
    "b": bLED
}

var PrimaryService = bleno.PrimaryService;
var CollectData = require('./CollectData');

console.log('Bleno – Collect IMU Data');

bleno.on('stateChange', function(state) {
    console.log('on -> stateChange: '+ state);

    if (state === 'poweredOn' ) {
        bleno.startAdvertising('CollectData', ['fff6']);
        changeLED("b");
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

function changeLED(color){

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
