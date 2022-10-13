'''Module for DHT 11 sensor.

Measure and read temperature and humidity from dht 11 sensor.
Used microcontroler pico with micropyton.

'''

from machine import Pin, Timer
import dht
from time import localtime


class Dht_s:
    '''DHT11 sensor.

    Mesure temperature and humidity with a dht11 sensor.

    Attributes
    ----------
    pin: int
        pin in of data pin of dht11 sensor
    
    methods
    ---------
    mesure
    m_t
    m_h
    t_mesure
    continu_measure
    stop_measure

    Returns:
    --------
    '''
    def __init__(self, pin, write_to_file=False):
        self.dht_s = dht.DHT11(Pin(pin))
        self.write_to_file = write_to_file

    def mesure(self):
        """measure temperature and humidity from sensor.

        measure temperature and humidity from sensor.
        and safe value in class. and return value.

        Returns
        -------
        tuple:
            float:
                temperature
            float:
                humidity
        """
        self.dht_s.measure()
        print(f'T = {self.dht_s.temperature()} h: {self.dht_s.humidity()}')
        return self.dht_s.temperature(), self.dht_s.humidity()

    def m_t(self):
        """Get measured temperature.
        
        Returns
        -------
        float:
            measured temperature
        """
        return self.dht_s.temperature()

    def m_h(self):
        """Get measured humidity.
        
        Returns
        -------
        float:
            measured humidity
        """
        return self.dht_s.humidity()

    def _t_mesure(self, *args):
        '''Meseare functionn for continue_measure.
        Write measured data to file.

        Mesuare Temperature and humidity and write value to file
        '''
        self.mesure()
        if self.write_to_file:
            self.write_data_to_file()

    def continu_measure(self):
        '''Set a timer to mesure temp and humidity periodic.'''
        self.timer = Timer()
        self.timer.init(mode=Timer.PERIODIC, period=1500,
            callback=self._t_mesure)

    def stop_measure(self):
        '''Stop continue_measure.'''
        self.timer.deinit()
        
    def write_data_to_file(self, filename='file.txt'):
        """Write temperature and humidity to file
        
        Parameter
        ---------
        filename: str
            name of file. Must end with '.txt'
        
        """
        with open(filename, 'a') as file:
            file.write(f't,{self.dht_s.temperature()}, h,{self.dht_s.humidity()}')



if __name__ == '__main__':
    sensor = Dht_s(10)
    timer = Timer()

    timer.init(mode=Timer.PERIODIC, period=1500, callback=sensor.t_mesure)
    