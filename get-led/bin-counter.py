import RPi.GPIO as GPIO 
import time 

GPIO.setmode(GPIO.BCM) 

leds = [24, 22, 23, 27, 17, 25, 12, 16]
leds = leds[::-1]

GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)

button_down = 10
button_up = 9
GPIO.setup([button_down,button_up], GPIO.IN)

num = 0

def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

sleep_time = 0.2

while True:
    if GPIO.input(button_up):
        if num <=255:
            num+=1
        print(num, dec2bin(num))
        time.sleep(sleep_time)
    elif GPIO.input(button_down):
        if num >= 1:
            num -= 1
        print(num, dec2bin(num))
        time.sleep(sleep_time)
    GPIO.output(leds,dec2bin(num))