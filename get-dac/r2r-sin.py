import r2r_dac as r2r 
import RPi.GPIO as GPIO
import signal_generator as sg 
import time 

amplitude = 3.2 
signal_frequency = 10 
sampling_frequency = 1000 

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

    def set_number(self, number):
        return [int(bit) for bit in bin(int(number))[2:].zfill(8)]
    
    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} В)")
            print("Устанавливаем 0.0 В")
            voltage = 0.0

        digital_value = int((voltage / self.dynamic_range)* 255)
        bit_list = self.set_number(digital_value)
        print(digital_value, bit_list)

        GPIO.output(self.gpio_bits, bit_list)
dynamic_range = 3.3
dac = r2r.R2R_DAC([16,20,21,25,26,17,27,22], dynamic_range)
try:
    print(f"Частота:{signal_frequency}Hz, Амплитуда:{amplitude}V")

    start_time = time.time()

    while True:
        current_time = time.time() - start_time 

        norm_amp = sg.get_sin_wave_amplitude(signal_frequency, current_time)
        target_voltage = norm_amp * amplitude
        dac.set_voltage(target_voltage)
        sg.wait_for_sampling_period(sampling_frequency)
except KeyboardInterrupt:
    print("Остановлено")
finally:
    dac.deinit()
    print("Чистка GPIO выполнена")