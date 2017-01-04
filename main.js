var config = require('./config');

var io = require("socket.io-client");

var sock = io.connect('https://ws.streamjar.tv/', {
    query: "key=" + config.apiKey
});

var serialport = require("serialport");

var port;

function getComName(cb) {
    serialport.list(function(err, ports) {
        cb(ports[0].comName);
    });
}

function launchConfetti() {
    console.log("Launching confetti!");
    port.write(Buffer("AFFF0101DF", 'hex'));
    console.log("turned on");
    setTimeout(function() {
        port.write(Buffer("AFFF0202DF", 'hex'));
        console.log("turned off");
    }, config.motorTime * 1000);
}

getComName(function(portname) {
    port = new serialport(portname, function() {

        sock.on('connect', function() {
            console.log('Connected');
        });

        sock.on('donation', function(donation) {
            console.log(donation.name + ' just donated to the stream.');
            console.log(donation);
            if (donation.amount >= config.minimumDonation) {
                launchConfetti();
            }
        });

        sock.on('subscribe', function(subscription) {
            console.log(subscription.name);
            launchConfetti();
        });
    });
});
