'''
For flask documentation see https://flask.palletsprojects.com/en/3.0.x/
'''

import flask 
from business_rules.device_manager import Device_Manager #imports a package from the module device_manager, the class Device_Manager is used for every data access with the device.
from business_rules.device import Device

from business_rules.categories_manager import Categories_Manager
from business_rules.category import Category

from business_rules.expiration_types_lookup import ExpirationTypeLookup

app = flask.Flask(__name__, static_url_path='/static')
app.secret_key = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcb1'

@app.get("/")
@app.get("/home")
@app.get("/dashboard")
def home():
    '''
    Initial route to land on the home page.
    This page contains a couple of dashboards
    '''

    #Dashboard section 1 - device count by categories
    device_count_by_cat_col = Device_Manager.get_device_count_by_categories()
    categories_col = Categories_Manager.get_all_categories()
    for device_count_by_cat in device_count_by_cat_col:
        category = Categories_Manager.get_category_by_id(category_id=device_count_by_cat.category_id, categories_col=categories_col)
        if category:
            device_count_by_cat.category_name = category.category_name 
            
    #Dashboard section 2 - device count by expiration date
    device_count_by_expiration_category = Device_Manager.get_device_count_by_warranty_expiration()

    
    return flask.render_template('home.html', 
                                 device_count_by_cat_col=sorted(device_count_by_cat_col, key=lambda a : a.category_name),
                                 device_count_by_expiration_category = device_count_by_expiration_category) #see templates directory for corresponding template


@app.get("/my_categories")
def my_categories():
    '''
    Route for managing categories
    '''    
    categories_col = Categories_Manager.get_all_categories()
    return flask.render_template('my_categories.html',categories_col=categories_col)

@app.get("/add_edit_category/")
@app.get("/add_edit_category/<category_id>")
def add_edit_category_get(category_id:int=None):
    '''
    Entry route for adding/editing categories
    Note: if category_id ==0 or category_id == NONE, it will be treated as insert.
          if category_id > 0 it will be treated as edit.
    '''
    data=None
    if category_id:
        try:
            category_id = int(category_id)
        except ValueError:
            raise ValueError(f"Invalid post data. Expected parameter category_id to be int")
        
        if category_id > 0:
            category = Categories_Manager.get_category_by_id(category_id)
            if not category:
                raise ValueError(f"Category with ID {category_id} not found.")
            data = category.to_dictionary()   
        
    return flask.render_template('add_edit_category.html', data=data)

 
@app.post("/add_edit_category")
def add_edit_category_post():
    '''
    POST route for receiving category information
    '''
    post_data_collected = {k:flask.request.form.get(k) for k in flask.request.form}  

    is_valid, validation_error, invalid_input_name = Categories_Manager.validate_category_dict(post_data_collected)

    if not is_valid:
        return flask.render_template('add_edit_category.html', data=post_data_collected, validation_error=validation_error, invalid_input_name=invalid_input_name)
    
    #create a device object
    category = Category()
    category.update_from_dictionary(post_data_collected)

    #add or edit the dictionary in the storage
    category, category_added = Categories_Manager.add_edit_category(category)

    #set a flash message for another request. In this case /my_devices will consume the flashed messages.
    if category_added:
        flask.flash(f'The new category was successfully added. The new category name is "{category.category_name}".')
    else:
        flask.flash(f'The category was successfully edited.')

    #go back to my devices
    return flask.redirect("/my_categories")



@app.post("/remove_category")
def remove_category():
    '''
    POST route for removing a category
    '''
    category_id = flask.request.form.get("category_id",0)  

    if not category_id:
        raise ValueError(f"Invalid post data. expected a parameter named category_id") 
       
    try:
        category_id = int(category_id)
    except ValueError:
          raise ValueError(f"Invalid post data. Expected parameter category_id to be int")
    
    if category_id <=0:
        raise ValueError(f"Invalid post data. Expected parameter category_id to be int > 0")
    
    category = Categories_Manager.get_category_by_id(category_id)

    if not category:
        raise ValueError(f"Category with id {category_id} not found.") 
    
    category_name = category.category_name
    success_ind, message = Categories_Manager.delete_category(category)

    if success_ind:
        flask.flash(f'The category "{category_name}" was successfully deleted.')
    else:
        flask.flash(message, category='error')

    return flask.redirect("/my_categories")


@app.get("/my_devices")
def my_devices():
    '''
    Route for managing devices.
    It returns a view with a list of all devices.
    That view also contains filter capabilities (see search_device route)
    '''

    #capture and clean up the category_id parameter
    try:
        selected_category_id = int(flask.request.args.get("category_id",0))
    except:
        selected_category_id = 0

    #capture and clean up the expiration type parameter
    try:
        expiration_type_id = int(flask.request.args.get("expiration_type_id",0))
    except:
        expiration_type_id = 0

    #filter the device
    devices_col = Device_Manager.query_devices(category_id=selected_category_id, expiration_type_id=expiration_type_id)


    #set the category name to the devices that will be rendered
    categories_col = Categories_Manager.get_all_categories()
    set_category_to_devices(devices_col, categories_col=categories_col)

    #load expiration types
    expiration_type_col = ExpirationTypeLookup.get_all_expiration_types()

    #render the template
    return flask.render_template('my_devices.html',
                                 devices_col=devices_col, 
                                 categories_col=categories_col,
                                 selected_category_id=selected_category_id,
                                 expiration_type_col=expiration_type_col) #see templates directory for corresponding template

@app.get("/search_device")
def search_device():
    '''
     This route is suitable to make asynchronous AJAX requests. 
     It allows filtering devices by category and by a portion of the name.
    '''   

    #prepare the category filter
    category_id = flask.request.args.get('category_id',0)
    if not category_id or category_id == '':
        category_id = 0
    category_id = int(category_id) 

    #prepare the expiration type
    expiration_type_id = flask.request.args.get('expiration_type_id',0) 
    if  not expiration_type_id or expiration_type_id == '':
        expiration_type_id = 0
    expiration_type_id = int(expiration_type_id)

    #prepare the device name filter
    device_name = flask.request.args.get('device_name','')
    if not device_name:
        device_name = ''
    device_name = device_name.strip()
    
    #filter the device
    devices_col = Device_Manager.query_devices(category_id=category_id, expiration_type_id=expiration_type_id, device_name=device_name) 

    set_category_to_devices(devices_col)
    
    return flask.render_template('devices_col.html',devices_col=devices_col) #see templates directory for corresponding template




def set_category_to_devices(devices_col, categories_col = None):
        '''
        Iterates over the list of devices and sets the category name
        '''

        if not categories_col:
            categories_col = Categories_Manager.get_all_categories()

        for device in devices_col:
            category = Categories_Manager.get_category_by_id(device.category_id, categories_col=categories_col)
            device.category_name = ''
            if category:
                device.category_name = category.category_name



@app.get("/add_edit_device/")
@app.get("/add_edit_device/<device_id>")
def add_edit_device_get(device_id:int=None):
    '''
    Entry route for adding/editing devices
    Note: if device_id ==0 or device_id == NONE, it will be treated as insert.
          if device_id > 0 it will be treated as edit.
    '''
    data=None
    if device_id:
        try:
            device_id = int(device_id)
        except ValueError:
          raise ValueError(f"Invalid post data. Expected parameter device_id to be int")
        
        if device_id > 0:
            device = Device_Manager.get_device_by_id(device_id)
            if not device:
                raise ValueError(f"Device with ID {device_id} not found.")
            data = device.to_dictionary()

    categories_col = Categories_Manager.get_all_categories()

    return flask.render_template('add_edit_device.html',data=data, categories_col=categories_col)

@app.post("/remove_device")
def remove_device():
    '''
    POST route for removing a device
    '''
    device_id = flask.request.form.get("device_id",0)  

    if not device_id:
        raise ValueError(f"Invalid post data. expected a parameter named device_id") 
       
    try:
        device_id = int(device_id)
    except ValueError:
          raise ValueError(f"Invalid post data. Expected parameter device_id to be int")
    
    if device_id <=0:
        raise ValueError(f"Invalid post data. Expected parameter device_id to be int > 0")
    
    device = Device_Manager.get_device_by_id(device_id)

    if not device:
        raise ValueError(f"Device with id {device_id} not found.") 
    
    device_name = device.device_name
    Device_Manager.delete_device(device)

    flask.flash(f'The device "{device_name}" was successfully deleted.')
    return flask.redirect("/my_devices")
   


@app.post("/add_edit_device")
def add_edit_device_post():
    '''
    POST route for receiving device information
    '''
    #collect the post data in a dictionary (uses dictionary comprehension)
    post_data_collected = {k:flask.request.form.get(k) for k in flask.request.form}  

    is_valid, validation_error, invalid_input_name = Device_Manager.validate_device_dict(post_data_collected)

    if not is_valid:
        categories_col = Categories_Manager.get_all_categories()
        return flask.render_template('add_edit_device.html', data=post_data_collected, validation_error=validation_error, invalid_input_name=invalid_input_name, categories_col=categories_col)
   

    #create a device object
    device = Device()
    device.update_from_dictionary(post_data_collected)
    
    #add or edit the dictionary in the storage
    device, device_added = Device_Manager.add_edit_device(device)
    
    #set a flash message for another request. In this case /my_devices will consume the flashed messages.
    if device_added:
        flask.flash(f'The new device was successfully added. The new device name is "{device.device_name}".')
    else:
        flask.flash(f'The device was successfully edited.')
        
    
    #go back to my devices    
    return flask.redirect("/my_devices")


#this line runs and initialize flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True) 


