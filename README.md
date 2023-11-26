# Comm. Nets. Protocol Project
---
### Terminal-based messaging protocol.
*The only requirement is a sufficiently modern version of Python 3 installed.*
*Scripts have been tested in Python version 3.10.5.*

- A server instance **must** be started before any cient instance.
- Once a server instance is started, **two** client instances may be started. 

---
## Running The Server
The server facilitates a messanger-like text communication between two clients.

If hosting locally, server may be started without any modifications.
Otherwise, the server_addr tuple may be modified for your (ip, port).

Open a new instance of your preferred terminal.
Enter the following to start the server:
*Replace ```/your/file/directory/``` with the directory where your server & client files are stored.*
```
cd /your/file/directory/
python server.py
```
Input from clients and output from the server can be observed in the same terminal where the server was started.

---
## Running Clients
If server is hosted locally, clients may be started without any modifications.
Otherwise, the server_addr tuple may be modified for the server's (ip, port) accordingly.

Open a new instance of your preferred terminal.
Enter the following to start a client:
*Replace ```/your/file/directory/``` with the directory where your server & client files are stored.*
```
cd /your/file/directory/
python client.py
```
*Repeat in a seperate terminal to start another instance.*
Clients will immediately attempt to connect to the server.
Once two clients have connected to the server, either client can enter a message into their repective terminal.
Likewise, messages received will appear in each client's respective terminal.

**Note:** Due to limitations of single-threaded terminal interactions with python, messages sent by the server do not get handled until terminal input (sending a message) completes.