class EntityBase:
    '''
    Class that represents base class of for each 'savable' property. 
    It contains common element such as the ID  
    '''
    def __init__(self):
        self.id:int =  None #internal id for the device

    def to_dictionary(self):
        '''
        returns a dictionary representation of this object.        
        '''
        return self.__dict__