import zmq
from hashring import HashRing
from server import Server
import time
import threading

print("Building Server!")
server1 = Server("Server1","5556",["4000"])
server2 = Server("Server2","5557",["4000"])


servers = [server1,server2]
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
for server in servers:
    backend.bind(server.address)

replication = context.socket(zmq.DEALER)
replication.bind("tcp://localhost:4000")

def answer_request(request):
    while(True):
        action = request.get("action")
        if action == "ping":
                return {"status": "success", "message": "Broker is alive"}
        elif action == "fetch_list":
                list_id = request.get("list_id")
                for server in ring.servers:
                    request = {"action": "fetch_list", "list_id": list_id}
                    replication.send_json(request)
                    response = replication.recv_json()
                    if(response.get("status") == "success"):
                        list = response.get("list")
                        break

                if(list != None):
                    return {"status": "success", "list_data": list}
        elif action == "update_list":
             list_id = request.get("list_id")
             list_data = request.get("list_data")
             for server in ring.servers:
                  request = {"action": "server_update", "list_data": list_data, "list_id": list_id}
                  replication.send_json(request)
        
    
try:
    zmq.proxy(frontend, backend)
    threading.Thread(target=answer_request, daemon=True)
except KeyboardInterrupt:
    print("Broker is shutting down...")
finally:
    frontend.close()
    backend.close()
    context.term()