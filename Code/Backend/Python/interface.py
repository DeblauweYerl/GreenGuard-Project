from model.MCP import MCP
from subprocess import check_output
from model.LCD import LCD
from RPi import GPIO
import time
import datetime
import serial

# status_display = 0

# joystick_btn = 4
# tijd_btn = 5
sda = 21
scl = 20
rs = 5
e = 6
# tx = 16
# rgb = [22,27,17]


GPIO.setmode(GPIO.BCM)
# GPIO.setup(joystick_btn, GPIO.IN, GPIO.PUD_UP)
# GPIO.setup(tx, GPIO.OUT)
# for color in rgb:
#     GPIO.setup(color, GPIO.OUT)

# MCP = MCP()
LCD = LCD(rs, e, sda, scl, 112)
# ser = serial.Serial('/dev/serial0')

# pwm_red = GPIO.PWM(rgb[0], 50)
# pwm_green = GPIO.PWM(rgb[1], 50)
# pwm_blue = GPIO.PWM(rgb[2], 50)
# pwm_red.start(3)
# pwm_green.start(3)
# pwm_blue.start(3)

# def display_joystick(joystick_as):
#     LCD.init_LCD()
#     for i in range(0, int(round(joystick_as/6.25,0))):
#         LCD.send_character(219)
#     LCD.second_row()
#     if status_display == 1:
#         LCD.write_message(f"VRX => {round(joystick_as,2)}")
#     elif status_display == 2:
#         LCD.write_message(f"VRY => {round(joystick_as,2)}")

def display_ips():
    ips = check_output(['hostname', '--all-ip-addresses'])
    arr_ips = str(ips).split()
    LCD.init_LCD()
    LCD.write_message(arr_ips[0].replace("'", "").lstrip("b"))
    LCD.second_row()
    LCD.write_message(arr_ips[1])


# def change_status(knop):
#     global status_display
#     LCD.init_LCD()
#     print("op de knop gedrukt")
#     if status_display == 0:
#         status_display += 1
#     elif status_display == 1:
#         status_display += 1
#     else:
#         status_display = 0
#         display_ips()

# def send_time(seconds=False):
#     tijd = str(datetime.datetime.now().time()).replace(':', '')
#     tijd = tijd[0:4]
#     print(tijd)

#     ser.write(tijd.encode())

# GPIO.add_event_detect(joystick_btn, GPIO.RISING, change_status, bouncetime=200)

try:
    display_ips()
    # while True:
    #     print(f"status display: {status_display}")
    #     joystick_x = MCP.read_channel(0)
    #     joystick_y = MCP.read_channel(1)
    #     pwm_red.ChangeDutyCycle(joystick_y)
    #     pwm_green.ChangeDutyCycle(joystick_x)
    #     pwm_blue.ChangeDutyCycle((joystick_x + joystick_y) / 2)

    #     send_time()

    #     if status_display == 1:
    #         display_joystick(joystick_x)

    #     elif status_display == 2:
    #         display_joystick(joystick_y)

    #     time.sleep(0.5)

except KeyboardInterrupt as ki:
    print(ki)

# finally:
    # LCD.clear_LCD()
    # GPIO.cleanup()
    # ser.close()