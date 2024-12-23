

#
#   Weather update server
#   Binds PUB socket to tcp://*:5556
#   Publishes random weather updates
#

import zmq
from random import randrange
import sys

# Check for port argument
if len(sys.argv) != 2:
    print("Usage: python pub.py <port>")
    sys.exit(1)

port = sys.argv[1]
bind_address = f"tcp://*:{port}"

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(bind_address)

while True:
    zipcode = randrange(1, 100000)
    temperature = randrange(-80, 135)
    relhumidity = randrange(10, 60)

    socket.send_string(f"{zipcode} {temperature} {relhumidity}")

