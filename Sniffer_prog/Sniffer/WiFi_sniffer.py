import threading
import Sniffer
import time
from mac_vendor_lookup import MacLookup

def main():
    Devices = {}
    Mutex = threading.Lock()
    SnifferObj = Sniffer.Sniffer(Devices, Mutex)

    print("Starting SnifferThread")
    SnifferThread = threading.Thread(target=SnifferObj.run)
    SnifferThread.start()

    while True:
        try:
            Mutex.acquire()
            tempstring = ""
            print("MAC-address:" + "\t" + "Avg. RSSI-Value:\n")
            print("------------------------------------------\n")

            for MAC, RSSI in Devices.items(): #For MAC and RSSI in devices
                #print(MAC + "\t")
                sumRssi = 0
                numberOfRssi = 0
                for value in RSSI:
                    sumRssi = sumRssi + value
                    numberOfRssi = numberOfRssi + 1
                Avg = sumRssi/numberOfRssi
                print(MAC + "\t" + "Avg. RSSI-Value: " + str(round(Avg,2)) + "\t" + str(RSSI))
                tempstring += str(MAC) + ";" + str(round(Avg,2)) + ","

        finally:
            Mutex.release()

        f = open("SnifferData.txt", "w")
        f.write(tempstring)
        f.close()
        print("------------------------------------------\n")

        time.sleep(5)


if __name__ == "__main__":
    main()
