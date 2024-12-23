import sys
import time
import zmq

# Check for port argument
if len(sys.argv) != 2:
    print("Usage: python server2.py <port>")
    sys.exit(1)

port = sys.argv[1]
bind_address = f"tcp://*:{port}"

# Socket to talk to clients
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(bind_address)

while True:
    # Receive message
    message = socket.recv_string()
    print(f"Received {message}")

    # Simulate work with a delay of 1 second
    time.sleep(1)

    # Send response
    socket.send_string("World")
