from datetime import datetime
import json
from threading import Thread
from core.CRDT.Items_CRDT import Items_CRDT
from core.CRDT.List_CRDT import List_CRDT

# Logging function
def log(message):
    # print(f"[{datetime.now()}] {message}")
    print(f"{message}")

# Helper function to load data from JSON
def load_json(filepath):
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        log(f"Error: File {filepath} not found.")
        return {}
    except json.JSONDecodeError:
        log(f"Error: File {filepath} is not a valid JSON.")
        return {}

# Helper function to save data to JSON
def save_json(filepath, data):
    try:
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        log(f"Error saving file {filepath}: {e}")

# Function to log the current state of the CRDT
def log_crdt_state(list_crdt, message="Current CRDT State"):
    log(message)
    if not list_crdt.items:
        log("CRDT is empty.")
    else:
        for list_id, crdt_items in list_crdt.items.items():
            log(f"List ID: {list_id}")
            log("  Items:")
            for item, data in crdt_items.add_set.items():
                log(f"    - {item}: {data}")

def initialize_crdt():
    lists_data = load_json("lists.json")
    items_data = load_json("items_details.json")

    if not lists_data or not items_data:
        log("Initialization failed due to missing data.")
        return None, None

    list_crdt = List_CRDT()

    for lst in lists_data["lists"]:
        success = list_crdt.add({
            "id": lst["id"],
            "items": lst["items"],
            "total_price": lst["total_price"]
        })
        if not success:
            log(f"Failed to add list {lst['id']}")

        for item in lst["items"]:
            if isinstance(item, dict) and "Item" in item and "Quantity" in item:
                success = list_crdt.add_item(
                    lst["id"],
                    {"Item": item["Item"], "Quantity": item["Quantity"]},
                    timestamp=0
                )
                if not success:
                    log(f"Failed to add item {item['Item']} to list {lst['id']}")
            else:
                log(f"Invalid item structure in list {lst['id']}: {item}")

    log_crdt_state(list_crdt, "Initialized CRDT with data from files.")
    return list_crdt, items_data


def test_conflicting_operations(list_crdt):
    log("Testing Conflicting Operations...")

    list_crdt.add_item(1, {"Item": "3", "Quantity": 1}, timestamp=1)  # Earlier timestamp
    list_crdt.add_item(1, {"Item": "3", "Quantity": 2}, timestamp=1)  # Later timestamp
    log_crdt_state(list_crdt, "After conflicting adds to item 3 in list 1.")

    list_crdt.remove_item(1, {"Item": "3", "Quantity": 1}, timestamp=3)  # Later timestamp
    list_crdt.remove_item(1, {"Item": "3", "Quantity": 2}, timestamp=2)  # Earlier timestamp
    log_crdt_state(list_crdt, "After conflicting removes of item 3 in list 1.")

def save_final_state(list_crdt, items_data):
    try:
        final_state = {
            "lists": [
                {
                    "id": list_id,
                    "items": [
                        {"Item": item_id, "Quantity": item_data["Quantity"]}
                        for item_id, item_data in list_crdt.items[list_id].add_set.items()
                    ],
                    "total_price": sum(
                        item_data["Quantity"]
                        * next(
                            (i["price"] for i in items_data["items"] if i["id"] == item_id),
                            0,
                        )
                        for item_id, item_data in list_crdt.items[list_id].add_set.items()
                    ),
                }
                for list_id in list_crdt.items
            ]
        }

        save_json("lists.json", final_state)
        log("Final state saved to lists.json.")
    except Exception as e:
        log(f"Error saving final state: {e}")

def main():

    list_crdt, items_data = initialize_crdt()

    if not list_crdt or not items_data:
        log("Initialization failed. Exiting.")
        return

    test_conflicting_operations(list_crdt)

    log_crdt_state(list_crdt, "Final CRDT State:")

    save_final_state(list_crdt, items_data)

    log("CRDT Testing Completed.")

if __name__ == "__main__":
    main()
