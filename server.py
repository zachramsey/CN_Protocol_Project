import socket
import struct


def send_ack(client_socket):
    # Pack the message with header fields
    acknowledgment = "Handshake received"
    message = struct.pack('!4sHH', b'ACK', len(acknowledgment),
                          calculate_checksum(acknowledgment)) + acknowledgment.encode('utf-8')
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
        print("Client failed to connect")
        return None  # Handle checksum verification failure


def calculate_checksum(data):
    # Calculate the checksum by summing ASCII values of characters
    checksum = sum(ord(char) for char in data)
    return checksum & 0xFFFF  # Keep it within a 16-bit range


def receive_data(client_socket):
    # Receive the message header
    header = client_socket.recv(8)
    message_type, length, checksum = struct.unpack('!4sHH', header)

    # Receive the message content based on the length
    data = b""
    while len(data) < length:
        chunk = client_socket.recv(length - len(data))
        if not chunk:
            break
        data += chunk

    # Verify the checksum
    if checksum == calculate_checksum(data.decode('utf-8')):
        # Send a confirmation back to the client
        confirmation_message = "Message received by the server."
        client_socket.sendall(confirmation_message.encode('utf-8'))
        return data.decode('utf-8')

    else:
        # Send a confirmation back to the client
        confirmation_message = "Message failed to send. Please retry."
        client_socket.sendall(confirmation_message.encode('utf-8'))
        return "Data corrupted."


def application_layer_handshake(client_socket):
    # Receive the handshake ("HELLO") message from the client
    ack_message = receive_hello(client_socket)

    if ack_message:
        print("Received ACK message from client:", ack_message)
        print("Connection established.")
        send_ack(client_socket)
        return True
    else:
        print("Failed to establish connection.")
        return False


# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 12345)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)


# Wait for a connection
client_socket, client_address = server_socket.accept()

handshake = False
while not handshake:
    # Perform the application layer handshake
    handshake = application_layer_handshake(client_socket)

# Handle the connection (e.g., receive and process messages)
data = receive_data(client_socket)
print("Received message from client:", data)

# Close the connection
client_socket.close()
