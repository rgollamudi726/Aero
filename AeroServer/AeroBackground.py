import OutletControl
import datetime
import xml.etree.ElementTree

def AeroBackgroundInitialSetup():

    AeroSettings=xml.etree.ElementTree.parse('AeroSettings.xml').getroot()
    for atype in AeroSettings.findall('device'):
        print(atype.get('name'))


def AeroBackground():
    AeroBackgroundInitialSetup()