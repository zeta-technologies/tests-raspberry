const Ganglion = require('./OBGanglion/index').Ganglion;
const ganglion = new Ganglion();
var origin = 0;
var cpt = 0;
var WebSocketServer = require('ws').Server
  , wss = new WebSocketServer({port: 8080});


ganglion.once('ganglionFound', (peripheral) => {
  ganglion.searchStop();
  wss.on('connection', function(ws) {
      ws.on('message', function(message) {
          console.log('RECEIVED: %s', message);
        });
        ws.send('MESSAGE FROM SERVER');
      ganglion.on('sample', (sample) => {
        // console.log('In ganglion.on');
    /** Work with sample */
        for (let i = 0; i < ganglion.numberOfChannels(); i++) {
          var data = sample.channelData[i].toFixed(8);
          var stringData = data.toString();
          // console.log(stringData);
          ws.send(stringData);
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
