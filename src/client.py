import json
import zmq
import os
from read_lists_items import add_item_to_list, remove_item_from_list, get_items_in_list, get_total_price_of_list

def display_menu():
    print("\nAvailable Actions:")
    print("1. Add Item to List")
    print("2. Remove Item from List")
    print("3. Get Items in List")
    print("4. Get Total Price of List")
    print("5. Exit")

def get_user_choice():
    try:
        return int(input("Select an action (1-5): "))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 5.")
        return -1

def send_files_to_server():
    try:
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")

        with open("../client_database/items_details.json", "r") as items_file:
            items_data = items_file.read()
        with open("../client_database/lists.json", "r") as lists_file:
            lists_data = lists_file.read()

        request = {
            "action": "update_files",
            "items_data": items_data,
            "lists_data": lists_data
        }
        socket.send_json(request)
        response = socket.recv_json()
        return response
    except zmq.ZMQError:
        return None

def client():
    while True:
        display_menu()
        choice = get_user_choice()

        if choice == 1:
            list_id = int(input("Enter List ID: "))
            item_id = int(input("Enter Item ID: "))
            quantity = int(input("Enter Quantity: "))
            result = add_item_to_list(list_id, item_id, quantity)
            if result == 0:
                print(f"Item {item_id} was successfully added to list {list_id}.")
            else:
                print(f"Failed to add item {item_id} to list {list_id}.")
        elif choice == 2:
            list_id = int(input("Enter List ID: "))
            item_id = int(input("Enter Item ID: "))
            quantity = int(input("Enter Quantity: "))
            result = remove_item_from_list(list_id, item_id, quantity)
            if result == 0:
                print(f"Item {item_id} was successfully removed from list {list_id}.")
            else:
                print(f"Failed to remove item {item_id} from list {list_id}.")
        elif choice == 3:
            list_id = int(input("Enter List ID: "))
            items = get_items_in_list(list_id)
            if items:
                print(f"Items in list {list_id}: {items}")
            else:
                print(f"No items found in list {list_id}.")
        elif choice == 4:
            list_id = int(input("Enter List ID: "))
            total_price = get_total_price_of_list(list_id)
            print(f"The total price of list {list_id} is ${total_price:.2f}.")
        elif choice == 5:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

        response = send_files_to_server()
        if response:
            print("Server updated successfully.")
        else:
            print("Failed to update server. Changes will be queued.")

if __name__ == "__main__":
    client()