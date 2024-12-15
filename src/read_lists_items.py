import json
from prettytable import PrettyTable
import uuid

def load_json(filepath):
    with open(filepath, "r") as file:
        return json.load(file)

def save_json(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

def add_new_item(list_name, item_id, lists_file, quantity=1):
    if quantity < 1:
        return -1, "Quantity must be greater than or equal to 1."

    lists_data = load_json(lists_file)

    for lst in lists_data["lists"]:
        if lst["name"] == str(list_name):
            for item in lst["items"]:
                if item["Item"] == str(item_id):
                    item["Quantity"] += quantity
                    mod = {"Item": str(item_id), "Quantity": quantity}
                    save_json(lists_file, lists_data)
                    return 0, f"Item '{item_id}' in list '{list_name}' incremented by {quantity}.", mod

            mod = {"Item": str(item_id), "Quantity": quantity}
            lst["items"].append(mod)
            save_json(lists_file, lists_data)
            return 0, f"New item '{item_id}' added to list '{list_name}' with quantity {quantity}.", mod

    return -1, f"List '{list_name}' not found. Please create it first.", None

def create_list(list_name, lists_file):
    if not str(list_name):
        return -1, "List name must be a non-empty string."

    lists_data = load_json(lists_file)

    for lst in lists_data["lists"]:
        if str(lst["name"]) == str(list_name):
            return -1, f"List name '{list_name}' already exists."

    new_list = {"id": str(uuid.uuid4()), "name": str(list_name), "items": []}
    lists_data["lists"].append(new_list)
    save_json(lists_file, lists_data)
    return 0, f"List '{list_name}' created successfully with ID '{new_list['id']}'."

def get_items_in_list(list_name, lists_file):
    lists_data = load_json(lists_file)
    for lst in lists_data["lists"]:

        if lst["name"] == str(list_name):
            table = PrettyTable()
            table.field_names = ["Item ID", "Quantity"]
            for item in lst["items"]:
                table.add_row([item["Item"], item["Quantity"]])
            return 0, table.get_string()
    return -1, f"List '{list_name}' not found."

def remove_item_from_list(list_name, item_id, lists_file, quantity=1):
    if quantity < 1:
        return -1, "Quantity must be greater than or equal to 1."

    lists_data = load_json(lists_file)

    for lst in lists_data["lists"]:
        if lst["name"] == str(list_name):
            for item in lst["items"]:
                if item["Item"] == str(item_id):
                    if item["Quantity"] >= quantity:
                        item["Quantity"] = quantity
                        mod = {"Item": str(item_id), "Quantity": quantity}
                        save_json(lists_file, lists_data)
                        return 0, f"{quantity} units of item '{item_id}' removed from list '{list_name}'.", mod
                    else:
                        return -1, f"Cannot remove {quantity} units. Only {item['Quantity']} available.", None
            return -1, f"Item '{item_id}' not found in list '{list_name}'.", None
    return -1, f"List '{list_name}' not found.", None

def remove_list(list_name, lists_file):
    lists_data = load_json(lists_file)

    for lst in lists_data["lists"]:
        if lst["name"] == str(list_name):
            lists_data["lists"].remove(lst)
            save_json(lists_file, lists_data)
            return 0, f"List '{list_name}' removed successfully."
    return -1, f"List '{list_name}' not found."