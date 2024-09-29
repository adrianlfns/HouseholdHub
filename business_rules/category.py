class Category:
    '''
    Class that represents the information of a single category
    '''

    def __init__(self):
        #general information of the category
        self.id:int =  None #internal id
        self.category_name = ''

    def update_from_dictionary(self, dict:dict):
        '''
        update all the properties from a dictionary
        '''

        #small sanitation of the ID
        self.id = dict.get("id",0)

        #empty means that we may be adding a new category
        if self.id == '':
            self.id = 0     

        #attempt to convert it to int. This is important just to validate the that data is correct.
        if not isinstance(self.id , int):
            try:
                self.id = int(self.id)
            except ValueError:
                raise ValueError(f"Invalid category dictionary ID value. Expected an integer value. Found: {self.id }")
            
        self.category_name = dict['category_name']

    def to_dictionary(self):
        '''
        returns a dictionary representation of this object.        
        '''
        return self.__dict__
    
    def update_from_category(self, cat):
        '''
        updates this property from another property of type category
        '''
        self.category_name = cat.category_name