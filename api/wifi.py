import network
from time import sleep
from resources import secret

''' Some work arrounds for wifi
# create instances
sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)

# connect to wifi
sta_if.active(True)
sta_if.connect('<your SSID>', '<your key>')

# controller verbinding
sta_if.isconnected()

# return ip adres
sta_if.ifconfig()
'''


wlan = network.WLAN(network.STA_IF)

def do_connect(ssid=None, key=None, re=False):
    """Connect to wifi

    Ask for password and klatey, as they don't exist.
    
    Parameters:
    -----------
    ssid str:
        string with the ssid of the wifi
    key str:
        string with the key of the wifi
    re bool:
        reconnect False or True
    Return:
    -------
    bool:
        True if connected or False as not connected
    tuble:
        connection details
    """
    if wlan.isconnected() and not re:
        print('already connected')
        return wlan.isconnected(), wlan.ifconfig()
    if not ssid:
        ssid = input('ssid: ')
    if not key:
        key = input('key: ')
    if not wlan.active(True):
        wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, key)
        sleep(3)
    else:
        raise('error with connect to wifi')
    print('wlan is connected?', wlan.isconnected())
    return wlan.isconnected(), wlan.ifconfig()


def connect():
    '''connect to wifi

    use secret.py to for login credentials
    '''
    for login in secret.logincredits:
        print('try to connect to: ', login['ssid'])
        do_connect(
            ssid=login['ssid'],
            key=login['key']
            )
        if wlan.isconnected():
            return wlan.ifconfig()
    print("Can't connect to wifi acces point")
    for ssids in wlan.scan():
        print('wifi accespoints:', ssids[0])

print(__name__)
if __name__ == '__main__':
    print(connect())
    fix_time()
    for ssids in wlan.scan():
        print('wifi accespoints:', ssids[0])
