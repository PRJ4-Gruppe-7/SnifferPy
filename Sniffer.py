from mac_vendor_lookup import MacLookup
import asyncio
from scapy.all import *


class Sniffer():
    def __init__(self, Devices: dict, Mutex: asyncio.Lock):
        conf.iface = "mon0"
        self.devices = Devices
        self.mut = Mutex

    def run(self):
        ## Setup sniff
        sniff(prn=self.packet_handler)


    def packet_handler(self,packet):
        if packet.haslayer(Dot11):
            self.mut.acquire()
            try:

                if packet.addr2 and str(packet.addr2) not in self.devices :
                    self.devices[str(packet.addr2)] = [packet.dBm_AntSignal]

                else:
                    self.devices[str(packet.addr2)] += [packet.dBm_AntSignal]
                    
            finally:
                self.mut.release()
