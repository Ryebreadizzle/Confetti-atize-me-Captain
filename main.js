var config = require('./config');

var io = require("socket.io-client");

var sock = io.connect('https://ws.streamjar.tv/', {
    query: "key=" + config.apiKey
});

var serialport = require("serialport");

var request = require("request");

var port;

var lastPercent;

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

function checkGoalPercent() {
    request("https://streamjar.tv/api/v1/goals?apikey=" + config.apiKey, function(error, response, body) {
        if (!error && response.statusCode == 200) {
            console.log(body);
            goals = JSON.parse(body);
            goals.forEach(function(goal) {
                if (goal.active) {
                    console.log(goal);
                }
            });
        }
    });
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
            setTimeout(checkGoalPercent, 1000 * (config.motorTime + 1));
        });

        sock.on('subscribe', function(subscription) {
            console.log(subscription.name);
            launchConfetti();
        });
    });
});
