from business_rules.device import Device
import json

class Device_Manager:
    '''
    Class that manage the data access to multiple devices
    '''

    @staticmethod
    def add_edit_device(device:Device):
        '''
          Adds/Edit a device 
        '''              
        devices_col =  Device_Manager.get_all_devices() 
        #innit de devices collection if needed  
        if not devices_col:
            devices_col = []  

        if not device.id or device.id == '': 
            #check that the device is new, then add it. 

            #we need to determine the ID for this new device  

            max_device = None 
            if len(devices_col) > 0:
                max_device = max(devices_col, key=lambda x: x.id) 
            if max_device:
                next_id = max_device.id + 1                
            else:
                next_id = 1 
            device.id = next_id

            #addd to the devices col
            devices_col.append(device)            
        else:
            #if the device exists just update 
            pass        
        Device_Manager.store_device_col(devices_col)
    

    @staticmethod    
    def store_device_col(devices_col):
        '''
          This acts as a database update.
          Given a list of devices it will dump the list into the 'database', a file named devices.json
        ''' 
        devices_json = json.dumps(devices_col, default=lambda o: o.__dict__)
        with open("db/devices.json", "w") as devices_file:
            devices_file.write(devices_json)

    @staticmethod  
    def delete_device_by_id(device_id:int):
        '''
        This acts as a database delete.
        Given a device id it will remove it from the 'database'
        '''
        devices_col = Device_Manager.get_all_devices() 
        found_device = next((e for e in devices_col if e.id == device_id),None)
        if found_device:
            devices_col.remove(found_device)
            Device_Manager.store_device_col(devices_col)

    @staticmethod
    def get_device_by_id(device_id:int):
        '''
        Gets a device by id.
        Returns: the device object if exists, otherwise it returns None
        '''        
        devices_col = Device_Manager.get_all_devices()
        device = next((e for e in devices_col if e.id == device_id),None) 
        return device    
           
    @staticmethod
    def get_all_devices():
        '''
          Retrieves all the devices from the  'database'
        '''
        devices_col = []
        with open("db/devices.json", "r") as devices_file:
            devices_json = json.load(devices_file)  
            for p in devices_json:
                device = Device()
                device.load_from_dictionary(p)
                devices_col.append(device)      
        return devices_col
            
    
    @staticmethod
    def validate_device_dict(device_dict):
        '''
           Validates the information of a device dict.
           Makes sure that device name is present. Device name must also be unique.

           Input: Receives a device dictionary
           Returns: a tuple with 3 values. ([Validation passed or not], [Validation message], [Name of the input that failed])
        '''
        
        #device name is required
        device_name = device_dict.get('device_name','')
        if (device_name is None or device_name == ""):
            return  False, 'Device name is required', 'device_name'
        
        #check device name already exists
        found_device = next((e for e in Device_Manager.get_all_devices() if e.device_name == device_name), None)
        if found_device:
            return  False, 'Device name already exists', 'device_name'
        
        return True, '', ''
    