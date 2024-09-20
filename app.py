'''
For flask documentation see https://flask.palletsprojects.com/en/3.0.x/
'''

import flask 
from business_rules.device_manager import Device_Manager #imports a package from the module device_manager, the class Device_Manager is used for every data access with the device.
from business_rules.device import Device

app = flask.Flask(__name__, static_url_path='/static')

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
    return flask.render_template('mydevices.html') #see templates directory for corresponding template

@app.get("/add_edit_device")
def add_edit_device_get():
    '''
    entry route for adding/editing devices
    '''
    return flask.render_template('add_edit_device.html')

@app.post("/add_edit_device")
def add_edit_device_post():
    '''
    POST route for receiving device information
    '''

    #collect the post data in a dictionary
    post_data_collected = {
    'device_name': flask.request.form.get("device_name"),      
    'device_make': flask.request.form.get("device_make"),
    'device_model':flask.request.form.get("device_model"),
    'purchase_price_dollars':  flask.request.form.get("purchase_price_dollars"),
    'purchase_store': flask.request.form.get("purchase_store"),
    'purchase_date':flask.request.form.get("purchase_date"),
    'guaranty_expiration_date': flask.request.form.get("guaranty_expiration_date"),
    'guaranty_notes': flask.request.form.get("guaranty_notes")
    }  

    is_valid, validation_error, invalid_input_name = Device_Manager.validate_device_dict(post_data_collected)

    if not is_valid:
        return flask.render_template('add_edit_device.html', data=post_data_collected, validation_error=validation_error, invalid_input_name=invalid_input_name)
   

    #create a device object
    device = Device()
    device.name = post_data_collected["device_name"]
    device.make = post_data_collected["device_make"]
    device.model = post_data_collected["device_model"]
    device.purchase_price_dollars = post_data_collected["purchase_price_dollars"]
    device.purchase_store = post_data_collected["purchase_store"]
    device.purchase_date = post_data_collected["purchase_date"]
    device.guaranty_expiration_date = post_data_collected["guaranty_expiration_date"]
    device.guaranty_notes = post_data_collected["guaranty_notes"]
    
    return flask.render_template('add_edit_device.html')


#this line runs and initialize flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True) 


