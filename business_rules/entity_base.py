class EntityBase:
    '''
    Class that represents base class of for each 'savable' entity. 
    It contains common element such as the ID  
    '''
    def __init__(self):
        self.id:int =  None #internal id for the device

    def to_dictionary(self):
        '''
        returns a dictionary representation of this object.        
        '''
        return self.__dict__
    
    @staticmethod
    def get_new_entity_key(entity_list:list):
        '''
        Returns a new ID given a list of entities.
        '''        
        if not entity_list:
            raise ValueError("Parameter entity_list can not be none.")

        if len(entity_list) <= 0:
            return 1 

        return max(entity_list, key=lambda x: x.id).id + 1

