from mac_vendor_lookup import MacLookup
import asyncio
import socket
from scapy.all import *
import pickle
import struct


class SocketServer():
    def __init__(self, Devices: dict, Mutex: asyncio.Lock):
        # IP taken from ifconfig on RPI
        self.IP = '172.20.10.9'
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.devices = Devices
        self.mut = Mutex

    def run(self):
        print("Running SocketServer")
        self.setup()

        while True:
            # accept connections from outside
            (clientsocket, address) = self.serversocket.accept()
            print("Accepted socket!!")

            Received = self.receive(clientsocket)
            print(f"Received is: {Received}")

            if Received == "GET":
                self.mut.acquire()
                try:
                    data = self.devices
                finally:
                    self.mut.release()
                self.send(data, clientsocket)



    def setup(self):
        # Bind socket to public host at port 80 (HTTP)
        self.serversocket.bind((self.IP, 80))
        print(f"hosting on {self.IP}")
        # Wait for connection
        self.serversocket.listen(5)

    def receive(self, sock):
        payload_size = struct.calcsize(">L")
        data = b""
        # Get size of data transmission
        while len(data) < payload_size:
            data += sock.recv(4096)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]

        # Unpack buffer "packed_msg_size" according to format ">L" (> = big-endian, L = unsigned long)
        # This gets the message size
        msg_size = struct.unpack(">L", packed_msg_size)[0]

        while len(data) < msg_size:
            data += sock.recv(4096)

        # Extract the raw data from the transmission. Ie. Cutoff unnecessary data at the end
        data = data[:msg_size]
        data = pickle.loads(data, fix_imports=True, encoding="bytes")
        return data

    def send(self, data, receivingsocket):
        data = pickle.dumps(data)
        size = len(data)

        receivingsocket.sendall(data)
