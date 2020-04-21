
from mac_vendor_lookup import MacLookup
from scapy.all import *

mac = MacLookup()

conf.iface = "mon0"
devices = set()
## Define our Custom Action function
def custom_action(packet):
    if packet.haslayer(Dot11):
        if packet.addr2 and (packet.addr2 not in devices) :
            devices.add(packet.addr2)
            try:
                device = mac.lookup(packet.addr2)
            except:
                device = str(packet.addr2)

            print(len(devices), device,str(packet.dBm_AntSignal) + "dBm")


## Setup sniff
sniff(prn=custom_action)
