import zmq
import json
import time
import os

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
        return {"status": "success", "message": "Files updated successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_list_on_server(list_data):
    try:
        with open("../server_database/lists.json", "r+") as lists_file:
            existing_data = json.load(lists_file)
            existing_data["lists"].append(list_data)
            lists_file.seek(0)
            json.dump(existing_data, lists_file, indent=4)
        return {"status": "success", "message": f"List '{list_data['name']}' created successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_list_on_server(list_id, list_data):
    try:
        with open("../server_database/lists.json", "r+") as lists_file:
            existing_data = json.load(lists_file)
            for i, lst in enumerate(existing_data["lists"]):
                if lst["id"] == list_id:
                    existing_data["lists"][i] = list_data
                    break
            else:
                existing_data["lists"].append(list_data)
            lists_file.seek(0)
            lists_file.truncate()
            json.dump(existing_data, lists_file, indent=4)
        return {"status": "success", "message": f"List with ID '{list_id}' updated successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_request(request):
    action = request.get("action")

    if action == "remove_list":
        list_name = request.get("list_name")
        return remove_list_from_server(list_name)
    elif action == "create_list":
        list_data = request.get("list_data")
        return create_list_on_server(list_data)
    elif action == "update_list":
        list_id = request.get("list_id")
        list_data = request.get("list_data")
        return update_list_on_server(list_id, list_data)
    else:
        return {"status": "error", "message": "Invalid action. Please try again."}

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

initialize_database("../server_database/lists.json")

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://localhost:5556")

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