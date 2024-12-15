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
        if not isinstance(element, tuple):
            raise ValueError("Element must be a tuple.")
    
        # Check for length
        length = len(element)
        if length != 2:
            raise ValueError(f"Element must be of length 2")
        
        # Validate the "Item" field
        item = element[0]
        if not isinstance(item, str) or not item.strip():
            raise ValueError("The first position of the tuple must be a str")
        
        # Validate the "Quantity" field
        quantity = element[1]
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("The second position of the tuple must be a non-negative integer")
        
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
            print("add_set: ", self.add_set)
            print(f"Element: {element}")
            if element[0] in self.add_set:
                print("Element in add_set: ", element[0])
                current_timestamp = self.add_set[element[0]]["timestamp"]
                if current_timestamp <= timestamp:
                    self.add_set[element[0]]["timestamp"] = timestamp
                    self.add_set[element[0]]["Quantity"] = element[1]
            else:
                self.add_set[element[0]] = {"Quantity": element[1], "timestamp": timestamp}
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
            if element[0] in self.remove_set:
                current_timestamp = self.remove_set[element[0]]["timestamp"]
                if current_timestamp < timestamp:
                    self.remove_set[element[0]]["timestamp"] = timestamp
                    self.remove_set[element[0]]["Quantity"] = element["Quantity"]
            else:
                self.remove_set[element[0]] = {"Quantity": element[1], "timestamp": timestamp}
        except:
            return_flag = False
        
        return return_flag

    def exist(self, element):
        if element not in self.add_set and element not in self.remove_set:
            print("Element not in add_set or remove_set")
            return False

        # add_quantity = self.add_set[element]["Quantity"] if element in self.add_set else 0
        # remove_quantity = self.remove_set[element]["Quantity"] if element in self.remove_set else 0
        elif element in self.add_set and element not in self.remove_set:
            print("Element do exist!")
            return True
        # if add_quantity - remove_quantity < 0:
        elif(self.add_set[element]['Quantity'] - self.remove_set[element]['Quantity'] < 0):
            print("Quantity is less than 0")
            return False

        print("Element exists")
        return True

    def get(self):
        set = []
        try:
            print("Starting get_list operation.")
            for element, data in self.add_set.items():
                print(f"Element in add_set: {element}\nData: {data}\n\n")

                if self.exist(element):

                    if element in self.remove_set:
                        remove_quantity = self.remove_set[element]["Quantity"]
                        effective_quantity = data["Quantity"] - remove_quantity
                        set.append({"Item": element, "Quantity": effective_quantity})
                    else:
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
