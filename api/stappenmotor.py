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
    for i in range(0+4*dirr, 4-4*dirr, 1-dirr*2):
        m_pins[(0+i)%4].on(); m_pins[(1+i)%4].off(); m_pins[(2+i)%4].off(); m_pins[(3+i)%4].off()
        sleep_ms(time)

def smootstep_l(time):
    for i in range(4):
        m_pins[(0+i)%4].on(); m_pins[(1+i)%4].off(); m_pins[(2+i)%4].off(); m_pins[(3+i)%4].off()
        sleep_ms(time)
        m_pins[(0+i)%4].on(); m_pins[(1+i)%4].on(); m_pins[(2+i)%4].off(); m_pins[(3+i)%4].off()
        sleep_ms(time)
        
def smootstep_r(time):
    for i in range(4):
        m_pins[(0-i)%4].on(); m_pins[(1-i)%4].off(); m_pins[(2-i)%4].off(); m_pins[(3-i)%4].off()
        sleep_ms(time)
        m_pins[(0-i)%4].on(); m_pins[(1-i)%4].off(); m_pins[(2-i)%4].off(); m_pins[(3-i)%4].on()
        sleep_ms(time)

def smootsteps(steps, time, dirr='left'):
    if dirr == 'left':
        for i in range(0, steps):
            smootstep_l(time)
    elif dirr == 'right':
        for i in range(0, steps):
            smootstep_r(time)
    for i in range(0, 4):
        m_pins[i].off()

def steps(steps, time, dirr=0):
    for z in range(0, steps):
        step(time, dirr)
    for i in range(0, 4):
        m_pins[i].off()

def ruitenwissers():
    for i in range(10):
        smootsteps(100, 1, 'left')
        smootsteps(100, 1, 'right')

def rotatedegree(degrees=45, time=1, *args):
    if degrees < 0 :
        dirr = 'left'
    else:
        dirr = 'right'
    smootsteps(abs(512/360*degrees), time=time, dirr=dirr)

def rotatedegree_t(t, degrees=45):
    return rotatedegree(degrees=45)
