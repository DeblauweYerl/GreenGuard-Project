const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

let html_temp, html_hum, html_moist, html_light;

const listenToUI = function () {
    const button = document.querySelector(".js-apply-water");
    button.addEventListener("click", function () {
        console.log("button pressed");
        socket.emit("F2B_activate_solenoid", 1);
    });
};

const listenToSocket = function() {
    socket.on("B2F_received_measurements", function(data) {
        html_temp.innerHTML = data.temp + "°C"
        html_hum.innerHTML = data.hum + "%"
        html_moist.innerHTML = data.moist + "%"
        html_light.innerHTML = data.light + "%"
    });
}

document.addEventListener("DOMContentLoaded", function () {
    console.info("DOM geladen");

    html_temp = document.querySelector(".js-temp");
    html_hum = document.querySelector(".js-hum");
    html_moist = document.querySelector(".js-moist");
    html_light = document.querySelector(".js-light");

    listenToUI();
    listenToSocket();

    setInterval(function() {
        socket.emit('F2B_request_measurements', null);
    }, 5000);
});