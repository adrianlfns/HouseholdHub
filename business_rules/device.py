class Device:
    '''
    Class that represents the information of a single device
    '''

    def __init__(self):

        #general information of the device
        self.id =  None #internal id
        self.name = ''
        self.category = None
        self.make = ''
        self.model = ''

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

