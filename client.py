import socket


def application_layer_handshake(client_socket):
    # Send a "HELLO" message to the server
    hello_message = "HELLO: Establish connection request."
    client_socket.sendall(hello_message.encode('utf-8'))
    print("Sent HELLO message to server")

    # Receive the acknowledgment ("ACK") message from the server
    ack_message = client_socket.recv(1024).decode('utf-8')
    print("Received ACK message from server:", ack_message)


# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 12345)
client_socket.connect(server_address)

# Perform the application layer handshake
application_layer_handshake(client_socket)

# Send a message to the server
message = "Hello, server! This is a message."
client_socket.sendall(message.encode('utf-8'))

# Receive and print the confirmation from the server
confirmation = client_socket.recv(1024)
print("Server confirmation:", confirmation.decode('utf-8'))

# Close the connection
client_socket.close()
