from business_rules.entity_base import EntityBase
from datetime import datetime
import os

class Device (EntityBase):
    '''
    Class that represents the information of a single device
    '''

    def __init__(self):
        EntityBase.__init__(self)

        #general information of the device        
        self.device_name = ''
        self.category_id:int = None #internal id for the category
        self.category_name:str = '' #this field will be filled only when needed
        self.device_make = ''
        self.device_model = ''

        #purchase information of the device
        self.purchase_price_dollars = 0.0
        self.purchase_store = ''
        self.purchase_date = None

        #warranty information of the device
        self.warranty_expiration_date = None
        self.warranty_notes = None

        #references to documents
        self.document_references = [] 

    @property
    def warranty_expiration_date_formatted(self, empty_value='Unknown'):
        '''
        returns the warranty expiration date in a friendly format.
        returns an empty value if the date is empty.
        '''

        if not self.warranty_expiration_date or self.warranty_expiration_date =='':
            return empty_value       
 
        date = self.warranty_expiration_date_to_datetime # datetime.strptime(self.warranty_expiration_date,'%Y-%m-%d')      
        
        return date.strftime("%A %B %d %Y")
    
    @property
    def warranty_expiration_date_to_datetime(self):
        '''
        converts warranty_expiration_date to datetime
        '''
        return datetime.strptime(self.warranty_expiration_date,'%Y-%m-%d')  
    
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
        self.warranty_expiration_date = dict.get("warranty_expiration_date",'')
        self.warranty_notes = dict.get("warranty_notes",'')

        document_references = dict.get('document_references',[])
        for i in document_references:
            self.document_references.append(i)
        

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
        self.warranty_expiration_date = dev.warranty_expiration_date
        self.warranty_notes = dev.warranty_notes

        for i in dev.document_references:
            self.document_references.append(i)

    def remove_doc_by_key(self,doc_key:str):
        '''
        Removes the documents a device given the key
        '''
        doc_to_delete = next((e for e in self.document_references if e['doc_ref_id'] == doc_key), None)
        self.remove_single_doc(doc_to_delete)
              
    
    def remove_single_doc(self, doc_to_delete):
        '''
        Remove a single document
        '''
        if doc_to_delete:            
              self.document_references.remove(doc_to_delete)                   
              try:
                os.remove(os.path.join('db','docs',doc_to_delete['doc_file_name']))
              except:
                  pass      

              
    def remove_all_docs(self):
        '''
        Clears all documents from a device given the key
        '''
        while len(self.document_references) > 0:
            doc_to_delete = self.document_references[0]
            self.remove_single_doc(doc_to_delete)








