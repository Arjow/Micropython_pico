print('main')
from time import localtime
import head


## BOOT IMPORTEND SERVICES
# connect wifi
head.wifi_connect()
head.fix_time()

## run programs
head.weather_api()
head.dht_sensor_update()
head.rotate_motor()
head.ifbutton()
