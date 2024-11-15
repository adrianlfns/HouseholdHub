import flask
import os

from routes_blueprints.route_utils import handle_route_error, handle_route_invalid_request

from business_rules.expiration_types_lookup import ExpirationTypeLookup
from business_rules.device_manager import Device_Manager #imports a package from the module device_manager, the class Device_Manager is used for every data access with the device.
from business_rules.device import Device
from business_rules.categories_manager import Categories_Manager

from routes_blueprints.route_utils import handle_route_error


#this creates the devices blueprint object. See app.py for registration
devices_blueprint = flask.Blueprint('devices_blueprint',__name__,static_url_path='/static')

  
@devices_blueprint.get("/my_devices")
def my_devices():
    '''
    Route for managing devices.
    It returns a view with a list of all devices.
    That view also contains filter capabilities (see search_device route)
    '''
    try:
        #capture and clean up the category_id parameter
        try:
            selected_category_id = int(flask.request.args.get("category_id",0))
        except:
            return handle_route_invalid_request()

        #capture and clean up the expiration type parameter
        try:
            expiration_type_id = int(flask.request.args.get("expiration_type_id",0))
        except:
            return handle_route_invalid_request()
        
        if not ExpirationTypeLookup.IsValidExpirationTypeID(expiration_type_id):
            return handle_route_invalid_request()


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
                                    expiration_type_col=expiration_type_col,
                                    expiration_type_id=expiration_type_id) #see templates directory for corresponding template
    except:
        return handle_route_error()

@devices_blueprint.get("/search_device")
def search_device():
    '''
     This route is suitable to make asynchronous AJAX requests. 
     It allows filtering devices by category and by a portion of the name.
    ''' 
    try:
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
    except:
        return handle_route_error()


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

@devices_blueprint.get("/add_edit_device/")
@devices_blueprint.get("/add_edit_device/<device_id>")
def add_edit_device_get(device_id:int=None):
    '''
    Entry route for adding/editing devices
    Note: if device_id ==0 or device_id == NONE, it will be treated as insert.
          if device_id > 0 it will be treated as edit.
    '''
    try:
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
    except:
        handle_route_error()

@devices_blueprint.post("/remove_device")
def remove_device():
    '''
    POST route for removing a device
    '''
    try:
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
    except:
        return handle_route_error()
  

def process_post_data_dictionary(post_data_collected:dict):
    '''
    Process and transform POST variables related to document 
    '''
    #get all keys related to documents
    document_related_keys = [i.replace("document_name_","") for i in post_data_collected.keys() if i.startswith("document_name_")]
    for key in document_related_keys:

        doc_name_dict_key = "document_name_" + key
        doc_url_dict_key = "document_url_" + key

        document_name = post_data_collected.get(doc_name_dict_key,'')
        document_url = post_data_collected.get(doc_url_dict_key,'')

        #validate that the file comes in the post
        file_name_key = 'document_upload_' + key
        if file_name_key in flask.request.files:
            file = flask.request.files[file_name_key]
            
            #obtain the file extension       
            file_split = os.path.splitext(file.filename)
            file_ext = file_split[1]
            if not file_ext:
                file_ext = ''
            
            #create the docs storage directory if needed
            doc_dir = os.path.join('db','docs')        
            if not os.path.isdir(doc_dir):
                os.mkdir(doc_dir)
        
            #store the file in db/docs/
            file_name_key = file_name_key + file_ext
            file.save(os.path.join(doc_dir,file_name_key))
        else:
            file_name_key = ''

        #prepare the dictionary 
        doc_list = post_data_collected.get('document_references',[])
        doc_list.append({
            'doc_ref_id':key,
            'doc_name':document_name,
            'doc_url':document_url,
            'doc_file_name':file_name_key
        })
        post_data_collected['document_references'] = doc_list

        #clean up entries
        if doc_name_dict_key in post_data_collected:
            del post_data_collected[doc_name_dict_key]
        
        if doc_url_dict_key in post_data_collected:
            del post_data_collected[doc_url_dict_key]
        

@devices_blueprint.post("/add_edit_device")
def add_edit_device_post():
    '''
    POST route for receiving device information.
    This is executed when a new device is added or edited
    '''
    try:
        #collect the post data in a dictionary (uses dictionary comprehension)
        post_data_collected = {k:flask.request.form.get(k) for k in flask.request.form}  

        is_valid, validation_error, invalid_input_name = Device_Manager.validate_device_dict(post_data_collected)

        if not is_valid:
            categories_col = Categories_Manager.get_all_categories()
            return flask.render_template('add_edit_device.html', data=post_data_collected, validation_error=validation_error, invalid_input_name=invalid_input_name, categories_col=categories_col)
    
        #process documents
        process_post_data_dictionary(post_data_collected)  

        #create a device object
        device = Device()
        device.update_from_dictionary(post_data_collected)
        
        #add or edit the dictionary in the storage
        device, device_added = Device_Manager.add_edit_device(device, docs_to_delete=post_data_collected.get('deleted_docs',''))
        
        #set a flash message for another request. In this case /my_devices will consume the flashed messages.
        if device_added:
            flask.flash(f'The new device was successfully added. The new device name is "{device.device_name}".')
        else:
            flask.flash(f'The device was successfully edited.')
            
        
        #go back to my devices    
        return flask.redirect("/my_devices")
    except:
        return handle_route_error()
 

@devices_blueprint.get("/device_document_download")
def device_document_download():
    '''
    Downloads a device document.
    Expected get parameters: device_id:int and doc_ref_id:str
    '''
    try:
        device_id = flask.request.args.get("device_id",0)
        try:
            device_id = int(device_id)
        except ValueError:
            raise ValueError(f"Invalid get data. Expected parameter device_id to be int.")
        
        if device_id<=0:
            raise ValueError(f"Invalid get data. Expected parameter device_id to be greater than zero.")
        
        doc_ref_id = flask.request.args.get("doc_ref_id",'')
        if doc_ref_id.strip() == '':
            raise ValueError(f"Invalid get data. Expected parameter doc_ref_id to be not empty.")
        
        device:Device = Device_Manager.get_device_by_id(device_id=device_id)
        if not device:
            raise ValueError(f"Unable to find device with ID {device_id}")
        
        doc_ref = device.find_doc_ref_by_key(doc_ref_id)
        if not doc_ref:
            raise ValueError(f"Unable to find document reference with id {doc_ref_id} in device with id {device_id}")
        
        return flask.send_file(path_or_file= os.path.join('db','docs',doc_ref['doc_file_name']) , as_attachment=True) 
    except:
        handle_route_error()