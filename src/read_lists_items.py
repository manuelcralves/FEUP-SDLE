import json
from prettytable import PrettyTable

lists_file = "../client_database/lists.json"

def load_json(filepath):
    with open(filepath, "r") as file:
        return json.load(file)

def save_json(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

def add_new_item(list_id, item_id, quantity=1):
    if quantity < 1:
        return -1, "Quantity must be greater than or equal to 1."

    lists_data = load_json(lists_file)

    for lst in lists_data["lists"]:
        if lst["id"] == str(list_id):
            for item in lst["items"]:
                if item["Item"] == str(item_id):
                    item["Quantity"] += quantity
                    save_json(lists_file, lists_data)
                    return 0, f"Item '{item_id}' in list '{list_id}' incremented by {quantity}."

            lst["items"].append({"Item": str(item_id), "Quantity": quantity})
            save_json(lists_file, lists_data)
            return 0, f"New item '{item_id}' added to list '{list_id}' with quantity {quantity}."

    return -1, f"List '{list_id}' not found. Please create it first."

def create_list(list_id):
    if not str(list_id):
        return -1, "List ID must be a non-empty string."

    lists_data = load_json(lists_file)

    for lst in lists_data["lists"]:
        if lst["id"] == str(list_id):
            return -1, f"List ID '{list_id}' already exists."

    new_list = {"id": str(list_id), "items": []}
    lists_data["lists"].append(new_list)
    save_json(lists_file, lists_data)
    return 0, f"List '{list_id}' created successfully."

def get_items_in_list(list_id):
    lists_data = load_json(lists_file)
    for lst in lists_data["lists"]:

        if lst["id"] == str(list_id):
            table = PrettyTable()
            table.field_names = ["Item ID", "Quantity"]
            for item in lst["items"]:
                table.add_row([item["Item"], item["Quantity"]])
            return 0, table.get_string()
    return -1, f"List '{list_id}' not found."

def remove_item_from_list(list_id, item_id, quantity=1):
    if quantity < 1:
        return -1, "Quantity must be greater than or equal to 1."

    lists_data = load_json(lists_file)

    for lst in lists_data["lists"]:
        if lst["id"] == str(list_id):
            for item in lst["items"]:
                if item["Item"] == str(item_id):
                    if item["Quantity"] > quantity:
                        item["Quantity"] -= quantity
                        save_json(lists_file, lists_data)
                        return 0, f"{quantity} units of item '{item_id}' removed from list '{list_id}'."
                    elif item["Quantity"] == quantity:
                        lst["items"].remove(item)
                        save_json(lists_file, lists_data)
                        return 0, f"Item '{item_id}' removed entirely from list '{list_id}'."
                    else:
                        return -1, f"Cannot remove {quantity} units. Only {item['Quantity']} available."
            return -1, f"Item '{item_id}' not found in list '{list_id}'."
    return -1, f"List '{list_id}' not found."

def remove_list(list_id):
    lists_data = load_json(lists_file)

    for lst in lists_data["lists"]:
        if lst["id"] == str(list_id):
            lists_data["lists"].remove(lst)
            save_json(lists_file, lists_data)
            return 0, f"List '{list_id}' removed successfully."
    return -1, f"List '{list_id}' not found."
