from threading import *
from core.CRDT.Interfaces.or_interface import OR_Set
from core.CRDT.Items_CRDT import Items_CRDT

class List_CRDT(OR_Set):

    def __init__(self):
        self.add_set = {}
        self.remove_set = {}
        self.items = {}

    """
        Element Structure:
        id: (id of the list)
        items: [] (array of item elements)
        total_price: (price) 
    """
    def add(self, element):
        return_flag = True

        try:
            self.validate_element(element)
            if element["id"] not in self.add_set:
                self.add_set[element["id"]] = element
                self.items[element["id"]] = Items_CRDT()
            else:
                return_flag = False
        except Exception as e:
            print(e)
            return_flag = False

        return return_flag
    
    def add_item(self, list_id, element, timestamp):
        return_flag = True
        try:
            self.items[list_id].add(element,timestamp)
        except Exception as e:
            print(e)
            return_flag = False
        
        return return_flag

    def remove(self, element):
        return_flag = True

        try:
            self.remove_set.add(element)
        except:
            return_flag = False

        return return_flag
    
    def remove_item(self,list_id,element,timestamp):
        return_flag = True
        try:
            self.items[list_id].remove(element,timestamp)
        except:
            return_flag = False

        return return_flag
    
    def merge(self,other_set):
        return_flag = True

        try:
            self.add_set = self.add_set.union(other_set.add_set)
            self.remove_set = self.remove_set.union(other_set.remove_set)
            
            for list_id, items in other_set.items.items():
                if list_id in self.items:
                    self.items[list_id].merge(items)
                else:
                    self.items[list_id] = items
        except:
            return_flag = False

        return return_flag
    
    def validate_element(self, element):

        if not isinstance(element, dict):
            raise ValueError("Element must be a dictionary.")
        
        required_keys = {"id", "items", "total_price"}
        if not required_keys.issubset(element.keys()):
            raise ValueError(f"Element must contain the keys: {required_keys}")
        
        shopping_list_id = element.get("id")
        if not isinstance(shopping_list_id, (str, int)) or (isinstance(shopping_list_id, str) and not shopping_list_id.strip()):
            raise ValueError("'id' must be a non-empty string or an integer.")
        
        items = element.get("items")
        #print(f"Validating items: {items} ({type(items)})")  # Debug: print items and type
        if not isinstance(items, list):
            raise ValueError("'items' must be a list.")
        
        for item in items:
            # print(f"Validating item: {item} ({type(item)})")  # Debug: print each item and type
            if isinstance(item, dict):
                # Ensure the dictionary has required keys
                if not {"Item", "Quantity"}.issubset(item.keys()):
                    raise ValueError(f"Item {item} must contain 'Item' and 'Quantity' keys.")
                if not isinstance(item["Item"], (str, int)) or (isinstance(item["Item"], str) and not item["Item"].strip()):
                    raise ValueError(f"Item 'Item' field must be a non-empty string or integer in {item}.")
                if not isinstance(item["Quantity"], int) or item["Quantity"] <= 0:
                    raise ValueError(f"Item 'Quantity' field must be a positive integer in {item}.")
            elif isinstance(item, (str, int)):
                continue  # Allow plain strings/integers as valid items
            else:
                raise ValueError(f"Item '{item}' must be a dictionary, string, or integer.")
            
        total_price = element.get("total_price")
        if not isinstance(total_price, (int, float)) or total_price < 0:
            raise ValueError("'total_price' must be a non-negative number.")
        
        return element
    

        

