const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

let html_temp_data, html_hum_data, html_moist_data, html_light_data, html_sol_time,
    html_temp_item_bg, html_temp_data_bg, html_moist_item_bg, html_moist_data_bg;
let mode;

const listenToUI = function () {
    let logo = document.querySelector(".js-logo")
    logo.addEventListener("click", function() {
        console.log("redirect to homepage")
        window.location.href = window.location.origin
    })


    let tile = document.querySelector(".js-temp")
    tile.addEventListener("click", function() {
        console.log("redirect to temperature details")
        window.location.href = `${window.location.origin}/details.html?variable=temperatuur`
    })
    tile = document.querySelector(".js-hum")
    tile.addEventListener("click", function() {
        console.log("redirect to humidity details")
        window.location.href = `${window.location.origin}/details.html?variable=luchtvochtigheid`
    })
    tile = document.querySelector(".js-moist")
    tile.addEventListener("click", function() {
        console.log("redirect to moisture details")
        window.location.href = `${window.location.origin}/details.html?variable=grondvochtigheid`
    })
    tile = document.querySelector(".js-light")
    tile.addEventListener("click", function() {
        console.log("redirect to light details")
        window.location.href = `${window.location.origin}/details.html?variable=licht`
    })
    tile = document.querySelector(".js-sol")
    tile.addEventListener("click", function() {
        console.log("redirect to solenoid details")
        window.location.href = `${window.location.origin}/details.html?variable=water`
    })


    let man = document.querySelector(".js-irrigation-man")
    let auto = document.querySelector(".js-irrigation-auto")
    man.addEventListener("click", function() {
        console.log("manual irrigation activated");
        socket.emit("F2B_irrigation_mode", "man");
    });

    auto.addEventListener("click", function() {
        console.log("automatic irrigation activated");
        socket.emit("F2B_irrigation_mode", "auto");
    });
    
    let button = document.querySelector(".js-apply-water");
    button.addEventListener("click", function () {
        console.log("button pressed");
        socket.emit("F2B_activate_solenoid", 1);
    });
};

const listenToSocket = function() {
    socket.on("B2F_received_measurements", function(data) {
        console.log(data);
        // display data on website
        html_temp_data.innerHTML = data.temp.Status + "°C";
        html_hum_data.innerHTML = data.hum.Status + "%";
        html_moist_data.innerHTML = data.moist.Status + "%";
        html_light_data.innerHTML = data.light.Status + "%";
        html_sol_time.innerHTML = data.sol.DateTime;

        // add warning class modifier if needed
        if(data.temp.Warning != null && html_temp_item_bg.classList.contains("c-data__item--warning") == false) {
            html_temp_item_bg.classList.add("c-data__item--warning");
            html_temp_data_bg.classList.add("c-data__data--warning");
        }
        else if(data.temp.Warning == null && html_temp_item_bg.classList.contains("c-data__item--warning")) {
            html_temp_item_bg.classList.remove("c-data__item--warning");
            html_temp_data_bg.classList.remove("c-data__data--warning");
        };

        if(data.moist.Warning != null && html_moist_item_bg.classList.contains("c-data__item--warning") == false) {
            html_moist_item_bg.classList.add("c-data__item--warning");
            html_moist_data_bg.classList.add("c-data__data--warning");
        }
        else if(data.moist.Warning == null && html_moist_item_bg.classList.contains("c-data__item--warning")) {
            html_moist_item_bg.classList.remove("c-data__item--warning");
            html_moist_data_bg.classList.remove("c-data__data--warning");
        };
    });

    socket.on("B2F_irrigation_mode", function(payload) {
        let man = document.querySelector(".js-irrigation-man")
        let auto = document.querySelector(".js-irrigation-auto")
        if(payload == "man"){
            man.classList.add("c-button--active");
            auto.classList.remove("c-button--active");
            mode = "man";
        }
        else if(payload == "auto"){
            man.classList.remove("c-button--active");
            auto.classList.add("c-button--active");
            mode = "auto";
        };
    });
};

document.addEventListener("DOMContentLoaded", function () {
    console.info("DOM geladen");

    html_temp_data = document.querySelector(".js-temp-data");
    html_hum_data = document.querySelector(".js-hum-data");
    html_moist_data = document.querySelector(".js-moist-data");
    html_light_data = document.querySelector(".js-light-data");
    html_sol_time = document.querySelector(".js-sol-time");
    html_temp_item_bg = document.querySelector(".js-temp-bg1");
    html_temp_data_bg = document.querySelector(".js-temp-bg2");
    html_moist_item_bg = document.querySelector(".js-moist-bg1");
    html_moist_data_bg = document.querySelector(".js-moist-bg2");
    mode = "auto";

    listenToUI();
    listenToSocket();

    setInterval(function() {
        socket.emit('F2B_request_measurements', null);
    }, 120000);
});