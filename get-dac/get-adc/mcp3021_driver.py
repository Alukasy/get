import smbus 
import time 

class MCP3021:
    def __init__(self, dynamic_range= 5.2, verbose = False):
        self.bus = smbus.SMBus(1)
        self.address = 0x4D 
        self.dynamic_range = dynamic_range
        self.verbose = verbose 
    
    def deinit(self):
        self.bus.close()

    def get_number(self):
        data = self.bus.read_word_data(self.address, 0)

        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF

        number = ((upper_data_byte & 0x0F) << 6 | (lower_data_byte >> 2))

        if self.verbose:
            print(f"Data: {data:04x}, Upper: {upper_data_byte:02x}, Lower: {lower_data_byte:02x}, Num: {number}")
        
        return number 
    
    def get_voltage(self):
        number = self.get_number()
        voltage = (number / 1024) * self.dynamic_range
        return voltage 

if __name__ == "__main__":
    V_ref = 5.2 
    adc = MCP3021(dynamic_range = V_ref, verbose = False) 

    try:
        while True:
            v = adc.get_voltage()
            print(f"Voltage:{v:.3f} V")
            time.sleep(1)
    except KeyboardInterrupt:
        print("STOP")
    finally:
        adc.deinit()