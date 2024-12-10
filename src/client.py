import json
import zmq
import time
import threading
import os
import sys
from read_lists_items import add_new_item, remove_item_from_list, get_items_in_list, create_list, remove_list

def display_menu():
    print("\nAvailable Actions:")
    print("1. Add or Update Item in List")
    print("2. Remove Item from List")
    print("3. Get Items in List")
    print("4. Create New List")
    print("5. Remove List")
    print("6. Exit")

def get_user_choice():
    try:
        return int(input("Select an action (1-6): "))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 6.")
        return -1
    
def initialize_database(filepath):
    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as file:
            json.dump({"lists": []}, file, indent=4)
            print(f"Database created at {filepath}.")
    else:
        print(f"Database already exists at {filepath}.")

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

def client(client_name):
    lists_file = f"../client_database/{client_name}/lists.json"
    initialize_database(lists_file)
    
    action_queue = []
    threading.Thread(target=send_files_to_server, args=(action_queue,), daemon=True).start()

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == 1:  
            list_name = input("Enter List Name: ")
            item_id = input("Enter Item: ")
            quantity = int(input("Enter Quantity: "))
            status, result = add_new_item(list_name, item_id, lists_file, quantity)
            if status == 0:
                print(result)
                try:
                    with open(lists_file, "r") as file:
                        lists_data = json.load(file)
                        list_data = next(lst for lst in lists_data["lists"] if lst["name"] == list_name)
                        
                        request = {
                            "action": "update_list",
                            "list_id": list_data["id"],
                            "list_data": list_data
                        }
                        action_queue.append(request)
                except Exception as e:
                    print(f"Error reading lists.json: {e}")
            else:
                print(f"Error: {result}")
        elif choice == 2:  
            list_name = input("Enter List Name: ")
            item_id = input("Enter Item: ")
            quantity = int(input("Enter Quantity: "))
            status, result = remove_item_from_list(list_name, item_id, lists_file, quantity)
            if status == 0:
                print(result)
                try:
                    with open(lists_file, "r") as file:
                        lists_data = json.load(file)
                        list_data = next(lst for lst in lists_data["lists"] if lst["name"] == list_name)
                        
                        request = {
                            "action": "update_list",
                            "list_id": list_data["id"],
                            "list_data": list_data
                        }
                        action_queue.append(request)
                except Exception as e:
                    print(f"Error reading lists.json: {e}")
            else:
                print(f"Error: {result}")
        elif choice == 3:
            list_name = input("Enter List Name: ")
            status, result = get_items_in_list(list_name, lists_file)
            if status == 0:
                print(f"Items in List {list_name}:\n{result}")
            else:
                print(f"Error: {result}")
        elif choice == 4:  
            list_name = input("Enter New List Name: ")
            status, result = create_list(list_name, lists_file)
            if status == 0:
                print(result)
                try:
                    with open(lists_file, "r") as file:
                        lists_data = json.load(file)
                        new_list = next(lst for lst in lists_data["lists"] if lst["name"] == list_name)
                        
                        request = {
                            "action": "create_list",
                            "list_data": new_list
                        }
                        action_queue.append(request)
                except Exception as e:
                    print(f"Error reading lists.json: {e}")
            else:
                print(f"Error: {result}")
        elif choice == 5:  
            list_name = input("Enter List Name: ")
            status, result = remove_list(list_name, lists_file)
            if status == 0:
                print(result)
                request = {
                    "action": "remove_list",
                    "list_name": list_name
                }
                action_queue.append(request)
            else:
                print(f"Error: {result}")
        elif choice == 6:  
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py {client_name}")
        sys.exit(1)
    client_name = sys.argv[1]
    client(client_name)