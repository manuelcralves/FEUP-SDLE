import zmq
import json
import time
import os
import threading
from core.CRDT.List_CRDT import List_CRDT

CRDTS = {}

def initialize_database(filepath):
    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as file:
            json.dump({"lists": []}, file, indent=4)
            print(f"Database created at {filepath}.")
    else:
        print(f"Database already exists at {filepath}.")

def update_files(lists_data):
    try:
        with open("../server_database/lists.json", "r+") as lists_file:
            existing_data = json.load(lists_file)
            existing_data["lists"].extend(json.loads(lists_data)["lists"])
            lists_file.seek(0)
            json.dump(existing_data, lists_file, indent=4)
            for list in existing_data:
                crdt = List_CRDT(list["id"])
                for item in list["items"]:
                    element = {"Item": item["Item"], "Quantity": item["Quantity"]}
                    crdt.add_item(element,-1)
                CRDTS[crdt.list_id] = crdt
        return {"status": "success", "message": "Files updated successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

"""
Utilize current CRDT state to update the Local Database
"""
def update_from_CRDT():
    not NotImplemented("Not Implemented Yet!")

def save_crdts_to_file(file_path):

    try:
        crdt_data = {"lists": []}

        for crdt_id, crdt in CRDTS.items():
            crdt_data["lists"].append({
                "id": crdt.list_id,
                "items": crdt.get_list()  
            })

        with open(file_path, "w") as file:
            json.dump(crdt_data, file, indent=4)

        print(f"CRDTs saved to {file_path}")
    except Exception as e:
        print(f"Error saving CRDTs: {e}")


def create_list_on_server(list_data):
    try:
        with open("../server_database/lists.json", "r+") as lists_file:
            existing_data = json.load(lists_file)
            existing_data["lists"].append(list_data)
            lists_file.seek(0)
            crdt = List_CRDT(list_data["id"])
            CRDTS[crdt.list_id] = crdt
            json.dump(existing_data, lists_file, indent=4)
        return {"status": "success", "message": f"List '{list_data['name']}' created successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

def update_list_on_server(list_id, list_data, operation):
    print(f"Update list {list_id} with data {list_data} and operation {operation}")
    try:
        with open("../server_database/lists.json", "r+") as lists_file:
            existing_data = json.load(lists_file)
            print(f"Existing data: {existing_data}")
            
            for i, lst in enumerate(existing_data["lists"]):
                print(f"Check list {lst['id']}")
                if lst["id"] == list_id:
                    existing_data["lists"][i] = list_data
                    print(f"Updated data: {existing_data}")

                    for item in list_data.get("items", []):
                        print(f"Processing item {item}")
                        hashable_item = tuple(sorted(item.items()))  

                        if operation == "add":
                            print(f"Adding item {hashable_item}")
                            if CRDTS[list_id].items.exist(hashable_item):  
                                CRDTS[list_id].add_item(item, CRDTS[list_id].timestamp)
                            else:
                                CRDTS[list_id].add(item)
                        elif operation == "remove":
                            print(f"Removing item {hashable_item}")
                            CRDTS[list_id].remove_item(item, CRDTS[list_id].timestamp)
                        else:
                            raise KeyError("Operation must be 'add' or 'remove'.")
                        
                    

                    break
            else:

                existing_data["lists"].append(list_data)

            lists_file.seek(0)
            lists_file.truncate()
            json.dump(existing_data, lists_file, indent=4)
            save_crdts_to_file("crdts.json")

        return {"status": "success", "message": f"List with ID '{list_id}' updated successfully."}
    except Exception as e:
        print(f"Error updating list: {e}")
        return {"status": "error", "message": str(e)}

    
def remove_item_from_list(list_id, item, purchased):
    CRDTS[list_id].remove(item, purchased)

connected_clients = []

def handle_request(request):
    action = request.get("action")

    if action == "ping":
        return {"status": "success", "message": "Server is alive"}
    elif action == "register_client":
        client_name = request.get("client_name")
        if client_name not in connected_clients:
            connected_clients.append(client_name)
            response = {"status": "success", "message": f"Client '{client_name}' registered successfully."}
        else:
            response = {"status": "error", "message": f"Client '{client_name}' is already registered."}
    elif action == "disconnect_client":
        client_name = request.get("client_name")
        if client_name in connected_clients:
            connected_clients.remove(client_name)
            response = {"status": "success", "message": f"Client '{client_name}' disconnected successfully."}
        else:
            response = {"status": "error", "message": f"Client '{client_name}' is not registered."}
    elif action == "remove_list":
        list_name = request.get("list_name")
        response = remove_list_from_server(list_name)
    elif action == "create_list":
        list_data = request.get("list_data")
        response = create_list_on_server(list_data)
    elif action == "update_list":
        operation = request.get("operation")
        list_id = request.get("list_id")
        list_data = request.get("list_data")
        print("Update list...")
        response = update_list_on_server(list_id, list_data, operation)
    elif action == "join_list":
        list_id = request.get("list_id")
        response = join_list_on_server(list_id)
    elif action == "check_update":
        list_id = request.get("list_id")
        response = check_update_on_server(list_id)
    else:
        response = {"status": "error", "message": "Invalid action. Please try again."}

    #print(f"Sending response: {response}")
    return response

def check_update_on_server(list_id):
    try:
        with open("../server_database/lists.json", "r") as lists_file:
            existing_data = json.load(lists_file)
            for lst in existing_data["lists"]:
                if lst["id"] == list_id:
                    return {"status": "success", "list_data": lst}
            return {"status": "error", "message": f"List with ID '{list_id}' not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def join_list_on_server(list_id):
    try:
        with open("../server_database/lists.json", "r") as lists_file:
            existing_data = json.load(lists_file)
            for lst in existing_data["lists"]:
                if lst["id"] == list_id:
                    return {"status": "success", "list_data": lst}
            return {"status": "error", "message": f"List with ID '{list_id}' not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def remove_list_from_server(list_name):
    try:
        with open("../server_database/lists.json", "r+") as lists_file:
            existing_data = json.load(lists_file)
            existing_data["lists"] = [lst for lst in existing_data["lists"] if lst["name"] != list_name]
            lists_file.seek(0)
            lists_file.truncate()
            json.dump(existing_data, lists_file, indent=4)
        return {"status": "success", "message": f"List '{list_name}' removed successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def print_connected_clients():
    while True:
        print(f"Connected clients: {connected_clients}")
        time.sleep(5)

def merge_CRDTS(other_CRDTS):
    for CRDT in CRDTS:
        for other_CRDT in other_CRDTS:
            if CRDT.list_id == other_CRDT.list_id:
                CRDT.merge(other_CRDT)
            elif other_CRDT.list_id not in CRDTS:
                CRDTS[other_CRDT.list_id] = other_CRDT

def send_CRDTS():
    raise NotImplemented("Not Implemented Yet!")

initialize_database("../server_database/lists.json")

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://localhost:5556")

# Start the thread to print connected clients
threading.Thread(target=print_connected_clients, daemon=True).start()

try:
    while True:
        if socket.poll(timeout=1000):  
            request = socket.recv_json()
            response = handle_request(request)
            socket.send_json(response)
        else:
            time.sleep(1)  
except KeyboardInterrupt:
    print("Server is shutting down...")
finally:
    socket.close()
    context.term()