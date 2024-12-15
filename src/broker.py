import zmq
from hashring import HashRing
from server import Server
import time
import threading

print("Building Server!")
server1 = Server("Server1","5556",["4000"])
#server2 = Server("Server2","5556",["4000"])


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

"""
def answer_request(request):
    while(True):
        print("Answering request!")
        action = request.get("action")
        if action == "ping":
                return {"status": "success", "message": "Broker is alive"}
        elif action == "fetch_list":
                list_id = request.get("list_id")
                for server in ring.servers:
                    print(f"Requesting List from: {server.name}\n")
                    req = {"action": "fetch_list", "list_id": list_id}
                    replication.send_json(req)
                    response = replication.recv_json()
                    print(f"Response from {server.name}: {response}\n\n")
                    if(response.get("status") == "success"):
                        list = response.get("list")
                        return {"status": "success", "list_data": list}
                    
        elif action == "update_list":
             list_id = request.get("list_id")
             list_data = request.get("list_data")
             for server in ring.servers:
                  req = {"action": "server_update", "list_data": list_data, "list_id": list_id}
                  replication.send_json(req)
"""
    
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