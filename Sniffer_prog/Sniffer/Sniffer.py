import threading
import collections
from scapy.all import sniff, Dot11

class Sniffer():
    def __init__(self, Devices: dict, Mutex: threading.Lock):
        conf.iface = "mon0"
        self.devices = Devices
        self.mut = Mutex

    def run(self):
        ## Setup sniff
        sniff(prn=self.packet_handler)

    def packet_handler(self,packet):
        if packet.haslayer(Dot11):
            try:
                self.mut.acquire()
                if packet.addr2 and str(packet.addr2) not in self.devices and packet.dBm_AntSignal > -69:
                    # Make circularbuffer if MAC does not exist in devices
                    temp = collections.deque(maxlen = 10)
                    # Append to buffer
                    temp.append(packet.dBm_AntSignal)
                    # set MAC in devicess to temp value (RSSI)
                    self.devices[str(packet.addr2)] = temp

                elif packet.dBm_AntSignal > -69:
                    # If MAC exists in devices append to buffer
                    self.devices[str(packet.addr2)].append(packet.dBm_AntSignal)


            finally:
                self.mut.release()
