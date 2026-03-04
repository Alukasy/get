import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose 
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21 

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def __del__(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        signal = [int(bit) for bit in bin(int(number))[2:].zfill(8)]
        GPIO.output(self.bits_gpio, signal)
    
    def successive_approximation_adc(self):
        value = 0
        for i in range(7, -1, -1):
            test_value = value | (1 << i)
            self.number_to_dac(test_value)
            time.sleep(self.compare_time)
            
            if GPIO.input(self.comp_gpio) == 0:
                value = test_value
        
        return value

    def get_sar_voltage(self):
        code = self.successive_approximation_adc()
        return (code / 256) * self.dynamic_range

if __name__ == "__main__":
    MY_DYNAMIC_RANGE = 3.3 
    try:
        adc = R2R_ADC(dynamic_range=MY_DYNAMIC_RANGE)
        print("Start SAR ADC measurements")

        while True:
            u = adc.get_sar_voltage()
            print(f"SAR Voltage: {u:.4f} V")
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nStopped")
    finally:
        if adc:
            del adc
