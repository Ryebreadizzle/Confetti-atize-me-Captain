var io = require("socket.io-client");

var sock = io.connect('https://ws.streamjar.tv/', { query: '[insert API key]' });

var serialport = require("serialport");

var onstring = new Buffer("AFFF0101DF", 'hex');

var offstring = new Buffer("AFFF0202DF", 'hex');

var port;

function comNameFunction(cb) {
    serialport.list(function (err, ports) {
	cb(ports[0].comName);
    });
}

function turnOff(){
    port.write(offstring);
    console.log("turned off");
}

function launchConfetti(){
    console.log("Launching confetti!");
    port.write(onstring);
    console.log("turned on");
    setTimeout(turnOff,3000);
}

comNameFunction(function(portname) {
    port = new serialport(portname, function() {

        sock.on('connect', function() {
            console.log('Connected');
        });

        sock.on('donation', function(donation) {
            console.log(donation.name + ' just donated to the stream.');
            console.log(donation);
            if (donation.amount >= 5) {
	        launchConfetti();
            }
        });

        sock.on('subscribe', function(subscription) {
            console.log(subscription.name);
            launchConfetti();
        });
    });
});