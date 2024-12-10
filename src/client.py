import json
import zmq
import os
import time
import threading
from read_lists_items import add_item_to_list, remove_item_from_list, get_items_in_list, get_total_price_of_list, remove_list, get_item_price, get_item_stock

def display_menu():
    print("\nAvailable Actions:")
    print("1. Add Item to List")
    print("2. Remove Item from List")
    print("3. Get Items in List")
    print("4. Get Total Price of List")
    print("5. Remove List")
    print("6. Get Item Price")
    print("7. Get Item Stock")
    print("8. Exit")

def get_user_choice():
    try:
        return int(input("Select an action (1-8): "))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 8.")
        return -1

def send_files_to_server(queue):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    while True:
        if queue:
            request = queue[0]
            try:
                socket.send_json(request)
                response = socket.recv_json()
                if response["status"] == "success":
                    queue.pop(0)
                else:
                    print("Failed to update server:", response["message"])
            except zmq.ZMQError:
                print("Server is offline. Queuing the actions.")
                time.sleep(5)  
        else:
            time.sleep(1)  

def client():
    action_queue = []
    threading.Thread(target=send_files_to_server, args=(action_queue,), daemon=True).start()

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == 1:
            list_id = int(input("Enter List ID: "))
            item_id = int(input("Enter Item ID: "))
            quantity = int(input("Enter Quantity: "))
            type, result = add_item_to_list(list_id, item_id, quantity)
            if type == 0:
                print(result)
            else:
                print(f"Error: {result}")
        elif choice == 2:
            list_id = int(input("Enter List ID: "))
            item_id = int(input("Enter Item ID: "))
            quantity = int(input("Enter Quantity: "))
            type, result = remove_item_from_list(list_id, item_id, quantity)
            if type == 0:
                print(result)
            else:
                print(f"Error: {result}")
        elif choice == 3:
            list_id = int(input("Enter List ID: "))
            type, result = get_items_in_list(list_id)
            if type == 0:
                print(result)
            else:
                print(f"Error: {result}")
        elif choice == 4:
            list_id = int(input("Enter List ID: "))
            type, result = get_total_price_of_list(list_id)
            if type == 0:
                print(f"The total price of list {list_id} is ${result:.2f}.")
            else:
                print(f"Error: {result}")
        elif choice == 5:
            list_id = int(input("Enter List ID: "))
            type, result = remove_list(list_id)
            if type == 0:
                print(result)
            else:
                print(f"Error: {result}")
        elif choice == 6:
            item_id = int(input("Enter Item ID: "))
            type, result = get_item_price(item_id)
            if type == 0:
                print(f"The price of item {item_id} is ${result:.2f}.")
            else:
                print(f"Error: {result}")
        elif choice == 7:
            item_id = int(input("Enter Item ID: "))
            type, result = get_item_stock(item_id)
            if type == 0:
                print(f"The stock of item {item_id} is {result}.")
            else:
                print(f"Error: {result}")
        elif choice == 8:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        try:
            with open("../client_database/items_details.json", "r") as items_file:
                items_data = items_file.read()
            with open("../client_database/lists.json", "r") as lists_file:
                lists_data = lists_file.read()

            request = {
                "action": "update_files",
                "items_data": items_data,
                "lists_data": lists_data
            }
            action_queue.append(request)
        except Exception as e:
            print(f"Error reading files: {e}")

if __name__ == "__main__":
    client()