from core.CRDT.Interfaces.or_interface import OR_Set
from core.CRDT.Items_CRDT import Items_CRDT

class List_CRDT(OR_Set):

    def __init__(self, list_id):
        self.add_set = {}
        self.remove_set = {}
        self.items = Items_CRDT()
        self.list_id = list_id
        self.timestamp = 0

    """
        Structure of Element -
        element: {"Item": (item name), "Quantity": (n items)}

    """
    def add(self, element):
        return_flag = True

        try:
            if element["Item"] not in self.add_set:
                self.add_set[element["Item"]] = None
                self.add_item(element,self.timestamp)
                self.timestamp += 1
            else:
                return_flag = False
                print("Item already exists!")
        except Exception as e:
            print(e)
            return_flag = False

        return return_flag
    
    def add_item(self, element, timestamp):
        return_flag = True
        try:
            self.items.add(element,timestamp)
        except Exception as e:
            print(e)
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
                if element["Item"] not in self.remove_set:
                    self.remove_set.add({element["Item"]: flag})
                    self.remove_item(element,self.timestamp)
                    self.timestamp += 1
                else:
                    if(flag):
                        self.remove_set.add({element["Item"]: flag})
            else:
                raise ValueError("Flag must be either TRUE or FALSE")
        except Exception as e:
            print(e)
            return_flag = False

        return return_flag
    
    def remove_item(self,element,timestamp):
        return_flag = True
        try:
            self.items.remove(element,timestamp)
        except Exception as e:
            print(e)
            return_flag = False

        return return_flag
    
    def merge(self,other_set):
        return_flag = True

        try:
            self.add_set = self.add_set.union(other_set.add_set)
            self.remove_set = self.remove_set.union(other_set.remove_set)
            self.items.merge(other_set.items)
        except Exception as e:
            print(e)
            return_flag = False

        return return_flag
    
    def get_list(self):
        set = []
        for item in self.items.get():
            if item["Item"] not in self.remove_set:
                set.append(item)
        
        return set


        

