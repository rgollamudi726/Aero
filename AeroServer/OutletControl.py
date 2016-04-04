import RPi.GPIO as GPIO
import asyncio

Outlet1 = 11 # Grow Light1
Outlet2 = 13 # Pump
Outlet3 = 15
Outlet4 = 16
OutletList = [Outlet1,Outlet2,Outlet3,Outlet4]

def initGPIOLock():
    global GPIOLock1
    global GPIOLock2
    global GPIOLock3
    global GPIOLock4
    GPIOLock1 = asyncio.Lock()
    GPIOLock2 = asyncio.Lock()
    GPIOLock3 = asyncio.Lock()
    GPIOLock4 = asyncio.Lock()    

def isGPIOLocked(Outlet):
    global GPIOLock1
    global GPIOLock2
    global GPIOLock3
    global GPIOLock4

    if(Outlet == Outlet1):
        return GPIOLock1.locked()
    elif(Outlet == Outlet2):
        return GPIOLock2.locked()
    elif(Outlet == Outlet3):
        return GPIOLock3.locked()
    elif(Outlet == Outlet4):
        return GPIOLock4.locked()


def initAeroIO():
    #Set Pins 11,13,15,16 High to turn off all outlets
    global OutletList
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(OutletList, GPIO.OUT, initial=GPIO.HIGH)
    initGPIOLock()

def OutletOn(Outlet):    
    global GPIOLock1
    global GPIOLock2
    global GPIOLock3
    global GPIOLock4

    if(Outlet == Outlet1):
        GPIOLock=GPIOLock1
    elif(Outlet == Outlet2):
        GPIOLock=GPIOLock2
    elif(Outlet == Outlet3):
        GPIOLock=GPIOLock3
    elif(Outlet == Outlet4):
        GPIOLock=GPIOLock4

    GPIOLock.acquire()
    GPIO.output(Outlet, GPIO.LOW)
    staus = GPIO.input(Outlet)
    GPIOLock.release()
    if(status == GPIO.LOW):        
        return True
    else:        
        return False
    
def OutletOff(Outlet):
    global GPIOLock1
    global GPIOLock2
    global GPIOLock3
    global GPIOLock4

    if(Outlet == Outlet1):
        GPIOLock=GPIOLock1
    elif(Outlet == Outlet2):
        GPIOLock=GPIOLock2
    elif(Outlet == Outlet3):
        GPIOLock=GPIOLock3
    elif(Outlet == Outlet4):
        GPIOLock=GPIOLock4
    
    GPIOLock.acquire()
    GPIO.output(Outlet, GPIO.HIGH)
    staus = GPIO.input(Outlet)
    GPIOLock.release()
    if(status == GPIO.HIGH):        
        return True
    else:    
        return False

