import json

items_file = "items_details.json"
lists_file = "lists.json"

def load_json(filepath):
    with open(filepath, "r") as file:
        return json.load(file)

def save_json(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

def add_item_to_list(list_id, item_id):
    items_data = load_json(items_file)
    lists_data = load_json(lists_file)
    
    # Find the item by ID
    item = next((item for item in items_data["items"] if item["id"] == item_id), None)
    if item is None:
        print(f"Error: Item '{item_id}' not found.")
        return
    
    # Check if there's enough stock
    if item["stock"] <= 0:
        print(f"Error: Item '{item_id}' is out of stock.")
        return
    
    # Find the list by ID
    for lst in lists_data["lists"]:
        if lst["id"] == list_id:
            # Add the item to the list
            lst["items"].append(item_id)
            lst["total_price"] += item["price"]
            item["stock"] -= 1  # Reduce the stock
            print(f"Item '{item_id}' added to list '{list_id}'. Remaining stock: {item['stock']}.")
            break
    else:
        # List does not exist, create a new one
        new_list = {
            "id": list_id,
            "items": [item_id],
            "total_price": item["price"]
        }
        lists_data["lists"].append(new_list)
        item["stock"] -= 1  # Reduce the stock
        print(f"List '{list_id}' created and item '{item_id}' added. Remaining stock: {item['stock']}.")

    # Save changes to JSON files
    save_json(lists_file, lists_data)
    save_json(items_file, items_data)

def remove_item_from_list(list_id, item_id):
    items_data = load_json(items_file)
    lists_data = load_json(lists_file)
    
    # Find the item by ID
    item = next((item for item in items_data["items"] if item["id"] == item_id), None)
    if item is None:
        print(f"Error: Item '{item_id}' not found.")
        return

    # Find the list by ID
    for lst in lists_data["lists"]:
        if lst["id"] == list_id:
            if item_id in lst["items"]:
                lst["items"].remove(item_id)  # Remove one occurrence of the item
                lst["total_price"] -= item["price"]
                item["stock"] += 1  # Restock the item
                print(f"Item '{item_id}' removed from list '{list_id}'. Updated stock: {item['stock']}.")
            else:
                print(f"Item '{item_id}' is not in list '{list_id}'.")
            break
    else:
        print(f"Error: List '{list_id}' not found.")
        return

    # Save changes to JSON files
    save_json(lists_file, lists_data)
    save_json(items_file, items_data)

def remove_list(list_id):
    # Load JSON files
    lists_data = load_json(lists_file)
    items_data = load_json(items_file)
    
    # Find the list by ID
    for lst in lists_data["lists"]:
        if lst["id"] == list_id:
            # Update stock for all items in the list
            for item_id in lst["items"]:
                # Find the item and update stock
                item = next((item for item in items_data["items"] if item["id"] == item_id), None)
                if item:
                    item["stock"] += 1  # Increase stock for each occurrence of the item
                    print(f"Stock for item '{item_id}' updated: {item['stock']}.")
            
            # Remove the list
            lists_data["lists"].remove(lst)
            print(f"List '{list_id}' removed successfully.")
            break
    else:
        # List not found
        print(f"Error: List '{list_id}' not found.")
        return

    # Save changes to JSON files
    save_json(lists_file, lists_data)
    save_json(items_file, items_data)

# Test calls
add_item_to_list(3, 2)  # Adds an item
remove_item_from_list(3, 2)  # Removes one occurrence of the item
#remove_list(3)  # Removes a list
