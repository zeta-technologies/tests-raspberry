const Ganglion = require('./OBGanglion/index').Ganglion;
const ganglion = new Ganglion();
var origin = 0;
var cpt = 0;
var start = new Date();

ganglion.once('ganglionFound', (peripheral) => {
  // Stop searching for BLE devices once a ganglion is found.
  ganglion.searchStop();
  ganglion.on('sample', (sample) => {
    /** Work with sample */
    // console.log(sample.sampleNumber);
    var time = new Date();
    console.log(time.getSeconds())
    // console.log(sample.channelData[0].toFixed(8), sample.channelData[1].toFixed(8), sample.channelData[2].toFixed(8), sample.channelData[3].toFixed(8)); //+ " Volts.");
    console.log(sample.channelData)
  });
  ganglion.once('ready', () => {
    ganglion.streamStart();
  });
  ganglion.connect(peripheral);
});
// Start scanning for BLE devices
ganglion.searchStart();
