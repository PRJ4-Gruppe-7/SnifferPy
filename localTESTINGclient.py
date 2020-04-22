import socket
import struct
import pickle

def receive(sock):
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

def send(data, receivingsocket):
    data = pickle.dumps(data)
    size = len(data)


    receivingsocket.sendall(struct.pack(">L", size) + data)


# create an INET, STREAMing socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# now connect to the web server on port 80 - the normal http port
socket.connect(('172.20.10.9', 80))
print("connected")

send("GET",socket)
print("Message sent")

rec = receive(socket)
for MAC, RSSI in rec.items():
    print(MAC, str(RSSI))
