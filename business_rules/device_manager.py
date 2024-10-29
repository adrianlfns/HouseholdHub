from business_rules.device import Device
from business_rules.entity_base import EntityBase
from business_rules.category_count import CategoryCount
import json
import os
from datetime import datetime

class Device_Manager:
    '''
    Class that manage the data access and business logic for devices.
    '''

    WARRANTY_EXPIRATION_STATUS_EXPIRED = 1    
    WARRANTY_EXPIRATION_STATUS_EXPIRES_YEAR = 2
    WARRANTY_EXPIRATION_STATUS_EXPIRES_YEAR_PLUS = 3
    WARRANTY_EXPIRATION_STATUS_EXPIRES_UNKNOWN = 4

    DEVICE_FILE_PATH = os.path.join('db','devices.json') #"db/devices.json"  'constant' to know the path where the data for the device is located'

    @staticmethod
    def get_all_devices():
        '''
          Retrieves all the devices from the  'database'
        '''
        devices_col = []

        #just in case, check if the file exists
        file_name = Device_Manager.DEVICE_FILE_PATH
        if not os.path.exists(file_name):
            return devices_col
        
        #just in case, check for file to be empty. If is empty. just return an empty list        
        if os.stat(file_name).st_size == 0:
            return devices_col

        #open an read the JSON file
        with open(file_name, "r") as devices_file:
            devices_json = json.load(devices_file)  
            for p in devices_json:
                device = Device()
                device.update_from_dictionary(p)
                devices_col.append(device)      
        return devices_col
    
    @staticmethod
    def get_devices_by_category_id(category_id:int, devices_col:list = None):
        '''
        Finds all the devices that belong to a category given a category list.

        '''
        if not devices_col:
            devices_col = Device_Manager.get_all_devices()

        return list(filter(lambda x: x.category_id == category_id, devices_col))
    

    @staticmethod
    def get_device_count_by_categories(devices_col:list = None):
        """
        Returns a number of devices per each category ID.
        See class CategoryCount in module category_count
        """        
        if not devices_col:
            devices_col = Device_Manager.get_all_devices()

        category_count = {}

        for device in devices_col:
            current_count = category_count.get(device.category_id,0)
            category_count[device.category_id] = current_count + 1 
        
        return [CategoryCount(category_id=device_id, device_count=count) for (device_id, count) in category_count.items()]
    
    @staticmethod
    def get_device_count_by_warranty_expiration(devices_col:list = None):
        """
        Returns a number of devices per different expiration types
        """ 
        if not devices_col:
            devices_col = Device_Manager.get_all_devices()
        
        device_count_by_warranty_expiration = {}  

        today_date = datetime.today() 
        year_from_today =  today_date.replace(year=today_date.year + 1) 

        for device in devices_col:
            if not device.warranty_expiration_date or device.warranty_expiration_date == "":
                device_count_by_warranty_expiration[Device_Manager.WARRANTY_EXPIRATION_STATUS_EXPIRES_UNKNOWN] = device_count_by_warranty_expiration.get(Device_Manager.WARRANTY_EXPIRATION_STATUS_EXPIRES_UNKNOWN,0) + 1
            else:
                expiration_date = datetime.strptime(device.warranty_expiration_date,'%Y-%m-%d')
                               
                if expiration_date <= today_date:
                    device_count_by_warranty_expiration[Device_Manager.WARRANTY_EXPIRATION_STATUS_EXPIRED] = device_count_by_warranty_expiration.get(Device_Manager.WARRANTY_EXPIRATION_STATUS_EXPIRED,0) + 1
                else:                 
                    if (expiration_date <= year_from_today):
                        device_count_by_warranty_expiration[Device_Manager.WARRANTY_EXPIRATION_STATUS_EXPIRES_YEAR] = device_count_by_warranty_expiration.get(Device_Manager.WARRANTY_EXPIRATION_STATUS_EXPIRES_YEAR,0) + 1
                    else:
                        device_count_by_warranty_expiration[Device_Manager.WARRANTY_EXPIRATION_STATUS_EXPIRES_YEAR_PLUS] = device_count_by_warranty_expiration.get(Device_Manager.WARRANTY_EXPIRATION_STATUS_EXPIRES_YEAR_PLUS,0) + 1

        return device_count_by_warranty_expiration



           

    


    @staticmethod
    def get_new_device_key(devices_col = None):
        '''
        Generates a new device ID.
        '''
        if not devices_col:
            devices_col = Device_Manager.get_all_devices()

        return EntityBase.get_new_entity_key(devices_col)
        

    @staticmethod
    def add_edit_device(device:Device):
        '''
          Adds/Edit a device, it depends on the ID that was passed.
          Parameter: device to be added or edited.

          If the device passed has an 'empty' or zero or None id, perform an add.
          IF the device passed has an id > 0, perform and edit.

          Returns: a tuple with tow values: the device that was added/edited and a flag that indicates that the device was added.
        '''              
        devices_col =  Device_Manager.get_all_devices() 
        #innit de devices collection if needed  
        if not devices_col:
            devices_col = []  
        
        device_added = False         

        #check that the device is new, then add it.
        if not device.id or device.id == '' or device.id == 0:
            #we need to determine the ID for this new device             
            device.id = Device_Manager.get_new_device_key()

            #addd to the devices col
            devices_col.append(device)
            device_added = True            
        else:
            #if the device exists just update       
            device_to_edit:Device = Device_Manager.get_device_by_id(device_id=device.id, devices_col=devices_col)   
            if not device_to_edit:
                raise ValueError(f"Device with id {device.id} not found.")
            device_to_edit.update_from_device(device)
            device = device_to_edit

        #stores the device
        Device_Manager.store_device_col(devices_col)

        return device, device_added
    

    @staticmethod    
    def store_device_col(devices_col):
        """
          This acts as a database update. \n
          Given a list of devices it will dump the list into the 'database', a file named devices.json
        """ 
        devices_json = json.dumps(devices_col, default=lambda o: o.__dict__, indent=2)
        with open(Device_Manager.DEVICE_FILE_PATH, "w") as devices_file:
            devices_file.write(devices_json)

    @staticmethod  
    def delete_device(device:Device):
        '''
        This acts as a database delete.
        Given a device it will remove it from the 'database'
        '''
        device_id = device.id
        devices_col = Device_Manager.get_all_devices() #obtain the devices from the database 
        found_device = Device_Manager.get_device_by_id(device_id=device_id, devices_col=devices_col) 
        if found_device:
            devices_col.remove(found_device)
            Device_Manager.store_device_col(devices_col)

    @staticmethod
    def get_device_by_id(device_id:int, devices_col:list = None):
        '''
        Gets a device by id. \n
        Parameters:
                device_id (int) - the Id of the device
                devices_col - a collection of devices. If the collection is None. Retrieve the collection of devices from the database.
        Returns: the device object if exists, otherwise it returns None
        '''
        if devices_col is None: 
            devices_col = Device_Manager.get_all_devices()
        device = next((e for e in devices_col if e.id == device_id),None) 
        return device 
    

    @staticmethod
    def validate_device_dict(device_dict):
        '''
           Validates the information of a device dict.
           Makes sure that device name is present. Device name must also be unique.

           Input: Receives a device dictionary
           Returns: a tuple with 3 values. ([Validation passed or not], [Validation message], [Name of the key that failed])
        '''
        
        #device name is required
        device_name = device_dict.get('device_name','')
        if (device_name is None or device_name == ""):
            return  False, 'Device name is required', 'device_name'
        
        device_id = device_dict.get('id','')
        
        #check device name already exists for in other devices
        found_device = next((e for e in Device_Manager.get_all_devices() if e.device_name == device_name and str(e.id) != device_id), None)
        if found_device:
            return  False, 'Device name already exists', 'device_name'
        
        #category is required
        category_id = device_dict.get('category_id',0)
        if category_id == 0 or category_id is None or category_id == '':
            return  False, 'Category is required.', 'category_id'
        
        
        
        return True, '', ''
    