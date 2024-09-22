'''
For flask documentation see https://flask.palletsprojects.com/en/3.0.x/
'''

import flask 
from business_rules.device_manager import Device_Manager #imports a package from the module device_manager, the class Device_Manager is used for every data access with the device.
from business_rules.device import Device

app = flask.Flask(__name__, static_url_path='/static')
app.secret_key = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcb1'

@app.get("/")
def home():
    '''
    Initial route to land on the home page
    '''
    return flask.render_template('home.html') #see templates directory for corresponding template

@app.get("/mydevices")
def mydevices():
    '''
    route for managing devices
    '''
    devices_col = Device_Manager.get_all_devices()
    return flask.render_template('mydevices.html',devices_col=devices_col) #see templates directory for corresponding template

@app.get("/add_edit_device/")
@app.get("/add_edit_device/<device_id>")
def add_edit_device_get(device_id:int=None):
    '''
    entry route for adding/editing devices
    '''
    data=None
    if device_id:
        device_id = int(device_id)
        device = Device_Manager.get_device_by_id(device_id)
        if not device:
            raise Exception(f"Device with ID {device_id} not found.")
        data = device.to_dictionary()

    return flask.render_template('add_edit_device.html',data=data)

@app.post("/remove_device")
def remove_device():
    '''
    POST route for removing a device
    '''
    device_id = flask.request.form.get("device_id",0)  
    if device_id:       
        device_id = int(device_id)
        Device_Manager.delete_device_by_id(device_id)
        return flask.redirect("/mydevices")
    

@app.post("/add_edit_device")
def add_edit_device_post():
    '''
    POST route for receiving device information
    '''
    #collect the post data in a dictionary (uses dictionary comprehension)
    post_data_collected = {k:flask.request.form.get(k) for k in flask.request.form}  

    is_valid, validation_error, invalid_input_name = Device_Manager.validate_device_dict(post_data_collected)

    if not is_valid:
        return flask.render_template('add_edit_device.html', data=post_data_collected, validation_error=validation_error, invalid_input_name=invalid_input_name)
   

    #create a device object
    device = Device()
    device.load_from_dictionary(post_data_collected)
    
    #add or edit the dictionary in the storage
    Device_Manager.add_edit_device(device)
    
    #set a flash message for another request. In this case /mydevices will consume the flashed messages. 
    flask.flash('New device added.')
    
    #go back to my devices
    return flask.redirect("/mydevices")


#this line runs and initialize flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True) 


