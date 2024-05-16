"""
https://www.instructables.com/Raspberry-Pi-Remote-GPIO/
Enable remote GPIO:
sudo systemctl enable pigpiod
sudo systemctl start pigpiod

sudo pigpiod -n 192.168.1.4

https://magpi.raspberrypi.com/articles/remote-control-gpio-raspberry-pi-gpio-zero
"""

from time import sleep

from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
# from signal import pause

factory = PiGPIOFactory("127.0.0.1")

led = LED(17, pin_factory=factory)  # remote pin

while True:

    led.on()

    sleep(1)

    led.off()

    sleep(1)
