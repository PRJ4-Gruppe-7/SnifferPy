import threading
import Sniffer
import SocketServer
import time
from mac_vendor_lookup import MacLookup

def main():
    Devices = {}
    Mutex = threading.Lock()
    SnifferObj = Sniffer.Sniffer(Devices, Mutex)
    SocketObj = SocketServer.SocketServer(Devices, Mutex)

    print("Starting SnifferThread")
    SnifferThread = threading.Thread(target=SnifferObj.run)
    SnifferThread.start()

    print("Starting SocketThread")
    SocketThread = threading.Thread(target=SocketObj.run)
    SocketThread.start()

    while True:
        Mutex.acquire()
        try:
            for MAC, RSSI in Devices.items():
                try:
                    print(MacLookup().lookup(MAC) + "\t\t" + str(RSSI))
                except:
                    print(MAC + "\t\t" + str(RSSI))
        finally:
            Mutex.release()

        print("\n \t----------------------- \n")
        time.sleep(10)


if __name__ == "__main__":
    main()
