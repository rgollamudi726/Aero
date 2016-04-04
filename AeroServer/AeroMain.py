#VS remote debugging
import ptvsd
ptvsd.enable_attach(secret=None)
ptvsd.wait_for_attach()

import time
import zmq
import OutletControl
import AeroBackground

if __name__ == '__main__':

    OutletControl.initAeroIO()
    IOLockState = OutletControl.isGPIOLocked()
    AeroBackground.AeroBackground()
    while(True):

        time.sleep(100)
