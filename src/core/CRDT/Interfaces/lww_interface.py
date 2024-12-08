import sys

# Credits to @junjizhi for the model of the interface!
class LWW_Set:
    
    MAX_STRING_IN_BYTES = 1 << 29  # 512 MB

    def __init__(self):
        pass

    def add(self, element, timestamp):
        raise NotImplementedError("Subclasses should implement this!")

    def remove(self,element,timestamp):
        raise NotImplementedError("Subclasses should implement this!")
    
    def exist(self, element):
        raise NotImplementedError("Subclasses should implement this!")
    
    def get(self):
        raise NotImplementedError("Subclasses should implement this!")
    
    def validate_timestamp(self, timestamp):
        try:
            timestamp = float(timestamp)
        except:
            raise ValueError("Timestamp must be able to be converted to a float!")
        return timestamp
    
    def validate_element(self, element):

        #Check that elemen is a dict
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
    
    def merge(self, other_set):
        raise NotImplementedError("Subclasses should implement this!")

