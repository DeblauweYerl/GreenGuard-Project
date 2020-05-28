# pylint: skip-file
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS

import time
import threading

# Code voor sensors en acuators
from helpers.SolenoidValve import SolenoidValve
from helpers.MCP3008 import MCP3008
from helpers.LCD import LCD
from helpers.PCF import PCF
from subprocess import check_output
import Adafruit_DHT
from RPi import GPIO

dht = 18
rs = 5
e = 6
sda = 21
scl = 20

solenoid = SolenoidValve(26)
moist_sensor = MCP3008()
LDR = MCP3008(0,0,1)
DHT_sensor = Adafruit_DHT.DHT11
LCD = LCD(rs, e, sda, scl, 112)

temp = 0
hum = 0
moist = 0
light = 0

GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super geheime code'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

#display ip
def display_ip():
    ips = check_output(['hostname', '--all-ip-addresses'])
    print(ips)
    arr_ips = str(ips).split()
    LCD.init_LCD()
    LCD.write_message(arr_ips[1].replace("'", "").lstrip("b"))

display_ip()

#thread
def read_sensors():
    global temp, hum, moist, light
    while True:
        print("sensors inlezen")
        hum_raw, temp_raw = Adafruit_DHT.read(DHT_sensor, dht)
        if hum_raw is not None and temp_raw is not None:
            temp = round(temp_raw, 0)
            hum = round(hum_raw, 0)
        # res = DataRepository.insert_measurement('HUM', 3, humidity, None)
        # res = DataRepository.insert_measurement('TEMP', 3, temperature, None)
        moist = abs(round(moist_sensor.read_channel() / 1023 * 100, 0) - 100)
        # res = DataRepository.insert_measurement('MOIST', 2, moisture, None)
        light = abs(round(LDR.read_channel() / 1023 * 100, 0) - 100)
        # res = DataRepository.insert_measurement('LIGHT', 1, light, None)
        time.sleep(5)

read_sensors_thread = threading.Thread(target=read_sensors)
read_sensors_thread.start()

# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!
    # vraag de status op van de lampen uit de DB
    # status = DataRepository.read_status_lampen()
    # socketio.emit('B2F_status_lampen', {'lampen': status})

@socketio.on('F2B_request_measurements')
def send_measurements(data):
    global temp, hum, moist, light
    socketio.emit('B2F_received_measurements', {'temp': temp, 'hum': hum, 'moist': moist, 'light': light})

@socketio.on('F2B_activate_solenoid')
def switch_light(data):
    print('Solenoid activated')
    res = DataRepository.insert_measurement('SOLM', 4, 1, None)
    solenoid.apply_water()
    res = DataRepository.insert_measurement('SOLM', 4, 0, None)


# @socketio.on('F2B_activate_solenoid')
# def switch_light(data):
#     print('licht gaat aan/uit')
#     lamp_id = data['lamp_id']
#     new_status = data['new_status']
#     # spreek de hardware aan
#     # stel de status in op de DB
#     res = DataRepository.update_status_lamp(lamp_id, new_status)
#     print(lamp_id)
#     if lamp_id == "2":
#         lees_knop(20)
#     # vraag de (nieuwe) status op van de lamp
#     data = DataRepository.read_status_lamp_by_id(lamp_id)
#     socketio.emit('B2F_verandering_lamp', {'lamp': data})


# def lees_knop(pin):
#     print("button pressed")
#     if GPIO.input(led1) == 1:
#         GPIO.output(led1, GPIO.LOW)
#         res = DataRepository.update_status_lamp("2", "0")
#     else:
#         GPIO.output(led1, GPIO.HIGH)
#         res = DataRepository.update_status_lamp("2", "1")
#     data = DataRepository.read_status_lamp_by_id("2")
#     socketio.emit('B2F_verandering_lamp', {'lamp': data})


# knop1.on_press(lees_knop)


if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
