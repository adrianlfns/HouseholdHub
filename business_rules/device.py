class Device:
    '''
    Class that represents the information of a single device
    '''

    def __init__(self):

        #general information of the device
        self.id:int =  None #internal id for the device
        self.device_name = ''
        self.category_id:int = None #internal id for the category
        self.device_make = ''
        self.device_model = ''

        #purchase information of the device
        self.purchase_price_dollars = 0.0
        self.purchase_store = ''
        self.purchase_date = None

        #guaranty information of the device
        self.guaranty_expiration_date = None
        self.guaranty_notes = None

        #references to documents
        self.manuals_doc_ref = [] 
        self.purchase_receipt_doc_ref = []
        self.guaranty_doc_ref = []

    def to_dictionary(self):
        '''
        returns a dictionary representation of this object.        
        '''
        return self.__dict__

    def update_from_dictionary(self, dict:dict):
        '''
        update all the properties from a dictionary
        '''

        #small sanitation of the ID
        self.id = dict.get("id",0)

        #empty means that we may be adding a new device
        if self.id == '':
            self.id = 0      
        
        #attempt to convert it to int. This is important just to validate the that data is correct.
        if not isinstance(self.id , int):
            try:
                self.id = int(self.id)
            except ValueError:
                raise ValueError(f"Invalid device dictionary ID value. Expected an integer value. Found: {self.id }")
            
        #small sanitation to the category id
        self.category_id = dict.get("category_id",0)
        if self.category_id == '':
            self.category_id = 0
        
        if not isinstance(self.category_id, int):
            try:
                self.category_id = int(self.category_id)
            except ValueError:
                raise ValueError(f"Invalid device category ID value. Expected and integer value. Found: {self.category_id}")                    

        self.device_name = dict["device_name"]        
        self.device_make = dict["device_make"]
        self.device_model = dict["device_model"]
        self.purchase_price_dollars = dict["purchase_price_dollars"]
        self.purchase_store = dict["purchase_store"]
        self.purchase_date = dict["purchase_date"]
        self.guaranty_expiration_date = dict["guaranty_expiration_date"]
        self.guaranty_notes = dict["guaranty_notes"]
        

    def update_from_device(self, dev):
        '''
        updates this property from another property of type device
        '''
        self.device_name = dev.device_name
        self.category_id = dev.category_id
        self.device_make = dev.device_make
        self.device_model = dev.device_model
        self.purchase_price_dollars = dev.purchase_price_dollars
        self.purchase_store = dev.purchase_store
        self.purchase_date = dev.purchase_date
        self.guaranty_expiration_date = dev.guaranty_expiration_date
        self.guaranty_notes = dev.guaranty_notes



