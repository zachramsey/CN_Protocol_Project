import socket
import struct

server_addr = ("localhost", 12345)
last_msg = ""


''' Sum ASCII values of character in data; return the 16-bit checksum '''
def calc_checksum(data):
    return sum(ord(char) for char in data) & 0xFFFF


''' Receive data '''
def receive(socket):
    data = socket.recv(1024)
    b_checksum = data[:2]
    checksum = struct.unpack('!H', b_checksum)[0]
    status = data[2:5].decode()
    msg = data[5:].decode()
    if checksum == calc_checksum(status + msg): return (status, msg)    # Return status and message if checksum passes
    return False                                                        # Otherwise, indicate corrupted message


''' Transmit data '''
def transmit(socket, status, msg):
    checksum = calc_checksum(status + msg)
    b_checksum = struct.pack('!H', checksum)
    data = b_checksum + status.encode() + msg.encode()
    socket.sendall(data)


''' Application-layer handshake '''
def handshake(socket):
    print("Requesting connection...")
    transmit(socket, "REQ", "")           # Request connection
    print("Waiting for request acknowledgement...")
    status, _ = receive(socket)             # Receive response
    if not status:
        print("Failed to establish connection.\n")
        return False
    elif status == "RAK":
        print("Successfully established connection.\n")
        return True


''' ------------------------ MAIN ------------------------ '''

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
client.connect(server_addr)                                 # Connect to server

try:
    if handshake(client):                                   # Perform handshake
        print("--------------------------------------------")
        print("| Enter a message or press Ctrl+C to exit. |")
        print("--------------------------------------------\n")
        while True:
            user_input = input("")            # Get user input
            if user_input: transmit(client, "MSG", user_input) # Send message to server

            status, msg = receive(client)                   # Receive message from server
            if status:
                if status == "MSG": print("Received: " + msg) # Otherwise, print message
                elif status == "NAK":                           # If NAK, resend last message
                    print("NAK received, resending last message...")
                    transmit(client, "MSG", last_msg)
            else:
                print("Something went wrong, closing connection...")
                break
            
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting...")
finally:
    client.close()