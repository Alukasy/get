import signal_generator as sg 
import time 
import pwm_dac as pwm

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000 



dynamic_range = 3.2
pin = 12

try: 
    dac = pwm.PWM_DAC(pin, 1000, dynamic_range, True)
    print(f"Генерация: Частота:{signal_frequency}Hz, Амплитуда:{amplitude}V")
    start_time = time.time()
    
    while True:
        t = time.time() - start_time
        norm_val = sg.get_sin_wave_amplitude(signal_frequency, t)
        target_voltage = norm_val*amplitude
        dac.set_voltage(target_voltage)
        sg.wait_for_sampling_period(sampling_frequency)

except KeyboardInterrupt:
    print("\nПрервано пользователем")
finally:
    dac.deinit()