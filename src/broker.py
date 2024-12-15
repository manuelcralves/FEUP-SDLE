import zmq
from hashring import HashRing
from server import Server
import time
import threading

print("Building Server!")
server1 = Server("Server1","5556",["4000"])
server2 = Server("Server2","5556",["4000"])


servers = [server1]
ring = HashRing(servers)
for server in servers:
    server_thread = threading.Thread(target=server.run, daemon=True)
    server_thread.start()

while(server.online == False):
    time.sleep(1)
context = zmq.Context()

frontend = context.socket(zmq.ROUTER)
frontend.bind("tcp://*:5555")

backend = context.socket(zmq.DEALER)
backend.bind("tcp://*:5556")

replication = context.socket(zmq.DEALER)
replication.bind("tcp://localhost:4000")
request = {"action": "get_ring", "ring": ring}
for server in servers:
    server.get_ring(ring)

try:
    #print("Got here!")
    #threading.Thread(target=answer_request, daemon=True)
    zmq.proxy(frontend, backend)
except KeyboardInterrupt:
    print("Broker is shutting down...")
finally:
    frontend.close()
    backend.close()
    context.term()