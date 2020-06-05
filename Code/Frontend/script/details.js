const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

let html_table;

const listenToUI = function () {
    let logo = document.querySelector(".js-logo")
    logo.addEventListener("click", function() {
        console.log("redirect to homepage");
        window.location.href = window.location.origin;
    });
};


const listenToSocket = function () {
    socket.on("connect", function() {
        console.log("connected to socket");
        socket.emit("F2B_request_data", "temp")
    });

    socket.on("B2F_read_data", function(data) {
        console.log("received data");
        console.log(data);
    });
};



document.addEventListener("DOMContentLoaded", function () {
    console.info("DOM geladen");

    html_table = document.querySelector(".js-table");


    listenToUI();
    listenToSocket();
});