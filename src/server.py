import zmq
import json
import time

def update_files(items_data, lists_data):
    try:
        with open("../server_database/items_details.json", "w") as items_file:
            items_file.write(items_data)
        with open("../server_database/lists.json", "w") as lists_file:
            lists_file.write(lists_data)
        return {"status": "success", "message": "Files updated successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_request(request):
    action = request.get("action")

    if action == "update_files":
        items_data = request.get("items_data")
        lists_data = request.get("lists_data")
        return update_files(items_data, lists_data)
    else:
        return {"status": "error", "message": "Invalid action. Please try again."}

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://localhost:5556")

try:
    while True:
        if socket.poll(timeout=1000):  
            message = socket.recv_json()
            response = handle_request(message)
            socket.send_json(response)
        else:
            time.sleep(1)  
except KeyboardInterrupt:
    print("Server is shutting down...")
finally:
    socket.close()
    context.term()