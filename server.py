import socket


def application_layer_handshake(client_socket):
    # Receive the client's "HELLO" message
    hello_message = client_socket.recv(1024).decode('utf-8')
    print("Received HELLO message from client:", hello_message)

    # Send an acknowledgment ("ACK") message back to the client
    ack_message = "ACK: Connection established."
    client_socket.sendall(ack_message.encode('utf-8'))
    print("Sent ACK message to client")


# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 12345)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)

while True:
    # Wait for a connection
    client_socket, client_address = server_socket.accept()

    # Perform the application layer handshake
    application_layer_handshake(client_socket)

    # Handle the connection (e.g., receive and process messages)
    data = client_socket.recv(1024)
    print("Received message from client:", data.decode('utf-8'))

    # Send a confirmation back to the client
    confirmation_message = "Message received by the server."
    client_socket.sendall(confirmation_message.encode('utf-8'))

    # Close the connection
    client_socket.close()
