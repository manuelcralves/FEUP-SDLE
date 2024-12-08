from threading import *
from core.CRDT.Interfaces.lww_interface import LWW_Set

class LWW(LWW_Set):
    
    #A LWW with an inherent ADD Bias

    def __init__(self):
        self.add_set = {}
        self.remove_set = {}
        self.add_lock = RLock()
        self.remove_lock = RLock()

    def add(self, element, timestamp):
        element = self.validate_element(element)
        timestamp = self.validate_timestamp(timestamp)
        
        return_flag = True

        self.add_lock.acquire()

        try:
            self._test_and_op(self.add_set, element, timestamp)
        except:
            return_flag = False
        finally:
            self.add_lock.release()

        return return_flag

    def remove(self, element, timestamp):
        element = self.validate_element(element)
        timestamp = self.validate_timestamp(timestamp)

        return_flag = True

        self.remove_lock.acquire()

        try:
            self._test_and_op(self.remove_set,element,timestamp)
        except:
            return_flag = False
        finally:
            self.remove_lock.release()
        
        return return_flag
    
    def _test_and_op(self, set, element, timestamp):
        if element in set:
            current_timestamp = set[element]
            if(current_timestamp < timestamp):
                set[element] = timestamp
            elif(current_timestamp == timestamp):
                if(set == self.add_set):
                    set[element] = timestamp
        else: 
            set[element] = timestamp

    def exist(self,element):
        element = self.validate_element(element)

        if(element not in self.add_set):
            return False
        elif(element not in self.remove_set):
            return True
        elif self.add_set[element] >= self.remove_set[element]:
            return True
        else:
            return False

    def get(self):
        set = []
        for element in self.add_set:
            if(self.exist(element)):
                set.append(element)
        return set