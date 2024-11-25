import zmq
import json
from read_lists_items import add_item_to_list, remove_item_from_list, get_items_in_list, get_total_price_of_list

def handle_request(request):
    action = request.get("action")
    list_id = request.get("list_id")
    item_id = request.get("item_id")

    if action == "add_item":
        add_item_to_list(list_id, item_id)
        return {"status": "success", "message": f"Item {item_id} added to list {list_id}."}
    elif action == "remove_item":
        remove_item_from_list(list_id, item_id)
        return {"status": "success", "message": f"Item {item_id} removed from list {list_id}."}
    elif action == "get_items":
        items = get_items_in_list(list_id)
        return {"status": "success", "items": items}
    elif action == "get_total_price":
        total_price = get_total_price_of_list(list_id)
        return {"status": "success", "total_price": total_price}
    else:
        return {"status": "error", "message": "Invalid action."}

context = zmq.Context()
socket = context.socket(zmq.REP)  
socket.connect("tcp://localhost:5556")  

while True:
    message = socket.recv_json()  
    print("Server received:", message)
    response = handle_request(message)  
    socket.send_json(response)  
