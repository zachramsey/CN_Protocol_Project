import socket
import struct
import selectors
import types

server_addr = ("localhost", 12345)
sel = selectors.DefaultSelector()


''' Sum ASCII values of character in data; return the 16-bit checksum '''
def calc_checksum(data): return sum(ord(char) for char in data) & 0xFFFF


''' Receive data '''
def receive(socket):
    data = socket.recv(1024)
    b_checksum = data[:2]
    checksum = struct.unpack('!H', b_checksum)[0]
    signal = data[2:5].decode()
    msg = data[5:].decode()
    if checksum == calc_checksum(signal + msg): return (signal, msg, data)   # Return signal and message if checksum passes
    return False                                            # Otherwise, indicate corrupted message


''' Transmit data '''
def transmit(socket, signal, msg):
    checksum = calc_checksum(signal + msg)
    b_checksum = struct.pack('!H', checksum)
    data = b_checksum + signal.encode() + msg.encode()
    socket.send(data)


''' Application-layer handshake '''
def handshake(server):
    socket, addr = server.accept()
    print("Server: Accepted client connection. Shaking hands...")

    signal, msg, _ = receive(socket)
    print(f"Client ({addr[0]}:{addr[1]}): [{signal}] {msg}")
    if signal == "REQ":
        socket.setblocking(False)
        data = types.SimpleNamespace(addr=addr, last=b"", inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(socket, events, data=data)

        print(f"Server: Sending [RAK] to ({data.addr[0]}:{data.addr[1]})")
        transmit(socket, "RAK", "")
        print(f"Server: Shook hands with ({addr[0]}:{addr[1]})\n")
    else:
        print("Server: Expected just [REQ], closing socket...\n")
        socket.close()


''' Handle client communication '''
def handle_client(key, mask):
    socket = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        received = receive(socket)
        if received:
            signal, msg, raw_data = received
            print(f"Client ({data.addr[0]}:{data.addr[1]}): [{signal}] {msg}")
            if signal == "MSG":
                for r_key, _ in events:
                    if r_key.data.addr != data.addr:
                        r_key.data.outb += raw_data
                        r_key.data.last = b""
                        r_key.data.last += raw_data
            elif signal == "NAK":
                data.outb += data.last
        else:
            print(f"Client ({data.addr[0]}:{data.addr[1]}) has disconnected.")
            sel.unregister(socket)
            socket.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Server: Echoing {repr(data.outb)} to ({data.addr[0]}:{data.addr[1]})")
            data_len = socket.send(data.outb)
            data.outb = data.outb[data_len:]


''' ------------------------ MAIN ------------------------ '''

print("-------------------------\n")
print("Opening socket...")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # Create a socket object
server.bind(server_addr)             # Bind socket to address & port
server.listen()                                 # Listen for incoming connections
print(f"Listening on {server_addr[0]}:{server_addr[1]}...\n")
server.setblocking(False)                       # Set socket to non-blocking mode
sel.register(server, selectors.EVENT_READ, data=None)  # Register server socket with selector

try:
    print("-------------------------")
    print("| Beginning of Exchange |")
    print("-------------------------\n")
    while True:
        events = sel.select(timeout=None)       # Wait for events
        for key, mask in events:
            if key.data is None:
                handshake(key.fileobj)
            else:
                handle_client(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting...")
except Exception as e:
    print(f"An exception occured: {e}\nClosing server...")
finally:
    sel.close()
    server.close()
    print("Server stopped.")
    exit()
