import RPi.GPIO as GPIO 

leds = [16,20,21,25,26,17,27,22]
gpio_bits = leds[::-1]
dynamic_range = 3.3

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial = 0)
    
    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    def set_number(number):
        return [int(bit) for bit in bin(int(number))[2:].zfill(8)]
    
    def set_voltage(voltage):
        if not (0.0 <= voltage <= dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)")
            print("Устанавливаем 0.0 В")
            voltage = 0.0

        GPIO.output(self.gpio_bits,set_number(int(voltage / dynamic_range * 255)))

if __name__ == "__main__":
    try:
        dac = R2R_DAC(gpio_bits, 3.183, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз \n")
    
    finally:
        dac.deinit()