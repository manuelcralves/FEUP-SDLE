import sys

# Credits to @junjizhi for the model of the interface!
class LWW_Set:
    
    MAX_STRING_IN_BYTES = 1 << 29  # 512 MB

    def __init__(self):
        pass

    def validate_element(self, element):
        raise NotImplementedError("Subclasses should implement this!")
    
    def validate_timestamp(self,timestamp):
        raise NotImplementedError("Subclasses should implement this!")
    
    def add(self, element, timestamp):
        raise NotImplementedError("Subclasses should implement this!")

    def remove(self,element,timestamp):
        raise NotImplementedError("Subclasses should implement this!")
    
    def exist(self, element):
        raise NotImplementedError("Subclasses should implement this!")
    
    def get(self):
        raise NotImplementedError("Subclasses should implement this!")
    
    def merge(self, other_set):
        raise NotImplementedError("Subclasses should implement this!")

