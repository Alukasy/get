import RPi.GPIO as GPIO
import signal_generator as sg 
import time 

# Параметры
amplitude = 3.0
signal_frequency = 5.0      # (10 / 2)
sampling_frequency = 500.0  # (1000 / 2) 

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose = False):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setwarnings(False) # Чтобы не спамило варнингами при перезапуске
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0)

    def deinit(self):
        self.pwm.stop()
        GPIO.cleanup()
    
    def set_voltage(self, voltage):
        # Ограничиваем напряжение, чтобы не выйти за 0..3.3
        if voltage < 0: voltage = 0
        if voltage > self.dynamic_range: voltage = self.dynamic_range

        duty_cycle = (voltage / self.dynamic_range) * 100
        self.pwm.ChangeDutyCycle(duty_cycle)

# Инициализация
dynamic_range = 3.3
pin = 12
# Создаем объект класса, который описан выше
dac = PWM_DAC(pin, 1000, dynamic_range)

try: 
    print(f"Генерация: Частота:{signal_frequency}Hz, Амплитуда:{amplitude}V")
    start_time = time.time()
    
    while True:
        t = time.time() - start_time
        
        # 1. Считаем значение (0..1)
        norm_val = sg.get_sin_wave_amplitude(signal_frequency, t)
        
        # 2. Масштабируем (0..3.0)
        target_voltage = norm_val * amplitude
        
        # 3. ОТПРАВЛЯЕМ НА ЦАП (этого не было)
        dac.set_voltage(target_voltage)
        
        # 4. Ждем такта дискретизации
        sg.wait_for_sampling_period(sampling_frequency)

except KeyboardInterrupt:
    print("\nПрервано пользователем")
finally:
    dac.deinit()
