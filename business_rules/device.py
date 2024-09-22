class Device:
    '''
    Class that represents the information of a single device
    '''

    def __init__(self):

        #general information of the device
        self.id:int =  None #internal id
        self.device_name = ''
        self.category = None
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

    def load_from_dictionary(self, dict:dict):
        '''
        loads all the properties from a dictionary
        '''
        self.id = dict.get("id",0)
        self.device_name = dict["device_name"]
        self.device_make = dict["device_make"]
        self.device_model = dict["device_model"]
        self.purchase_price_dollars = dict["purchase_price_dollars"]
        self.purchase_store = dict["purchase_store"]
        self.purchase_date = dict["purchase_date"]
        self.guaranty_expiration_date = dict["guaranty_expiration_date"]
        self.guaranty_notes = dict["guaranty_notes"]



