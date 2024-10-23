class CategoryCount:
    '''
    Class for counting devices by category.
    '''

    def __init__(self, category_id:int, device_count:int, category_name:str = ''):
         self.category_id = category_id
         self.category_name = category_name
         self.device_count = device_count


