import spidev

class MCP:

    def __init__(self, bus=0, device=0):
        self.bus = bus
        self.device = device
        self.spi = self.spi_maken()

    @property
    def bus(self):
        """The bus property."""
        return self._bus
    @bus.setter
    def bus(self, value):
        self._bus = value
    
    @property
    def device(self):
        """The device property."""
        return self._device
    @device.setter
    def device(self, value):
        self._device = value

    @property
    def spi(self):
        """The spi property."""
        return self._spi
    @spi.setter
    def spi(self, value):
        self._spi = value

    def spi_maken(self):
        spi = spidev.SpiDev()
        spi.open(self.bus, self.device)              # Bus SPI0, slave op CE 0
        spi.max_speed_hz = 10 ** 5  # 100 kHz
        return spi

    def read_channel(self, channel):
        bytes_out = [1, (8+channel)<<4, 0]
        bytes_in = self.spi.xfer2(bytes_out)
        output = ((bytes_in[1] << 8) + bytes_in[2])
        return round(output / 1023 * 100,2)