import zmq
import json
import read_lists_items

def handle_request(request):
    action = request.get("action")
    list_id = request.get("list_id")
    item_id = request.get("item_id")

    try:
        if action == "add_item":
            result = read_lists_items.add_item_to_list(list_id, item_id)
            return {"status": "success", "message": f"Item {item_id} was successfully added to list {list_id}."} if not result else {"status": "error", "message": result}
        elif action == "remove_item":
            result = read_lists_items.remove_item_from_list(list_id, item_id)
            return {"status": "success", "message": f"Item {item_id} was successfully removed from list {list_id}."} if not result else {"status": "error", "message": result}
        elif action == "get_items":
            items = read_lists_items.get_items_in_list(list_id)
            if items:
                return {"status": "success", "message": f"Items in list {list_id}: {items}"}
            else:
                return {"status": "error", "message": f"No items found in list {list_id}."}
        elif action == "get_total_price":
            total_price = read_lists_items.get_total_price_of_list(list_id)
            return {"status": "success", "message": f"The total price of list {list_id} is ${total_price:.2f}."}
        else:
            return {"status": "error", "message": "Invalid action. Please try again."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


context = zmq.Context()
socket = context.socket(zmq.REP)  
socket.connect("tcp://localhost:5556")  

while True:
    message = socket.recv_json()  
    #print("Server received:", message)
    response = handle_request(message)  
    socket.send_json(response)  
