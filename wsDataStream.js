
const WebSocket = require('ws');
const Ganglion = require('./OBGanglion/index').Ganglion;
const ganglion = new Ganglion();
var origin = 0;
var cpt = 0;
var start = new Date().getTime();
var WebSocketServer = require('websocket').server;
const ws = new WebSocket('ws://127.0.0.1:8080');

ganglion.once('ganglionFound', (peripheral) => {
  // Stop searching for BLE devices once a ganglion is found.
  ganglion.searchStop();

  ganglion.on('sample', (sample) => {
    /** Work with sample */
    // console.log(sample.sampleNumber);
    ws.on('open', function(){
      for (let i = 0; i < ganglion.numberOfChannels(); i++) {
        ws.send('sample.channelData[i].toFixed(8)');
      }
    });
  });
  ganglion.once('ready', () => {
    ganglion.streamStart();
  });
  ganglion.connect(peripheral);
});
// Start scanning for BLE devices
ganglion.searchStart();
