import socket
import struct


def send_data(client_socket, data):
    message = struct.pack('!4sHH', b'DATA', len(data), calculate_checksum(data)) + data.encode('utf-8')
    client_socket.sendall(message)


def send_ack(client_socket, acknowledgment):
    message = struct.pack('!4sHH', b'ACK', len(acknowledgment),
                          calculate_checksum(acknowledgment)) + acknowledgment.encode('utf-8')
    client_socket.sendall(message)


def send_hello(client_socket):
    hello_message = "HELLO: Establish connection request."
    message = struct.pack('!4sHH', b'HELLO', len(hello_message),
                          calculate_checksum(hello_message)) + hello_message.encode('utf-8')
    client_socket.sendall(message)


def receive_hello(client_socket):
    # Receive the handshake message header
    header = client_socket.recv(8)
    message_type, length, checksum = struct.unpack('!4sHH', header)

    # Receive the handshake message content based on the length
    hello_message = client_socket.recv(length).decode('utf-8')

    # Verify the checksum
    if checksum == calculate_checksum(hello_message):
        return hello_message
    else:
        return None  # Handle checksum verification failure


def calculate_checksum(data):
    # Calculate the checksum by summing ASCII values of characters
    checksum = sum(ord(char) for char in data)
    return checksum & 0xFFFF  # Keep it within a 16-bit range


# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 12345)
client_socket.connect(server_address)

handshake = False
while not handshake:
    # Perform the application layer handshake
    send_hello(client_socket)

    # Receive the acknowledgment ("ACK") message from the server
    ack_message = receive_hello(client_socket)

    if ack_message:
        print("Received ACK message from server:", ack_message)
        print("Connection established.")
        handshake = True
    else:
        print("Failed to establish connection.")


# Send a message to server
message_to_server = input("Enter your message: ")
send_data(client_socket, message_to_server)

# Receive and print the confirmation from the server
confirmation_message = client_socket.recv(1024).decode('utf-8')
print("Server confirmation:", confirmation_message)

# Close the connection
client_socket.close()
