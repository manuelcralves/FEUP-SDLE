import json

items_file = "items_details.json"
lists_file = "lists.json"

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
            return lst["items"]
    print(f"Error: List '{list_id}' not found.")
    return []

def get_total_price_of_list(list_id):
    lists_data = load_json(lists_file)
    for lst in lists_data["lists"]:
        if lst["id"] == list_id:
            return lst["total_price"]
    print(f"Error: List '{list_id}' not found.")
    return 0.0

def get_item_price(item_id):
    items_data = load_json(items_file)
    item = next((item for item in items_data["items"] if item["id"] == item_id), None)
    if item:
        return item["price"]
    print(f"Error: Item '{item_id}' not found.")
    return 0.0

def get_item_stock(item_id):
    items_data = load_json(items_file)
    item = next((item for item in items_data["items"] if item["id"] == item_id), None)
    if item:
        return item["stock"]
    print(f"Error: Item '{item_id}' not found.")
    return 0

def add_item_to_list(list_id, item_id, quantity=1):
    items_data = load_json(items_file)
    lists_data = load_json(lists_file)
    
    item = next((item for item in items_data["items"] if item["id"] == item_id), None)
    if item is None:
        print(f"Error: Item '{item_id}' not found.")
        return -1

    if item["stock"] < quantity:
        print(f"Error: Not enough stock for item '{item_id}'. Requested: {quantity}, Available: {item['stock']}.")
        return -1

    for lst in lists_data["lists"]:
        if lst["id"] == list_id:
            lst["items"].extend([item_id] * quantity)
            lst["total_price"] += item["price"] * quantity
            item["stock"] -= quantity
            print(f"{quantity} units of item '{item_id}' added to list '{list_id}'. Remaining stock: {item['stock']}.")
            save_json(lists_file, lists_data)
            save_json(items_file, items_data)
            return 0
    
    new_list = {
        "id": list_id,
        "items": [item_id] * quantity,
        "total_price": item["price"] * quantity
    }
    lists_data["lists"].append(new_list)
    item["stock"] -= quantity
    print(f"List '{list_id}' created and {quantity} units of item '{item_id}' added. Remaining stock: {item['stock']}.")
    save_json(lists_file, lists_data)
    save_json(items_file, items_data)
    return 0

def remove_item_from_list(list_id, item_id, quantity=1):
    items_data = load_json(items_file)
    lists_data = load_json(lists_file)

    item = next((item for item in items_data["items"] if item["id"] == item_id), None)
    if item is None:
        print(f"Error: Item '{item_id}' not found.")
        return -1

    for lst in lists_data["lists"]:
        if lst["id"] == list_id:
            count_in_list = lst["items"].count(item_id)
            if count_in_list >= quantity:
                for _ in range(quantity):
                    lst["items"].remove(item_id)
                lst["total_price"] -= item["price"] * quantity
                item["stock"] += quantity
                print(f"{quantity} units of item '{item_id}' removed from list '{list_id}'. Updated stock: {item['stock']}.")
                save_json(lists_file, lists_data)
                save_json(items_file, items_data)
                return 0
            else:
                print(f"Error: Only {count_in_list} units of item '{item_id}' in list '{list_id}', cannot remove {quantity} units.")
                return -1
    
    print(f"Error: List '{list_id}' not found.")
    return -1

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
            print(f"List '{list_id}' removed successfully.")
            save_json(lists_file, lists_data)
            save_json(items_file, items_data)
            return 0
    
    print(f"Error: List '{list_id}' not found.")
    return -1


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
            print(f"List '{list_id}' removed successfully.")
            break
    else:
        print(f"Error: List '{list_id}' not found.")
        return

    save_json(lists_file, lists_data)
    save_json(items_file, items_data)

# Example Usage
#remove_list(3)  # Adds item 2 to list 3
#print(get_items_in_list(3))  # Gets all items in list 3
#print(get_total_price_of_list(3))  # Gets total price of list 3
#print(get_item_price(2))  # Gets the price of item 2
#print(get_item_stock(2))  # Gets the stock of item 2
#add_item_to_list(1, 3, 2)  # Adds 2 units of item 2 to list 3
