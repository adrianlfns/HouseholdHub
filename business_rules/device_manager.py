class Device_Manager:
    '''
    Class that manage the data access to multiple devices
    '''

    @staticmethod
    def add_edit_device(device):
        '''
          Adds/Edit a device to the 'database'
        '''
        pass

    @staticmethod
    def get_all_devices():
        '''
          Retrieves all the devices from the  'database'
        '''
        pass
    
    @staticmethod
    def validate_device_dict(device_dict):
        '''
           Validates the information of a device dict.

           Input: Recevices a device dictionary
           Returns: a tuple with 3 values. ([Validation passed or not], [Validation message], [Name of the input that failed])
        '''
        
        #device name is required
        device_name = device_dict.get('device_name','')
        if (device_name is None or device_name == ""):
            return  False, 'Device name is required', 'device_name'
        
              

        
        return True, '', ''



    