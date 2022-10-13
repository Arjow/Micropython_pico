# stappenmotor
from machine import Pin
from time import sleep_ms

# connect stappenmotor:
# 6 to in1
# 7 to in2
# 8 to in3
# 9 to in4

m_pins = [Pin(i, Pin.OUT) for i in range(6, 10)]


def step(time, dirr=0):
    '''Rotate 1 fullstep.

    Parameters
    ----------
    sleep: int
        delay in ms
    dirr: bool (o or 1)
        Dirrection of step. Left or right rotation.
    '''
    for i in range(0+4*dirr, 4-4*dirr, 1-dirr*2):
        m_pins[(0+i) % 4].on()
        m_pins[(1+i) % 4].off()
        m_pins[(2+i) % 4].off()
        m_pins[(3+i) % 4].off()
        sleep_ms(time)


def steps(steps, time, dirr=0):
    '''Rotate multiple steps.

    Parameters
    ----------
    steps: int
        number of steps
    time: int
        delay in ms
    dirr: bool or 1 or 0
        Dirrection of step. Left or right rotation.
    '''
    for z in range(0, steps):
        step(time, dirr)
    for i in range(0, 4):
        m_pins[i].off()


def smootstep_l(time):
    '''Rotate 1 full halvestep to left.

    Parameters
    ----------
    sleep: int
        delay in ms
    '''
    for i in range(4):
        m_pins[(0+i) % 4].on()
        m_pins[(1+i) % 4].off()
        m_pins[(2+i) % 4].off()
        m_pins[(3+i) % 4].off()
        sleep_ms(time)
        m_pins[(0+i) % 4].on()
        m_pins[(1+i) % 4].on()
        m_pins[(2+i) % 4].off()
        m_pins[(3+i) % 4].off()
        sleep_ms(time)


def smootstep_r(time):
    '''Rotate 1 full halvestep to right.

    Parameters
    ----------
    sleep: int
        delay in ms
    '''
    for i in range(4):
        m_pins[(0-i) % 4].on()
        m_pins[(1-i) % 4].off()
        m_pins[(2-i) % 4].off()
        m_pins[(3-i) % 4].off()
        sleep_ms(time)
        m_pins[(0-i) % 4].on()
        m_pins[(1-i) % 4].off()
        m_pins[(2-i) % 4].off()
        m_pins[(3-i) % 4].on()
        sleep_ms(time)


def smootsteps(steps, time, dirr='left'):
    '''Rotate multiple steps.

    Parameters
    ----------
    steps: int
        number of steps
    time: int
        delay in ms
    dirr: str: 'left' or 'right'
        Dirrection of step. Left or right rotation.
    '''
    if dirr == 'left':
        for i in range(0, steps):
            smootstep_l(time)
    elif dirr == 'right':
        for i in range(0, steps):
            smootstep_r(time)
    for i in range(0, 4):
        m_pins[i].off()


def ruitenwissers():
    '''Rotate 10 times 100 steps left and 100 steps right.'''
    for i in range(10):
        smootsteps(100, 1, 'left')
        smootsteps(100, 1, 'right')


def rotatedegree(degrees=45, time=1, *args):
    '''Rotate degrees. 

    Ratate degrees if negative degree the motor wil turn left,
    positive degree motor turn right.

    Parameters
    ----------
    time:int
        delay in ms between the steps
    degrees: float
        rotate x degrees.
    '''
    if degrees < 0:
        dirr = 'left'
    else:
        dirr = 'right'
    smootsteps(abs(512/360*degrees), time=time, dirr=dirr)


def rotatedegree_t(t, degrees=45):
    '''Function for machine.Timer interupt'''
    return rotatedegree(degrees)
