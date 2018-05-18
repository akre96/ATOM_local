var gpio = require('onoff').Gpio

var rLED = new gpio(17,'out');
var gLED = new gpio(27,'out');
var bLED = new gpio(22,'out');

var RGB = {
    "r": rLED,
    "g": gLED,
    "b": bLED
}

changeLED("a");
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
