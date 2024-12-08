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
        try:
            element = str(element)
        except:
            raise ValueError("Element must be able to be converted to a String!")
        
        if sys.getsizeof(element) > self.MAX_STRING_IN_BYTES:
            raise ValueError("Element string exceeds the maximum length in bytes: %s!"%self.MAX_STRING_IN_BYTES)
        return element

