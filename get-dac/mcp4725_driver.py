import smbus

class MCP4725:

    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)
        
        self.address = address
        self.wm = 0x00     
        self.pds = 0x00    
        
        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        self.bus.close()

    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")
            return

        if not (0 <= number <= 4095):
            print("Число выходит за разрядность MCP4725 (12 бит)")
            return

        first_byte = (self.wm << 4) | (self.pds << 1) | (number >> 8)
        second_byte = number & 0xFF

        self.bus.write_byte_data(self.address, first_byte, second_byte)

        if self.verbose:
            print(f"Число: {number}, отправленные по I2C данные: "
                  f"[0x{(self.address << 1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n")

    def set_voltage(self, voltage):
        if voltage >= 5:
            voltage = 0
        number = int((voltage / self.dynamic_range) * 4095)
        
        number = max(0, min(4095, number))
        
        self.set_number(number)

if __name__ == "__main__":
    dac = MCP4725(dynamic_range=5.0)
    while True:
        try:
            target_v = float(input("Введите желаемое напряжение:\n"))
            print(f"Установка напряжения: {target_v} В")
            dac.set_voltage(target_v)
        except KeyboardInterrupt:
            print("\nЗавершение работы...")
        finally:
            dac.deinit()