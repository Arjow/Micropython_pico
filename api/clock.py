"""Time related classes, functions, fixes."""
import ntptime
from machine import RTC
from time import localtime


def fix_time(summ=1):
    """ Set the local time to  ntp server time.

    Set the time in timezone Amsterdam
    
    Parameters:
    -----------
    summ:
        int: if summer time:1 if winter time: 0 
    """
    tm = localtime(ntptime.time()+3600*2)
    RTC().datetime((tm[0], tm[1], tm[2], tm[6] + summ, tm[3], tm[4], tm[5], 0))

