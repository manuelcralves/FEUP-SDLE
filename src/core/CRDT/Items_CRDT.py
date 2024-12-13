from core.CRDT.Interfaces.lww_interface import LWW_Set

class Items_CRDT(LWW_Set):
    
    #A LWW with an inherent ADD Bias

    """
        Structure of each set:
        add set - {"Item" : {"Quantity": quantity, "timestamp": timestamp} }
        remove set - {"Item": {"Quantity": quantity, "timestamp": timestamp} }
    """
    def __init__(self):
        self.add_set = {}
        self.remove_set = {}

    def validate_timestamp(self, timestamp):
        try:
            timestamp = float(timestamp)
        except:
            raise ValueError("Timestamp must be able to be converted to a float!")
        return timestamp
    
    def validate_element(self, element):

        #Check that element is a dict
        if not isinstance(element, dict):
            raise ValueError("Element must be a dictionary.")
    
        # Check for required keys
        required_keys = {"Item", "Quantity"}
        if not required_keys.issubset(element.keys()):
            raise ValueError(f"Element must contain the keys: {required_keys}")
        
        # Validate the "Item" field
        item = element.get("Item")
        if not isinstance(item, str) or not item.strip():
            raise ValueError("The 'Item' field must be a non-empty string.")
        
        # Validate the "Quantity" field
        quantity = element.get("Quantity")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("The 'Quantity' field must be a non-negative integer.")
        
        return element

    """
        Structure of Element -
        element: {"Item": (item name), "Quantity": (n items)}
        
        timestamp - float
        (item name): string
        (n items): int
    """
    def add(self, element, timestamp):
        element = self.validate_element(element)
        timestamp = self.validate_timestamp(timestamp)
        
        return_flag = True

        try:
            if element["Item"] in self.add_set:
                current_timestamp = self.add_set[element["Item"]]["timestamp"]
                if current_timestamp <= timestamp:
                    self.add_set[element["Item"]]["timestamp"] = timestamp
                    self.add_set[element["Item"]]["Quantity"] = element["Quantity"]
            else:
                self.add_set[element["Item"]] = {"Quantity": element["Quantity"], "timestamp": timestamp}
        except:
            return_flag = False

        print(f"Added to Items_CRDT: {element} at timestamp {timestamp}")

        return return_flag

    """
        Structure of Element -
        element: {"Item": (item name), "Quantity": (n items)}
        
        timestamp - float
        (item name): string
        (n items): int
    """
    def remove(self, element, timestamp):
        element = self.validate_element(element)
        timestamp = self.validate_timestamp(timestamp)

        return_flag = True

        try:
            if element["Item"] in self.remove_set:
                current_timestamp = self.remove_set[element["Item"]]["timestamp"]
                if current_timestamp < timestamp:
                    self.remove_set[element["Item"]]["timestamp"] = timestamp
                    self.remove_set[element["Item"]]["Quantity"] = element["Quantity"]
            else:
                self.remove_set[element["Item"]] = {"Quantity": element["Quantity"], "timestamp": timestamp}
        except:
            return_flag = False
        
        return return_flag

    def exist(self,element):
        return_flag = True
        if(element not in self.add_set):
            return_flag = False
        elif(element not in self.remove_set):
                return_flag = False
        elif(self.add_set[element]['Quantity'] - self.remove_set[element]['Quantity'] <= 0):
                return_flag = False
        return return_flag

    def get(self):
        set = []
        try:
            for element, data in self.add_set.items(): 
                print("Element in add_set: ", element, "Data: ", data)
                if self.exist(element):
                    set.append({"Item": element, "Quantity": data["Quantity"]})
            print("Items_CRDT: ", set)
        except Exception as e:
            print(f"Error in get method: {e}")
        return set

    def merge(self, other_set):

        return_flag = True

        try:
            for item, value in other_set.add_set.items():
                quantity = value["Quantity"]
                timestamp = self.validate_timestamp(value["timestamp"])
                if item in self.add_set:
                    if self.add_set[item]["timestamp"] < timestamp:
                        self.add_set[item] = {"Quantity": quantity, "timestamp": timestamp}
                else:
                    self.add_set[item] = {"Quantity": quantity, "timestamp": timestamp}
        except:
            return_flag = False

        try:
            for item, value in other_set.remove_set.items():
                quantity = value["Quantity"]
                timestamp = self.validate_timestamp(value["timestamp"])
                if item in self.remove_set:
                    if self.remove_set[item]["timestamp"] < timestamp:
                        self.remove_set[item] = {"Quantity": quantity, "timestamp": timestamp}
                else:
                    self.remove_set[item] = {"Quantity": quantity, "timestamp": timestamp}
        except:
            return_flag = False

        try:
            for item, value in list(self.add_set.items()):
                if item in self.remove_set:
                    if self.remove_set[item]["timestamp"] < value["timestamp"]:
                        del self.remove_set[item]
        except:
            return_flag = False

        return return_flag
