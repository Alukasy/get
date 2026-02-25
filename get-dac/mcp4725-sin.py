import RPi.GPIO as GPIO
import signal_generator as sg 
import time 
import mcp4725_driver as pwm

amplitude = 3.0
signal_frequency = 10    
sampling_frequency = 1000 



dynamic_range = 3.3
pin = 12
dac = pwm.MCP4725(5.0)

try: 
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