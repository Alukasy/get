import pwm_dac as pwm
import RPi.GPIO as GPIO
import signal_generator as sg 
import time 

amplitude = 3.0
signal_frequency = 10 / 2
sampling_frequency = 1000 / 2 

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose = False):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0)

    def deinit(self):
        self.pwm.stop()
        GPIO.cleanup()
    
    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} В)")
            print("Устанавливаем 0.0 В")
            voltage = 0.0

        duty_cycle = (voltage/ self.dynamic_range) * 100
        self.pwm.ChangeDutyCycle(duty_cycle)

dynamic_range = 3.3
pin = 12
dac = pwm.PWM_DAC(pin, 1000, dynamic_range)

try: 
    print(f"Частота:{signal_frequency}Hz, Амплитуда:{amplitude}V")

    start_time = time.time()
    while True:
        t = time.time() - start_time
        norm_val = sg.get_sin_wave_amplitude(signal_frequency, t)
        target_voltage = norm_val * amplitude
        sg.wait_for_sampling_period(sampling_frequency)
except KeyboardInterrupt:
    print("прервано")
finally:
    dac.deinit()