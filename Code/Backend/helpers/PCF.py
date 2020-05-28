from RPi import GPIO
import time

class PCF:

    def __init__(self, SDA, SCL, address):
        GPIO.setmode(GPIO.BCM)
        self.SDA = SDA
        self.SCL = SCL
        self.address = address

    @property
    def SDA(self):
        """The SDA property."""
        return self._SDA
    @SDA.setter
    def SDA(self, value):
        GPIO.setup(value, GPIO.OUT)
        self._SDA = value

    @property
    def SCL(self):
        """The SCL property."""
        return self._SCL
    @SCL.setter
    def SCL(self, value):
        GPIO.setup(value, GPIO.OUT)
        self._SCL = value

    @property
    def address(self):
        """The address property."""
        return self._address
    @address.setter
    def address(self, value):
        self._address = value

    def __start_conditie(self):
        GPIO.output(self.SDA, GPIO.HIGH)
        GPIO.output(self.SCL, GPIO.HIGH)

        GPIO.output(self.SDA, GPIO.LOW)
        time.sleep(0.001)
        GPIO.output(self.SCL, GPIO.LOW)

    def __stop_conditie(self):
        GPIO.output(self.SDA, GPIO.LOW)
        GPIO.output(self.SCL, GPIO.LOW)
        
        GPIO.output(self.SCL, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(self.SDA, GPIO.HIGH)

    def __ack(self):
        GPIO.setup(self.SDA, GPIO.IN, GPIO.PUD_UP)
        GPIO.output(self.SCL, GPIO.HIGH)
        GPIO.input(self.SDA)
        GPIO.setup(self.SDA, GPIO.OUT)
        GPIO.output(self.SCL, GPIO.LOW)

    def __writebit(self, bit):
        if bit:
            GPIO.output(self.SDA, GPIO.HIGH)

            GPIO.output(self.SCL, GPIO.HIGH)
            GPIO.output(self.SCL, GPIO.LOW)
        else:
            GPIO.output(self.SDA, GPIO.LOW)

            GPIO.output(self.SCL, GPIO.HIGH)
            GPIO.output(self.SCL, GPIO.LOW)

    def __writebyte(self, byte):
        mask = 0x80
        for i in range(0,8):
            self.__writebit(byte & (mask >> i))

    def write_outputs(self, data:int):
        #start
        self.__start_conditie()
        #address + R/W
        self.__writebyte(self.address)
        #ack
        self.__ack()
        #data
        self.__writebyte(data)
        #ack
        self.__ack()
        #stop
        self.__stop_conditie()