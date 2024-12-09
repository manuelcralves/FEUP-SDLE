import json

items_file = "../client_database/items_details.json"
lists_file = "../client_database/lists.json"

def load_json(filepath):
    with open(filepath, "r") as file:
        return json.load(file)

def save_json(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

def get_items_in_list(list_id):
    lists_data = load_json(lists_file)
    for lst in lists_data["lists"]:
        if lst["id"] == list_id:
            return 0, lst["items"]
    return -1, f"List '{list_id}' not found."

def get_total_price_of_list(list_id):
    lists_data = load_json(lists_file)
    for lst in lists_data["lists"]:
        if lst["id"] == list_id:
            return 0, lst["total_price"]
    return -1, f"List '{list_id}' not found."

def get_item_price(item_id):
    items_data = load_json(items_file)
    item = next((item for item in items_data["items"] if item["id"] == item_id), None)
    if item:
        return 0, item["price"]
    return -1, f"Item '{item_id}' not found."

def get_item_stock(item_id):
    items_data = load_json(items_file)
    item = next((item for item in items_data["items"] if item["id"] == item_id), None)
    if item:
        return 0, item["stock"]
    return -1, f"Item '{item_id}' not found."

def add_item_to_list(list_id, item_id, quantity=1):
    if list_id < 1:
        return -1, f"List ID must be greater than or equal to 1."

    items_data = load_json(items_file)
    lists_data = load_json(lists_file)
    
    item = next((item for item in items_data["items"] if item["id"] == item_id), None)
    if item is None:
        return -1, f"Item '{item_id}' not found."

    if item["stock"] < quantity:
        return -1, f"Not enough stock for item '{item_id}'. Requested: {quantity}, Available: {item['stock']}."

    for lst in lists_data["lists"]:
        if lst["id"] == list_id:
            lst["items"].extend([item_id] * quantity)
            lst["total_price"] += item["price"] * quantity
            item["stock"] -= quantity
            save_json(lists_file, lists_data)
            save_json(items_file, items_data)
            return 0, f"{quantity} units of item '{item_id}' added to list '{list_id}'. Remaining stock: {item['stock']}."
    
    new_list = {
        "id": list_id,
        "items": [item_id] * quantity,
        "total_price": item["price"] * quantity
    }
    lists_data["lists"].append(new_list)
    item["stock"] -= quantity
    save_json(lists_file, lists_data)
    save_json(items_file, items_data)
    return 0, f"List '{list_id}' created and {quantity} units of item '{item_id}' added. Remaining stock: {item['stock']}."

def remove_item_from_list(list_id, item_id, quantity=1):
    if list_id < 1:
        return -1, f"List ID must be greater than or equal to 1."
    if item_id < 1:
        return -1, f"Item ID must be greater than or equal to 1."
    if quantity < 0:
        return -1, f"Quantity must be greater than or equal to 0."

    items_data = load_json(items_file)
    lists_data = load_json(lists_file)

    item = next((item for item in items_data["items"] if item["id"] == item_id), None)
    if item is None:
        return -1, f"Item '{item_id}' not found."

    for lst in lists_data["lists"]:
        if lst["id"] == list_id:
            count_in_list = lst["items"].count(item_id)
            if count_in_list >= quantity:
                for _ in range(quantity):
                    lst["items"].remove(item_id)
                lst["total_price"] -= item["price"] * quantity
                item["stock"] += quantity
                save_json(lists_file, lists_data)
                save_json(items_file, items_data)
                return 0, f"{quantity} units of item '{item_id}' removed from list '{list_id}'. Updated stock: {item['stock']}."
            else:
                return -1, f"Only {count_in_list} units of item '{item_id}' in list '{list_id}', cannot remove {quantity} units." 
    return -1, f"List '{list_id}' not found."

def remove_list(list_id):
    lists_data = load_json(lists_file)
    items_data = load_json(items_file)
    
    for lst in lists_data["lists"]:
        if lst["id"] == list_id:
            for item_id in lst["items"]:
                item = next((item for item in items_data["items"] if item["id"] == item_id), None)
                if item:
                    item["stock"] += 1
                    print(f"Stock for item '{item_id}' updated: {item['stock']}.")
            lists_data["lists"].remove(lst)
            save_json(lists_file, lists_data)
            save_json(items_file, items_data)
            return 0, f"List '{list_id}' removed successfully."
    return -1, f"List '{list_id}' not found."


def remove_list(list_id):
    lists_data = load_json(lists_file)
    items_data = load_json(items_file)
    
    for lst in lists_data["lists"]:
        if lst["id"] == list_id:
            for item_id in lst["items"]:
                item = next((item for item in items_data["items"] if item["id"] == item_id), None)
                if item:
                    item["stock"] += 1
                    print(f"Stock for item '{item_id}' updated: {item['stock']}.")
            lists_data["lists"].remove(lst)
            break
    else:
        return -1, f"List '{list_id}' not found."

    save_json(lists_file, lists_data)
    save_json(items_file, items_data)
    return 0, f"List '{list_id}' removed successfully."