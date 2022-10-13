print('head')
from apps import wifi
from apps import clock
from apps import weather
from apps import stappenmotor
from apps import dht_sensor
from machine import Pin, Timer
import time

LOCATION = 52.19, 4.42

def wifi_connect():
    wifi.connect()

def fix_time():
    try:
        clock.fix_time()
    except OSError:
        print('Can not set the time')
        print('localtime =', time.localtime())

def weather_api():
    ## start WEATHER API
    # get weather information
    print('gethering weather information')
    w = weather.Weather(LOCATION[0], LOCATION[1])
    # start weather thread
    w.update_periodice()

def weather_update():
    """
    Parameters:
    triggerPin = GP5 of 5
    """
    trigger = Pin(5, Pin.IN, Pin.PULL_UP)
    ## start WEATHER API
    # get weather information
    print('loading weather')
    w = weather.Weather(LOCATION[0], LOCATION[1])
    # start weather thread
    auto_off = Timer()
    led = False
    while True:
        if not trigger.value():
            print('triggered')
            w.update()
            led = True
        if led:
            auto_off.init(mode=Timer.ONE_SHOT, period=5000, callback=w.Leds_off)
            led = False


def dht_sensor_update():
    sensor = dht_sensor.Dht_s(10)
    timer = Timer()
    timer.init(mode=Timer.PERIODIC, period=50000, callback=sensor.t_mesure)

def rotate_motor():
    timer = Timer()
    timer.init(mode=Timer.PERIODIC, period=5000, callback=stappenmotor.rotatedegree_t)

def ifbutton(fn=None):
    if not fn:
        def foo(arg):
            print('foo')
            return None
        fn = foo
    trigger = Pin(11, Pin.IN, Pin.PULL_UP)
    trigger.irq(handler=fn, trigger=Pin.IRQ_FALLING)
    return True
    

if __name__ == '__main__':
    pass