

#
#   Weather update client
#   Connects SUB socket to tcp://localhost:5556
#   Collects weather updates and finds avg temp in zipcode
#

import sys
import zmq


#  Socket to talk to server
context = zmq.Context()
subscriber_us = context.socket(zmq.SUB)
subscriber_pt = context.socket(zmq.SUB)

print("Collecting updates from weather server...")
subscriber_us.connect("tcp://localhost:5556")
subscriber_pt.connect("tcp://localhost:5557")

# Subscribe to zipcode, default is NYC, 10001
filter_us = "10001 "
filter_pt = "4200 "

subscriber_us.setsockopt_string(zmq.SUBSCRIBE, filter_us)
subscriber_pt.setsockopt_string(zmq.SUBSCRIBE, filter_pt)

# Initialize poll set
poller = zmq.Poller()
poller.register(subscriber_us, zmq.POLLIN)
poller.register(subscriber_pt, zmq.POLLIN)

total_temp_us = 0
total_temp_pt = 0
count_us = 0
count_pt = 0

# Collect 100 updates from each source
while count_us < 100 or count_pt < 100:
    socks = dict(poller.poll())

    # Check if a message is available from the U.S. subscriber
    if subscriber_us in socks and count_us < 100:
        message = subscriber_us.recv_string()
        zipcode, temperature, relhumidity = message.split()
        total_temp_us += int(temperature)
        count_us += 1
        print(f"U.S. Received: {zipcode} {temperature} {relhumidity}")

    # Check if a message is available from the Portugal subscriber
    if subscriber_pt in socks and count_pt < 100:
        message = subscriber_pt.recv_string()
        zipcode, temperature, relhumidity = message.split()
        total_temp_pt += int(temperature)
        count_pt += 1
        print(f"Portugal Received: {zipcode} {temperature} {relhumidity}")

# Calculate and print the average for each location
print(f"Average temperature for U.S. is {total_temp_us / count_us}")
print(f"Average temperature for Portugal is {total_temp_pt / count_pt}")

