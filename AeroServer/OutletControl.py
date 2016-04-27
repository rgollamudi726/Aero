import RPi.GPIO as GPIO
import asyncio
import time

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
    while( not GPIOLock1.acquire()):
        print("GPIO LOCK1 not acquired")
    while(GPIOLock1.locked()):
        print("GPIO1 is locked")
        GPIOLock1.release()

    GPIOLock2 = asyncio.Lock()
    while( not GPIOLock2.acquire()):
        print("GPIO LOCK2 not acquired")
    while(GPIOLock2.locked()):
        print("GPIO2 is locked")
        GPIOLock2.release()

    GPIOLock3 = asyncio.Lock()
    while( not GPIOLock3.acquire()):
        print("GPIO LOCK3 not acquired")
    while(GPIOLock3.locked()):
        print("GPIO3 is locked")
        GPIOLock3.release()

    GPIOLock4 = asyncio.Lock()    
    while( not GPIOLock4.acquire()):
        print("GPIO LOCK4 not acquired")
    while(GPIOLock4.locked()):
        print("GPIO4 is locked")
        GPIOLock4.release()


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
    
    while(not GPIOLock.acquire()):
        print("Failed to acquire lock\n")        
    
    GPIO.output(Outlet, GPIO.LOW)
    status = GPIO.input(Outlet)
    while(GPIOLock.locked()):
        print("Failed to release lock\n")
        GPIOLock.release()        
        #time.sleep(5)

    time.sleep(0.05)
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
    
    while(not GPIOLock.acquire()):
        print("Failed to acquire lock\n")        
    
    GPIO.output(Outlet, GPIO.HIGH)
    status = GPIO.input(Outlet)

    while(GPIOLock.locked()):
        print("Failed to release lock\n")
        GPIOLock.release()
        
    
    if(status == GPIO.HIGH):        
        return True
    else:    
        return False

