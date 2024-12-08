class OR_Set:

    def __init__(self):
        pass

    def add(load, element, tag):
        raise NotImplementedError("Subclasses should implement this!")
    
    def remove(loadA, loadR, element):
        raise NotImplementedError("Subclasses should implement this!")
    
    def compare(load1, load2):
        raise NotImplementedError("Subclasses should implement this!")
    
    def merge(load1,load2):
        raise NotImplementedError("Subclasses should implement this!")
    
    def display(name, load):
        raise NotImplementedError("Subclasses should implement this!")
    
    def query(element, load):
        raise NotImplementedError("Subclasses should implement this!")
    
    def validate_element(element):
        raise NotImplementedError("Subclasses should implement this!")