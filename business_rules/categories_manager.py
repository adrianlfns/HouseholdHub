import json
import os
from business_rules.category import Category
from business_rules.device_manager import Device_Manager

class Categories_Manager:
    '''
    Class that manages the data access and business logic for categories.
    '''

    CATEGORIES_FILE_PATH = "db/categories.json" #'constant to know the path where the data for the device is located'

    @staticmethod
    def get_all_categories():
        '''
          Retrieves all the categories from the 'database'
        '''
        categories_col = []

        #just in case, check for file to be empty. If is empty. just return an empty list
        file_name = Categories_Manager.CATEGORIES_FILE_PATH
        if os.stat(file_name).st_size == 0:
            return categories_col

        #open the file and parse the json content
        with open(file_name, "r") as categories_file:
            categories_json = json.load(categories_file)  
            for p in categories_json:
                category = Category()
                category.update_from_dictionary(p)
                categories_col.append(category) 

        categories_col.sort(key=lambda p: p.category_name) #output the category sorted by name
        return categories_col
    
    
    @staticmethod
    def get_category_by_id(category_id:int, categories_col:list = None):
        '''
        Gets a category by id. \n
        Parameters:
                category_id (int) - the Id of the category
                categories_col - a collection of categories. If the collection is None. Retrieve the collection of devices from the database.
        Returns: the category object if exists, otherwise it returns None
        '''
        if categories_col is None: 
            categories_col = Categories_Manager.get_all_categories()
        category = next((e for e in categories_col if e.id == category_id),None) 
        return category 

    @staticmethod  
    def delete_category(category:Category):
        '''
        This acts as a database delete.
        Given a device it will remove it from the 'database'

        returns: a tuple with two values:  
           First tuple value is a boolean reporting success.
           Second tuple value is a message.
        '''
        category_id = category.id
        categories_col = Categories_Manager.get_all_categories() #obtain the category from the database 
        found_category = Categories_Manager.get_category_by_id(category_id=category_id, categories_col=categories_col) 
        if found_category:
            #validation that makes sure that the category is not in use by a device
            devices =Device_Manager.get_devices_by_category_id(category_id=found_category.id)
            if len(devices) > 0:
                return (False, f'The category "{found_category.category_name}" can not be deleted because it is in use by one or more devices.')

            categories_col.remove(found_category)
            Categories_Manager.store_category_col(categories_col) 

        return (True, "")
        

    @staticmethod
    def validate_category_dict(category_dict):
        '''
           Validates the information of a category dict.
           Makes sure that category name is present. Category name must also be unique.

           Input: Receives a category dictionary
           Returns: a tuple with 3 values. ([Validation passed or not], [Validation message], [Name of the key that failed])
        '''

        #category name is required
        category_name = category_dict.get('category_name','')
        if (category_name is None or category_name == ""):
            return  False, 'Category name is required', 'category_name'
        
        category_id = category_dict.get('id','')
        
        #check category name already exists for in other devices
        found_category= next((e for e in Categories_Manager.get_all_categories() if e.category_name == category_name and str(e.id) != category_id), None)
        if found_category:
            return  False, 'Category name already exists', 'category_name'
        
        return True, '', ''
    
    @staticmethod
    def add_edit_category(category:Category): 
        '''
          Adds/Edit a category, it depends on the ID that was passed.
          Parameter: category to be added or edited.

          If the category passed has an 'empty' or zero or None id, perform an add.
          IF the category passed has an id > 0, perform and edit.

          Returns: a tuple with tow values: the device that was added/edited and a flag that indicates that the device was added.
        '''  
        categories_col =  Categories_Manager.get_all_categories() 
        #innit de devices collection if needed  
        if not categories_col:
            categories_col = []  
        
        category_added = False         

        #check that the device is new, then add it.
        if not category.id or category.id == '' or category.id == 0:
            #we need to determine the ID for this new device             
            category.id = Categories_Manager.get_new_category_key()

            #addd to the devices col
            categories_col.append(category)
            category_added = True            
        else:
            #if the device exists just update       
            category_to_edit:Category = Categories_Manager.get_category_by_id(category_id=category.id, categories_col=categories_col)   
            if not category_to_edit:
                raise ValueError(f"Category with id {category.id} not found.")
            category_to_edit.update_from_category(category)
            category = category_to_edit

        #stores the device
        Categories_Manager.store_category_col(categories_col)

        return category, category_added
    
    @staticmethod
    def get_new_category_key(categories_col = None):
        '''
        Generates a new category ID.
        '''
        if not categories_col:
            categories_col = Categories_Manager.get_all_categories()
        
        max_category = None 
        if len(categories_col) > 0:
            max_category = max(categories_col, key=lambda x: x.id) 
            if max_category:
                next_id = max_category.id + 1                
        else:
            next_id = 1

        return next_id  
    
    @staticmethod
    def store_category_col(categories_col):
        """
          This acts as a database update. \n
          Given a list of categories it will dump the list into the 'database', a file named categories.json
        """ 
        categories_json = json.dumps(categories_col, default=lambda o: o.__dict__, indent=2)
        with open(Categories_Manager.CATEGORIES_FILE_PATH, "w") as categories_file:
            categories_file.write(categories_json)






