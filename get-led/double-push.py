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
    up = GPIO.input(button_up)
    down = GPIO.input(button_down)
    if up or down:
        flag = True 
        if up and down:
            num = 255
            print('ок')
        else:
            if up:
                num = min(255,num+1)
            else:
                num = max(0,num-1)
    else:
        flag = False
    if flag:
        print(num,dec2bin(num))        
        GPIO.output(leds,dec2bin(num))
        time.sleep(sleep_time*2)