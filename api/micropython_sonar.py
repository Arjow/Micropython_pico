from machine import Pin
import time

trig_pin = 2
echo_pin = 3

class Sonar:
    
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = Pin(trig_pin, Pin.OUT)
        self.echo_pin = Pin(echo_pin, Pin.IN)
        self.time_trig = 0
        self.time_ech = 0

    
    def trigger(self):
        time.sleep_us(5)
        self.trig_pin.on()
        time.sleep_us(10)
        self.trig_pin.off()
        self.time_trig = time.ticks_us()
        time.sleep_us(100)
    
    def echo(self):
        while True:
            if not self.echo_pin.value():
                self.time_ech = time.ticks_us()
                break
        
    
    def mesure(self):
        self.trigger()
        self.echo()   
        return time.ticks_diff(self.time_ech, self.time_trig)

          
if __name__ == "__main__":
    sonar1 = Sonar(trig_pin, echo_pin)
    print(sonar1.mesure())
