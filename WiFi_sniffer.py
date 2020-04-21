
from mac_vendor_lookup import MacLookup
from scapy.all import *

mac = MacLookup()

conf.iface = "mon0"
devices = {}
## Define our Custom Action function
def custom_action(packet):
    if packet.haslayer(Dot11):
        if packet.addr2 and str(packet.addr2) not in devices :
            devices[str(packet.addr2)] = [packet.dBm_AntSignal]

            try:
                device = mac.lookup(packet.addr2)
            except:
                device = str(packet.addr2)

            print(len(devices), device ,str(packet.dBm_AntSignal) + "dBm")

        else:
            devices[str(packet.addr2)] += [packet.dBm_AntSignal]
            print(mac.lookup(packet.addr2),devices[str(packet.addr2)])


## Setup sniff
sniff(prn=custom_action)
