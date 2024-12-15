from core.CRDT.Interfaces.or_interface import OR_Set
from core.CRDT.Items_CRDT import Items_CRDT

class List_CRDT(OR_Set):

    def __init__(self, list_id, list_name):
        self.add_set = {}
        self.remove_set = {}
        self.items = Items_CRDT()
        self.list_id = list_id
        self.list_name = list_name
        self.timestamp = 0

    """
        Structure of Element -
        element: {"Item": (item name), "Quantity": (n items)}
        element(tuple): ("ItemName","Quantity","Purchased")
        ItemName - Nome
        Quantity - Quantidade
        Purchased - Flag

    """
    def add(self, element):
        return_flag = True

        try:
            if element[0] not in self.add_set:
                print(f"Adding new element: {element}")
                self.add_set[element[0]] = None
                self.add_item(element,self.timestamp)
                print(f"Item added: {element} at timestamp {self.timestamp}")
                self.timestamp += 1
            else:
                return_flag = False
                print("Item already exists!")
                print(f"Attempted to add an existing item: {element}")
                self.add_item(element,self.timestamp)
        except Exception as e:
            print(f"Error adding item: {e}")
            return_flag = False

        return return_flag
    
    def add_item(self, element, timestamp):
        return_flag = True
        try:
            self.items.add(element,timestamp)
            print(f"Item successfully added: {element} with timestamp {timestamp}")
        except Exception as e:
            print(f"Error adding item: {element}, error: {e}")
            return_flag = False

        
        return return_flag

    """
    Element - Product being removed
    Flag - Reason of removal (True being Purchased, False being Removed)
    Program has a PURCHASE bias
    """
    def remove(self, element, flag):
        return_flag = True
        
        try:
            if(flag is bool):
                if element[0] not in self.remove_set:
                    self.remove_set.add({element[0]: flag})
                    self.remove_item(element,self.timestamp)
                    print(f"Item removed: {element} with flag: {flag} at timestamp: {self.timestamp}")
                    self.timestamp += 1
                else:
                    if(flag):
                        self.remove_set.add({element[0]: flag})
            else:
                raise ValueError("Flag must be either TRUE or FALSE")
        except Exception as e:
            print(f"Error removing item: {element}, error: {e}")
            return_flag = False

        return return_flag
    
    def remove_item(self,element,timestamp):
        return_flag = True
        try:
            
            self.items.remove(element,timestamp)
            print(f"Removed from Item: {element} at timestamp: {timestamp}")
        except Exception as e:
            print(f"Error in remove_item: {element}, timestamp: {timestamp}, error: {e}")
            return_flag = False

        return return_flag
    
    def merge(self,other_set):
        return_flag = True

        try:
            print(f"Starting merge operation with other_set: {other_set.list_id}")
            self.add_set = self.add_set.union(other_set.add_set)
            self.remove_set = self.remove_set.union(other_set.remove_set)
            self.items.merge(other_set.items)
            print(f"Merge successful with other_set: {other_set.list_id}")
        except Exception as e:
            print(f"Error during merge with other_set: {other_set.list_id}, error: {e}")
            return_flag = False

        return return_flag
    
    def get_list(self):
        result_set = []

        try:
            print("Starting get_list operation.")
            for item in self.items.get():
                print(f"Item: {item}")
                if item["Item"] not in self.remove_set:
                    result_set.append(item)
            print(f"get_list result: {result_set}")
        except Exception as e:
            print(f"Error during get_list operation, error: {e}")

        return result_set
