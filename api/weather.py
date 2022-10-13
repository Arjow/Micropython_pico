import urequests
import time
from machine import Pin, Timer

class Weather:
    '''get weather data from buienrader api
    
    Attributes
    ----------
    
    functions
    ---------
    
    Returns:
    --------
    '''

    def __init__(self, lat=52.19, lon=4.42, pins=[0, 1, 2, 3, 4]):
        '''
        Parameters
        ----------
        lat: float
            latitude
        lon: float
            longitude
        Pins: list
            [green, blue, orange, red]
        
        '''
        self.lat = round(lat, 2)
        self.lon = round(lon, 2)
        self.url = self.create_url()

        self.green = Pin(pins[0], Pin.OUT)
        self.blue = Pin(pins[1], Pin.OUT)
        self.yellow = Pin(pins[2], Pin.OUT)
        self.orange = Pin(pins[3], Pin.OUT)
        self.red = Pin(pins[4], Pin.OUT)

        self.r_data = None

        self.error = False
        self.timer = Timer()
        _timer_on = False
        
        self.test_LEDS()

    def create_url(self):
        '''create api url

        set the gps coordinate in url
        
        Returns:
        --------
        str
            url of buienradar api
        '''
        return f'https://gpsgadget.buienradar.nl/data/raintext?lat={self.lat}&lon={self.lon}'

    def get_request(self):
        """Request weather data

        Request the wather data from gpsgadget.buienradar.nl
        print the request time in terminal
        """
        print('get request on', ':'.join(str(i) for  i in time.localtime()[3:6]))
        try:
            self.r_data = urequests.get(self.url).content
        except OSError as err:
            print(err)
            print('get no new data')
            self.error = True

    def clr_str_data(self):
        """create data layout
        (((hh,mm), (...),..) (mm_rainfal, mm_.., ..)
        """
        self.clear_str_data = [item.split(b'|') for item in self.r_data.replace(b'\r', b'').split(b'\n') if not item == b'']
        clear_data = ((tuple(mm_time[1].decode('utf-8').split(':')),int(mm_time[0])) for mm_time in self.clear_str_data)
        self.time = []
        self.rain = []
        for item in clear_data:
            self.time.append([int(item[0][0]),
                              int(item[0][1])])
            self.rain.append(self.rain_intensitie(item[1]))

    def time_diff(self, _time):
        """ change (hh:mm) notation to minutes
        """
        return (_time[0]-time.localtime()[3])*60+_time[1]-time.localtime()[4]

    def rain_intensitie(self, val):
        '''Calculate the rain_intensitie to rain in mm.

        Paramters:
        ----------
        val: int
            rain intensitie
            
        returns:
        --------
        float
            rain in [mm]
        '''
        return round(10**((val-109)/32), 3)

    def rainfall_next_hour(self):
        '''Rainfall next_hour in mm scale.

        Return
        ------
        flaot
            [mm] rain next hour
        '''
        self.mm_rain_hour = int(0)
        for time, rain in zip(self.time, self.rain):
            if self.time_diff(time) <=60:
                self.mm_rain_hour += round(rain, 3)
            else:
                break
        print(f'rainfall next hour is {self.mm_rain_hour} mm')
        return self.mm_rain_hour

    def rainfall_next_2_hours(self):
        '''Rainfall next 2 hours in mm scale.

        Return
        ------
        flaot
            [mm] rain next hour
        '''
        self.mm_rain_2_hours = sum(self.rain)
        var = ':'.join(str(i) for i in self.time[-1])
        print(f"expacted rainfall before {var} is {self.mm_rain_2_hours} mm")


    def update(self):
        '''Update weather data'''
        self.get_request()
        if not self.error:
            self.clr_str_data()
            self.rainfall_next_hour()
            self.rainfall_next_2_hours()
        self.Leds()

    def red_LED_toggle(self):
        self._timer_on = True
        def _red_LED_toggle(t):
            self.red.toggle()
        self.timer.init(freq=2.5,
                        mode=Timer.PERIODIC,
                        callback=_red_LED_toggle)

    def red_LED_toggle_off(self):
        self._timer_on = False
        self.timer.deinit()
        self.red.off()

    def test_LEDS(self):
        self.green.on()
        self.blue.on()
        self.yellow.on()
        self.orange.on()
        self.red_LED_toggle()
        time.sleep(1)
        self.timer.deinit()
        self.green.off()
        self.blue.off()
        self.yellow.off()
        self.orange.off()
        self.red_LED_toggle_off()
   
    def Leds(self):
        '''set Led on based on mm_rain_hour'''
        # check for error
        if self.error:
            self.red_LED_toggle()
            return
        elif self._timer_on:
            self.red_LED_toggle_off()
        # check rain
        self.green.off()
        self.blue.off()
        self.yellow.off()
        self.orange.off()
        self.red.off()
        if self.mm_rain_hour == 0:
            self.green.on()
        elif self.mm_rain_hour <= 0.1:
            self.blue.on()
        elif self.mm_rain_hour <= 0.5:
            self.yellow.on()
        elif self.mm_rain_hour <= 1.5:
            self.orange.on()
        else:
            self.red.on()
    
    def update_periodice(self):
        self.update()
        self._periodic_update = Timer()
        per = 600000 # miliseconds = 300 sec = 5 min
        def perodic_update(t):
            self.update()
        self._periodic_update.init(mode=self._periodic_update.PERIODIC,
                             period=per,
                             callback=perodic_update)
        

if __name__ == '__main__':
    coorodinaten = (52.19, 4.42)
    weather = Weather(coorodinaten[0], coorodinaten[1])
