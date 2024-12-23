import sys
import zmq

class Place:
    def __init__(self, zipcode, temperature_scale):
        self.zipcode = zipcode
        self.temperature_scale = temperature_scale
        self.total_temp = 0
        self.count = 0

# Define the places
nyc = Place("10001", "F")
opo = Place("4200", "C")
places = [nyc, opo]

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from weather server...")
socket.connect("tcp://localhost:5557")

# Subscribe to zipcodes
for place in places:
    socket.setsockopt_string(zmq.SUBSCRIBE, place.zipcode + " ")

# Process updates
update_nbr = 0
while places[0].count < 100 or places[1].count < 100:
    string = socket.recv_string()
    zipcode, temperature, relhumidity = string.split()
    print(f"Received: {string}")
    for place in places:
        if place.zipcode == zipcode and place.count < 100:
            place.total_temp += int(temperature)
            place.count += 1
    update_nbr += 1

print(f"Received {update_nbr} updates")

for place in places:
    if place.count > 0:
        avg_temp = place.total_temp / place.count
        print(f"Count {place.zipcode}: {place.count}")
        print(f"Average temperature for zipcode '{place.zipcode}' was {avg_temp:.1f}{place.temperature_scale}")

socket.close()
context.term()
