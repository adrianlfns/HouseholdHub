class Device:
    '''
    Class that represents the information of a single device
    '''

    def __init__(self):

        #general information of the device
        self.name = None
        self.category = None
        self.make = None
        self.model = None

        #purchase information of the device
        self.purchase_price = None
        self.purchase_store = None
        self.purchase_date = None

        #guaranty information of the device
        self.guaranty_expiration_date = None
        self.guaranty_notes = None

        #references to documents
        self.manuals_doc_ref = [] 
        self.purchase_receipt_doc_ref = []
        self.guaranty_doc_ref = []

