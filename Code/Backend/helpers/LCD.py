from .PCF import PCF
from RPi import GPIO
import time

class LCD:

    def __init__(self, rs, e, sda, scl, address):
        self.pcf = PCF(sda, scl, address)
        self.rs = rs
        self.e = e
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([rs,e] , GPIO.OUT)
        # for i in data:
        #     GPIO.setup(i, GPIO.OUT)

    # @property
    # def data(self):
    #     return self._data
    # @data.setter
    # def data(self, value):
    #     self._data = value

    @property
    def rs(self):
        return self._rs
    @rs.setter
    def rs(self, value):
        self._rs = value

    @property
    def e(self):
        return self._e
    @e.setter
    def e(self, value):
        self._e = value

    @property
    def pcf(self):
        """The pcf property."""
        return self._pcf
    @pcf.setter
    def pcf(self, value):
        self._pcf = value

    def send_data_to_pcf(self, value):
        GPIO.output(self.e, 1)
        self.pcf.write_outputs(value)
        GPIO.output(self.e, 0)

    def send_instruction(self, value):
        GPIO.output(self.rs, 0)
        self.send_data_to_pcf(value)

    def send_character(self, value):
        GPIO.output(self.rs, 1)
        self.send_data_to_pcf(value)
    
    def second_row(self):
        self.send_instruction(2)
        for i in range(0, 40):
            self.send_instruction(20)

    def write_message(self, msg):
        print(list(msg))
        if len(msg) > 16:
            for i in range(0, len(msg), 16):
                rij = msg[i:i+16].lstrip(' ')
                print(rij)
                if i == 16:
                    self.second_row()
                for char in list(rij):
                    self.send_character(ord(char))
        else:
            for char in list(msg):
                self.send_character(ord(char))

    def init_LCD(self):
        self.send_instruction(56)
        self.send_instruction(15)
        self.send_instruction(1)

    def clear_LCD(self):
        self.send_instruction(1)