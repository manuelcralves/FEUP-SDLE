import zmq

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

def client():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")  

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == 1:
            list_id = int(input("Enter List ID: "))
            item_id = int(input("Enter Item ID: "))
            request = {"action": "add_item", "list_id": list_id, "item_id": item_id}
        elif choice == 2:
            list_id = int(input("Enter List ID: "))
            item_id = int(input("Enter Item ID: "))
            request = {"action": "remove_item", "list_id": list_id, "item_id": item_id}
        elif choice == 3:
            list_id = int(input("Enter List ID: "))
            request = {"action": "get_items", "list_id": list_id}
        elif choice == 4:
            list_id = int(input("Enter List ID: "))
            request = {"action": "get_total_price", "list_id": list_id}
        elif choice == 5:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        print(f"Sending request: {request}")
        socket.send_json(request)

        response = socket.recv_json()
        print(f"Response: {response}")

if __name__ == "__main__":
    client()
