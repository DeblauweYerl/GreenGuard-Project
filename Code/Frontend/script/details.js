const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

let html_table, variable;


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
        socket.emit("F2B_request_data", variable)
    });

    socket.on("B2F_read_data", function(data) {
        console.log("received data");
        console.log(data);

        let counter = 0;
        let graphdata = [];
        while(counter < 40) {
            graphdata.push(data[counter]);
            counter ++;
        };

        let dates = [];
        let measurements = [];
        let maxMeasurement = 0;
        let minMeasurement = 100;
        for(item of graphdata.reverse()){
            dates.push(item.DateTime);
            measurements.push(item.Status);
            if(item.Status > maxMeasurement){
                maxMeasurement = item.Status;
            }
            if(item.Status < minMeasurement){
                minMeasurement = item.Status;
            }
        };
        console.log(dates);
        console.log(measurements);
    
    
        var canvas = document.querySelector("#Graph");
        var graph = new Chart(canvas, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    // label: variable,
                    data: measurements,
                    backgroundColor: 'rgba(255, 255, 255, 0)',
                    pointBackgroundColor: 'rgba(77, 128, 0, 1)',
                    borderColor: 'rgba(77, 128, 0, 1)',
                }]
            },
            options: {
                legend: {
                    display: false
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            suggestedMin: minMeasurement-1,
                            suggestedMax: maxMeasurement+1,
                            precision: 0
                        }
                    }],
                    xAxes: [{
                        ticks: {
                            display: false
                        }
                    }]
                }
            }
        });
        console.log(`max: ${maxMeasurement}`)
        console.log(`min: ${minMeasurement}`)


        let rows = "";
        for(record of data) {
            rows += `   <div class="c-cell u-1-of-2 js-table-date">${record.DateTime}</div>
                        <div class="c-cell u-1-of-2 js-table-status">${record.Status}</div>`;
        }
        html_table.innerHTML = rows;
    });
};



document.addEventListener("DOMContentLoaded", function () {
    console.info("DOM geladen");

    html_table = document.querySelector(".js-table");


    listenToUI();
    listenToSocket();

    const urlParams = new URLSearchParams(window.location.search);
    variable = urlParams.get('variable');
    console.log(variable);

    let title = document.querySelector(".js-title");
    title.innerHTML = variable;

    setInterval(function() {
        socket.emit('F2B_request_data', variable);
    }, 120000);
});