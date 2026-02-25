import smbus

class MCP4725:
    """Класс для управления 12-битным ЦАП MCP4725 по интерфейсу I2C."""

    def __init__(self, dynamic_range, address=0x61, verbose=True):
        # Инициализируем шину I2C (на Raspberry Pi обычно 1)
        self.bus = smbus.SMBus(1)
        
        self.address = address
        self.wm = 0x00     # Write Mode (00 = Write to DAC Register)
        self.pds = 0x00    # Power Down Select (00 = Normal Mode)
        
        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        """Закрывает работу с шиной I2C."""
        self.bus.close()

    def set_number(self, number):
        """Записывает 12-битное число в микросхему."""
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")
            return

        if not (0 <= number <= 4095):
            print("Число выходит за разрядность MCP4725 (12 бит)")
            return

        # Формируем байты согласно протоколу MCP4725 Fast Mode:
        # 1. Первый байт содержит настройки (4 бита) и 4 старших бита числа
        # 2. Второй байт содержит 8 младших бит числа
        first_byte = (self.wm << 4) | (self.pds << 1) | (number >> 8)
        second_byte = number & 0xFF

        # Передаем данные. SMBus.write_byte_data отправляет: [address, command/first_byte, second_byte]
        self.bus.write_byte_data(self.address, first_byte, second_byte)

        if self.verbose:
            # Выводим адрес в формате записи (сдвиг влево на 1 бит)
            print(f"Число: {number}, отправленные по I2C данные: "
                  f"[0x{(self.address << 1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n")

    def set_voltage(self, voltage):
        """Вычисляет код и выставляет соответствующее напряжение."""
        # Линейная интерпретация: 0 соответствует 0, 4095 соответствует dynamic_range
        # Расчет: code = (V_out * 4095) / V_ref
        number = int((voltage / self.dynamic_range) * 4095)
        
        # Ограничиваем число, чтобы не выйти за пределы 12 бит при расчетах
        number = max(0, min(4095, number))
        
        self.set_number(number)

if __name__ == "__main__":
    # Тестовый запуск: диапазон 5.0В, адрес по умолчанию 0x61
    dac = MCP4725(dynamic_range=5.0)
    
    try:
        target_v = 2.5
        print(f"Установка напряжения: {target_v} В")
        dac.set_voltage(target_v)
    except KeyboardInterrupt:
        print("\nЗавершение работы...")
    finally:
        dac.deinit()
