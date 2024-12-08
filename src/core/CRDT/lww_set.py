from threading import *
from core.CRDT.Interfaces.lww_interface import LWW_Set

class LWW(LWW_Set):
    
    #A LWW with an inherent ADD Bias

    """
        Structure of each set:
        add set - {"Item" : {"Quantity": quantity, "timestamp": timestamp} }
        remove set - {"Item": {"Quantity": quantity, "timestamp": timestamp} }
    """
    def __init__(self):
        self.add_set = {}
        self.remove_set = {}
        self.add_lock = RLock()
        self.remove_lock = RLock()

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

        self.add_lock.acquire()

        try:
            if element["Item"] in self.add_set:
                current_timestamp = self.add_set[element["Item"]]["timestamp"]
                if current_timestamp < timestamp:
                    self.add_set[element["Item"]]["timestamp"] = timestamp
                elif current_timestamp == timestamp:
                    self.add_set[element["Item"]]["timestamp"] = timestamp
            else:
                self.add_set[element["Item"]] = {"Quantity": element["Quantity"], "timestamp": timestamp}
        except:
            return_flag = False
        finally:
            self.add_lock.release()

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

        self.remove_lock.acquire()

        try:
            if element["Item"] in self.remove_set:
                current_timestamp = self.remove_set_set[element["Item"]]["timestamp"]
                if current_timestamp < timestamp:
                    self.remove_set[element["Item"]]["timestamp"] = timestamp
            else:
                self.remove_set[element["Item"]] = {"Quantity": element["Quantity"], "timestamp": timestamp}
        except:
            return_flag = False
        finally:
            self.remove_lock.release()
        
        return return_flag

    def exist(self,element):
        element = self.validate_element(element)

        if(element not in self.add_set):
            return False
        elif(element not in self.remove_set):
            return True
        elif self.add_set[element["Item"]]["Timestamp"] >= self.remove_set[element["Item"]]["Timestamp"]:
            return True
        else:
            return False

    def get(self):
        set = []
        for element in self.add:
            if(self.exist(element)):
                set.append(element)
        return set
    
    def merge(self, other_set):

        return_flag = True
        
        self.add_lock.acquire()

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
        finally:
            self.add_lock.release()

        self.remove_lock.acquire()
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
        finally:
            self.remove_lock.release()

        self.add_lock.acquire()
        self.remove_lock.acquire()
        try:
            for item, value in list(self.add_set.items()):
                if item in self.remove_set:
                    if self.remove_set[item]["timestamp"] < value["timestamp"]:
                        del self.remove_set[item]
        except:
            return_flag = False
        finally:
            self.add_lock.release()
            self.remove_lock.release()

        return return_flag