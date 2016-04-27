import OutletControl
import datetime
import xml.etree.ElementTree
import time


def AeroBackgroundInitialSetup():
    
    global numDevices
    global numGrowLight
    global numContPump
    global numNonContPump
    global GrowLightDict
    global ContPumpDict

    global sleepTime 
    global pumpOnCounter


    GrowLightDict = dict()
    ContPumpDict = dict()

    numDevices = 0
    numGrowLight = 0
    numContPump = 0
    numNonContPump = 0
    AeroSettings=xml.etree.ElementTree.parse('AeroSettings.xml').getroot()
    
    for devices in AeroSettings:
        tag = devices.tag
        attrib =  devices.attrib
        if(tag == 'device'):            
            devName = attrib['name']
            if(devName == 'Grow Light'):
                
                title = devices.find('title').text
                TurnOnTime = devices.find('TurnOnTime').text
                TurnOffTime = devices.find('TurnOffTime').text
                Outlet = devices.find('Outlet').text
                LightDict = dict()
                LightDict['title'] = title
                LightDict['TurnOnTime'] = TurnOnTime
                LightDict['TurnOffTime'] = TurnOffTime
                LightDict['Outlet'] = Outlet
                LigtDuctNum = 'Light' + str(numGrowLight+1)
                GrowLightDict[LigtDuctNum] = LightDict
                numGrowLight = numGrowLight +1
                                
            elif(devName == 'Pump'):
                title = devices.find('title').text
                ContOp = devices.find('ContinuousOperation').text
                Outlet = devices.find('Outlet').text
                if(ContOp == 'YES'):                    
                    OnTime = devices.find('OnTime').text
                    OffTime = devices.find('OffTime').text
                    PDict = dict()
                    PDict['title'] = title
                    PDict['ContinuousOperation'] = ContOp
                    PDict['OnTime'] = OnTime
                    PDict['OffTime'] = OffTime
                    PDict['Outlet'] = Outlet
                    PDictNum = 'ContPump' + str(numContPump+1)
                    ContPumpDict[PDictNum] = PDict
                    numContPump = numContPump + 1

    if(numContPump > 1):
        print("PANIC\n")
    elif(numContPump == 1):
        sleepTime = int(ContPumpDict['ContPump1']['OnTime'])
        pumpOnCounter = 0
    elif(numContPump == 0):
        sleepTime = 60

                    
                


def AeroBackground():

    global numDevices
    global numGrowLight
    global numContPump
    global numNonContPump
    global GrowLightDict
    global ContPumpDict

    global sleepTime 
    global pumpOnCounter

    AeroBackgroundInitialSetup()

    print("Sleep Time is ",str(sleepTime))

    while(True):        
        if(numContPump == 1):
            outletNum = int(ContPumpDict['ContPump1']['Outlet']) -1 
            if(pumpOnCounter <= 0):
               pumpOnCounter =  int(ContPumpDict['ContPump1']['OffTime'])
               OutletControl.OutletOn(OutletControl.OutletList[outletNum])
            else:
                pumpOnCounter = pumpOnCounter - sleepTime
                OutletControl.OutletOff(OutletControl.OutletList[outletNum])

        if(numGrowLight == 1):
            outletNum = int(GrowLightDict['Light1']['Outlet']) - 1
            TurnOnTime = GrowLightDict['Light1']['TurnOnTime']            
            OnHour,OnMinute = TurnOnTime.split(':',maxsplit=1)
            OnHour = int(OnHour)
            OnMinute  = int(OnMinute )
            OnTime = datetime.time(hour=OnHour,minute=OnMinute)
            
            TurnOffTime = GrowLightDict['Light1']['TurnOffTime']
            OffHour,OffMinute = TurnOffTime.split(':',maxsplit=1)
            OffHour = int(OffHour)
            OffMinute  = int(OffMinute )
            OffTime = datetime.time(hour=OffHour,minute=OffMinute)
            
            
            curtime = datetime.datetime.now()            
            hour = int(curtime.hour)
            minute = int(curtime.minute)
            comptime = datetime.time(hour=hour,minute=minute)
            if( (comptime >= OnTime) and ( comptime < OffTime)):
                #print("Turning on Grow Light")
                OutletControl.OutletOn(OutletControl.OutletList[outletNum])
            else:
                #print("Turning off Grow Light")
                OutletControl.OutletOff(OutletControl.OutletList[outletNum])


        time.sleep(sleepTime)
