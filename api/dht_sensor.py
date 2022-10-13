from machine import Pin, Timer
import dht
from time import localtime


class Dht_s:
    def __init__(self, pin):
        self.dht_s = dht.DHT11(Pin(pin))

    def mesure(self):
        self.dht_s.measure()
        print(f'T = {self.dht_s.temperature()} h: {self.dht_s.humidity()}')
        return self.dht_s.temperature(), self.dht_s.humidity()

    def m_t(self):
        return self.dht_s.temperature()

    def m_h(self):
        return self.dht_s.humidity()

    def t_mesure(self, *args):
        self.mesure()
        self.write_data_to_file()

    def continu_measure(self):
        sensor = Dht_s(10)
        self.timer = Timer()
        self.timer.init(mode=Timer.PERIODIC, period=1500, callback=sensor.t_mesure)

    def stop_measure(self):
        self.timer.deinit()
        
    def write_data_to_file(self, filename='file.txt'):
        with open(filename, 'a') as file:
            file.write(f't,{self.dht_s.temperature()}, h,{self.dht_s.humidity()}')



if __name__ == '__main__':
    sensor = Dht_s(10)
    timer = Timer()
    
    timer.init(mode=Timer.PERIODIC, period=1500, callback=sensor.t_mesure)
    