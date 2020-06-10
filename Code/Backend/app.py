# pylint: skip-file
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS

import time
import datetime
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
water_applied = 0
irrigation_mode = "auto"

GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super geheime code'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

#display ip
def display_ip():
    ips = check_output(['hostname', '--all-ip-addresses'])
    arr_ips = str(ips).split()
    LCD.init_LCD()
    LCD.write_message(arr_ips[1].replace("'", "").lstrip("b"))

display_ip()


def sensordata():
    sol = DataRepository.read_latest_solenoid()
    sol['DateTime'] = str(sol['DateTime'])[11:16]
    data = {
        'temp': DataRepository.read_latest_temperature(),
        'hum': DataRepository.read_latest_humidity(),
        'moist': DataRepository.read_latest_moisture(),
        'light': DataRepository.read_latest_light(),
        'sol': sol
    }
    return data


#thread
def read_sensors():
    global temp, hum, moist, light, water_applied, irrigation_mode
    while True:
        print("sensors inlezen")
        hum_raw, temp_raw = Adafruit_DHT.read(DHT_sensor, dht)
        if hum_raw is not None and temp_raw is not None:
            temp = round(temp_raw, 0)
            hum = round(hum_raw, 0)

        moist = abs(round((moist_sensor.read_channel()-350) / 673 * 100, 0) - 100)

        light = abs(round(LDR.read_channel() / 1023 * 100, 0) - 100)

        insert_sensordata()
        
        if irrigation_mode == "auto":
            if moist < 35:
                res = DataRepository.insert_measurement('SOLA', 4, 1, None)
                solenoid.apply_water()
                res = DataRepository.insert_measurement('SOLA', 4, 0, None)
                water_applied = 1
            else:
                water_applied = 0

        check_warnings()
        
        time.sleep(120)

def insert_sensordata():
    global temp, hum, moist, light
    if temp > 30 and light > 95:
        res = DataRepository.insert_measurement('TEMP', 3, temp, 'HOT')
    elif temp < 16 and light < 50:
        res = DataRepository.insert_measurement('TEMP', 3, temp, 'COLD')
    else:
        res = DataRepository.insert_measurement('TEMP', 3, temp, None)

    #humidity
    res = DataRepository.insert_measurement('HUM', 3, hum, None)

    #moisture
    if DataRepository.read_latest_moisture()['Status'] < 35 and water_applied == 1:
        res = DataRepository.insert_measurement('MOIST', 2, moist, 'WATER')
    else:
        res = DataRepository.insert_measurement('MOIST', 2, moist, None)

    res = DataRepository.insert_measurement('LIGHT', 1, light, None)

def check_warnings():
    data = sensordata()

    if data['temp']['Warning'] is not None:
        LCD.init_LCD()
        LCD.write_message("Waarschuwing:")
        LCD.second_row()
        LCD.write_message(data['temp']['Warning'])

    elif data['moist']['Warning'] is not None:
        LCD.init_LCD()
        LCD.write_message("Waarschuwing:")
        LCD.second_row()
        LCD.write_message(data['moist']['Warning'])
    
    else:
        display_ip()

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
    send_measurements(1)
    socketio.emit('B2F_irrigation_mode', irrigation_mode)

@socketio.on('F2B_request_measurements')
def send_measurements(payload):
    data = sensordata()
    socketio.emit('B2F_received_measurements', data)
    
    if data['temp']['Warning'] is not None:
        socketio.emit('B2F_warning', data['temp']['Warning'])

    elif data['moist']['Warning'] is not None:
        socketio.emit('B2F_warning', data['moist']['Warning'])

@socketio.on('F2B_request_data')
def send_data(payload):
    if payload == 'temperatuur':
        data = DataRepository.read_temperature()
        for i in data:
            i['DateTime'] = str(i['DateTime'])
        socketio.emit('B2F_read_data', data)
    if payload == 'luchtvochtigheid':
        data = DataRepository.read_humidity()
        for i in data:
            i['DateTime'] = str(i['DateTime'])
        socketio.emit('B2F_read_data', data)
    if payload == 'grondvochtigheid':
        data = DataRepository.read_moisture()
        for i in data:
            i['DateTime'] = str(i['DateTime'])
        socketio.emit('B2F_read_data', data)
    if payload == 'licht':
        data = DataRepository.read_light()
        for i in data:
            i['DateTime'] = str(i['DateTime'])
        socketio.emit('B2F_read_data', data)
    if payload == 'water':
        data = DataRepository.read_solenoid()
        for i in data:
            i['DateTime'] = str(i['DateTime'])
        socketio.emit('B2F_read_data', data)


@socketio.on('F2B_activate_solenoid')
def activate_solenoid(data):
    global irrigation_mode
    print('Solenoid activated')
    if irrigation_mode == "man":
        res = DataRepository.insert_measurement('SOLM', 4, 1, None)
        solenoid.apply_water()
        res = DataRepository.insert_measurement('SOLM', 4, 0, None)

@socketio.on('F2B_irrigation_mode')
def switch_irrigation_mode(data):
    global irrigation_mode
    irrigation_mode = data
    socketio.emit('B2F_irrigation_mode', irrigation_mode)


if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
