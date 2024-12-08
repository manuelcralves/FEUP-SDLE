from threading import *
from core.CRDT.Interfaces.or_interface import OR_Set
from core.CRDT.Items_CRDT import Items_CRDT

class List_CRDT(OR_Set):

    def __init__(self):
        self.add_set = {}
        self.remove_set = {}
        self.add_lock = RLock()
        self.remove_lock = RLock()
        self.items = {}



    """
        Element Structure:
        id: (id of the list)
        items: [] (array of item elements)
        total_price: (price) 
    """

    def add(self, element):
        return_flag = True

        self.add_lock.acquire()
        try:
            self.add_set.add(element)
            self.items[element["id"]] = Items_CRDT()
        except:
            return_flag = False
        finally:
            self.add_lock.release()

        return return_flag
    
    def add_item(self, list_id, element, timestamp):
        return_flag = True
        try:
            self.items[list_id].add(element,timestamp)
        except:
            return_flag = False
        
        return return_flag

    def remove(self, element):
        return_flag = True

        self.remove_lock.acquire()
        try:
            self.remove_set.add(element)
        except:
            return_flag = False
        finally:
            self.remove_lock.release()

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

        self.add_lock.acquire()
        self.remove_lock.acquire()

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
        finally:
            self.add_lock.release()
            self.remove_lock.release()

        return return_flag
    
    def validate_element(element):

        if not isinstance(element, dict):
            raise ValueError("Element must be a dictionary.")
        
        required_keys = {"id", "items", "total_price"}
        if not required_keys.issubset(element.keys()):
            raise ValueError(f"Element must contain the keys: {required_keys}")
        
        shopping_list_id = element.get("id")
        if not isinstance(shopping_list_id, (str, int)) or (isinstance(shopping_list_id, str) and not shopping_list_id.strip()):
            raise ValueError("'id' must be a non-empty string or an integer.")
        
        items = element.get("items")
        if not isinstance(items, list) or not all(isinstance(item, str) and item.strip() for item in items):
            raise ValueError("'items' must be a list of non-empty strings.")
        
        total_price = element.get("total_price")
        if not isinstance(total_price, (int, float)) or total_price < 0:
            raise ValueError("'total_price' must be a non-negative number.")
        
        return element
    

        

