import zmq
import json
import time
import os
import threading
from core.CRDT.List_CRDT import List_CRDT

class Server:

    def __init__(self, name, port,broker_ports, update_timer = 15, timeout = 100000):
            self.name = name
            self.online = False
            self.port = port
            self.address = f"tcp://localhost:{self.port}"
            self.update_timer = update_timer
            self.timeout = timeout
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.REP)
            self.repart_socket = self.context.socket(zmq.REQ)
            self.CRDTS = {}
            self.broker_ports = broker_ports

    def get_ring(self, ring):
        self.hashring = ring
        print(f"Hashring: {self.hashring}")

    def initialize_database(self, filepath):
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w") as file:
                json.dump({"lists": []}, file, indent=4)
                print(f"[{self.name}] - Database created at {filepath}.")
        else:
            print(f"Database already exists at {filepath}.")
    
    def update_files(self,lists_data):
        try:
            with open(f"./server_database/{self.name}/lists.json", "r+") as lists_file:
                self.existing_data = json.load(lists_file)
                self.existing_data["lists"].extend(json.loads(lists_data)["lists"])
                lists_file.seek(0)
                json.dump(self.existing_data, lists_file, indent=4)
                for list in self.existing_data:
                    crdt = List_CRDT(list["id"],list["name"])
                    for item in list["items"]:
                        element = {"Item": item["Item"], "Quantity": item["Quantity"]}
                        crdt.add_item(element,-1)
                    self.CRDTS[crdt.list_id] = crdt

            return {"status": "success", "message": "Files updated successfully."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def create_list_on_server(self,list_data):
        try:
            with open(f"./server_database/{self.name}/lists.json", "r+") as lists_file:
                self.existing_data = json.load(lists_file)
                self.existing_data["lists"].append(list_data)
                lists_file.seek(0)
                crdt = List_CRDT(list_data["id"],list_data["name"])
                self.CRDTS[crdt.list_id] = crdt
                json.dump(self.existing_data, lists_file, indent=4)
            return {"status": "success", "message": f"List '{list_data['name']}' created successfully."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_list_on_server(self,list_id, list_data,operation,mod):
        try:
            list_found = False
            with open(f"./server_database/{self.name}/lists.json", "r+") as lists_file:
                existing_data = json.load(lists_file)
                for i, lst in enumerate(existing_data["lists"]):
                    if lst["id"] == list_id:
                        list_found = True
                        #dupe = existing_data["lists"][i]
                        #print(f"Dupe - {dupe}")
                        existing_data["lists"][i] = list_data
                        
                        for item in list_data.get("items", []):
                            print(f"Processing item {item}")  
                            element = (item["Item"],mod["Quantity"])

                            if operation == "add":
                                if(item["Item"] == mod["Item"]):
                                    print(f"Adding item {element}")
                                    if self.CRDTS[list_id].items.exist(element):  
                                        self.CRDTS[list_id].add_item(element, self.CRDTS[list_id].timestamp)
                                    else:
                                        self.CRDTS[list_id].add(element)
                            elif operation == "remove":
                                if(item["Item"] == mod["Item"]):
                                    print(f"Removing item {element}")
                                    """
                                    print(f"Dupe:{dupe["items"][item["Item"]]}")
                                    difference = dupe["items"][item["Item"]]["Quantity"]
                                    print(f"Difference:{difference}")
                                    eff = difference - item["quantity"]
                                    print(f"Eff Difference: {eff}")
                                    element = (item["Item"],eff)
                                    print(f"Element:{element}")
                                    """
                                    self.CRDTS[list_id].remove_item(element, self.CRDTS[list_id].timestamp)
                            else:
                                raise KeyError("Operation must be 'add' or 'remove'.")
                        break
                    else:
                        existing_data["lists"].append(list_data)

                #if(list_found == False):
                    #response = self.request_list_from_server(list_id)
                    #if(response.get("status") == "success"):
                        #data = response.get("list_data")
                        #print(data)
                lists_file.seek(0)
                lists_file.truncate()
                #json.dump(existing_data, lists_file, indent=4)
                self.save_crdts_to_file(f"./server_database/{self.name}/lists.json")
                self.save_crdts_to_file(f"crdts.json")
            return {"status": "success", "message": f"List with ID '{list_id}' updated successfully."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    def save_crdts_to_file(self,file_path):
        try:
            crdt_data = {"lists": []}

            for crdt_id, crdt in self.CRDTS.items():
                crdt_data["lists"].append({
                    "id": crdt.list_id,
                    "name": crdt.list_name,
                    "items": crdt.get_list()  
                })

            with open(file_path, "w") as file:
                json.dump(crdt_data, file, indent=4)

            print(f"CRDTs saved to {file_path}")
        except Exception as e:
            print(f"Error saving CRDTs: {e}")

    def remove_item_from_list(self,list_id, item, purchased):
        self.CRDTS[list_id].remove(item, purchased)

    def get_list(self,list_id):
        list_found = False
        print(f"{self.name} - Getting List {list_id}!")
        try:
            with open(f"./server_database/{self.name}/lists.json", "r+") as lists_file:
                existing_data = json.load(lists_file)
                for i, lst in enumerate(existing_data["lists"]):
                    if lst["id"] == list_id:
                        list_found = True
                        return {"status": "success","list_id": list_id, "list_data": lst}
                    
                if (list_found == False):
                    response = self.request_list_from_server(self,list_id)
                    return response
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def request_list_from_server(self, list_id):
        self_key = self.hashring.hash(self.name)
        sorted_keys = self.hashring.sorted_keys
        next_key = -1;
        i = 0
        for key in sorted_keys:
            if(key == self_key):
                next_key = sorted_keys[i+1]
                break
        
        if next_key != -1:
            next_server = self.hashring.get_server(next_key)
            server_addr = next_server.address
            request = {"action": "request_list", "list_id": list_id}
            self.repart_socket.connect(server_addr)
            self.repart_socket.send_json(request)
            response = self.repart_socket.recv_json()
            if(response.get("status") == "success"):
                print(f"[{self.name}] - List with id {list_id} found!\n")
                list_data = response.get("list_data")
                return {"status": "success", "list_id": list_id, "list_data": list_data}
            
        return {"status": "error", "message": f"List with id {list_id} not found."}

    def run(self):
        print(f"[{self.name}] - Running Server")
        self.connect()
        self.online = True
        try:
            self.connected_clients = []
            # Start the thread to print connected clients
            threading.Thread(target=self.print_connected_clients, daemon=True).start()
            self.initialize_database(f"./server_database/{self.name}/lists.json")
            while(True):
                if self.socket.poll(timeout=self.timeout):
                    request = self.socket.recv_json()
                    response = self.handle_request(request)
                    self.socket.send_json(response)
                else:
                    time.sleep(1)  
        except Exception as e:
            if(Exception is KeyboardInterrupt):
                print("Server is shutting down...")
            else:
                print(e)
        finally:
            self.disconnect()
            self.online = False
            self.socket.close()
            self.context.term()

    def connect(self):
        self.socket.connect(self.address)
        for port in self.broker_ports:
            self.repart_socket.connect(f"tcp://localhost:{port}")

        print(f"[{self.name}] : Listening on port {self.port}")

    def disconnect(self):
        self.socket.disconnect(self.address)
        for port in self.broker_ports:
            self.repart_socket.disconnect(f"tcp://localhost:{port}")

        print(f"[{self.name}] : Disconnected from port {self.port}")
        

    def handle_request(self,request):
        action = request.get("action")

        if action == "ping":
            return {"status": "success", "message": "Server is alive"}
        elif action == "register_client":
            client_name = request.get("client_name")
            if client_name not in self.connected_clients:
                self.connected_clients.append(client_name)
                response = {"status": "success", "message": f"Client '{client_name}' registered successfully."}
            else:
                response = {"status": "error", "message": f"Client '{client_name}' is already registered."}
        elif action == "disconnect_client":
            client_name = request.get("client_name")
            if client_name in self.connected_clients:
                self.connected_clients.remove(client_name)
                response = {"status": "success", "message": f"Client '{client_name}' disconnected successfully."}
            else:
                response = {"status": "error", "message": f"Client '{client_name}' is not registered."}
        elif action == "remove_list":
            list_name = request.get("list_name")
            response = self.remove_list_from_server(list_name)
        elif action == "create_list":
            list_data = request.get("list_data")
            response = self.create_list_on_server(list_data)
        elif action == "update_list":
            operation = request.get("operation")
            list_id = request.get("list_id")
            list_data = request.get("list_data")
            mod = request.get("mod")
            response = self.update_list_on_server(list_id, list_data, operation,mod)
            #self.propagate_updates(list_data,list_id)
        elif action == "join_list":
            list_id = request.get("list_id")
            response = self.join_list_on_server(list_id)
        elif action == "check_update":
            list_id = request.get("list_id")
            response = self.check_update_on_server(list_id)
        elif action == "get_ring":
            ring = request.get("ring")
            self.get_ring(ring)
        elif action == "request_list":
            list_id = request.get("list_id")
            response = self.get_list(list_id)
        else:
            response = {"status": "error", "message": "Invalid action. Please try again."}
        #print(f"[{self.name}] - Sending response: {response}")
        return response

    def check_update_on_server(self,list_id):
        try:
            with open(f"./server_database/{self.name}/lists.json", "r") as lists_file:
                self.existing_data = json.load(lists_file)
                for lst in self.existing_data["lists"]:
                    if lst["id"] == list_id:
                        return {"status": "success", "list_data": lst}
                return {"status": "error", "message": f"List with ID '{list_id}' not found."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def join_list_on_server(self,list_id):
        try:
            with open(f"./server_database/{self.name}/lists.json", "r") as lists_file:
                self.existing_data = json.load(lists_file)
                for lst in self.existing_data["lists"]:
                    if lst["id"] == list_id:
                        return {"status": "success", "list_data": lst}
                return {"status": "error", "message": f"List with ID '{list_id}' not found."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def remove_list_from_server(self,list_name):
        try:
            with open(f"./server_database/{self.name}/lists.json", "r+") as lists_file:
                self.existing_data = json.load(lists_file)
                self.existing_data["lists"] = [lst for lst in self.existing_data["lists"] if lst["name"] != list_name]
                lists_file.seek(0)
                lists_file.truncate()
                json.dump(self.existing_data, lists_file, indent=4)
            return {"status": "success", "message": f"List '{list_name}' removed successfully."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def print_connected_clients(self):
        while True:
            print(f"[{self.name}] - Connected clients: {self.connected_clients}")
            time.sleep(5)

    def merge_CRDTS(self,other_CRDTS):
        for CRDT in self.CRDTS:
            for other_CRDT in other_CRDTS:
                if CRDT.list_id == other_CRDT.list_id:
                    CRDT.merge(other_CRDT)
                elif other_CRDT.list_id not in self.CRDTS:
                    self.CRDTS[other_CRDT.list_id] = other_CRDT

    def send_CRDTS():
        raise NotImplemented("Not Implemented Yet!")

