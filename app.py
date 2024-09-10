'''
For flask documentation see https://flask.palletsprojects.com/en/3.0.x/
'''

import flask 
from business_rules.device_manager import Device_Manager #imports a package from the module device_manager, the class Device_Manager is used for every data access with the device.

app = flask.Flask(__name__, static_url_path='/static')

@app.route("/")
def home():
    '''
    Initial route to land on the home page
    '''
    return flask.render_template('home.html') #see templates directory for corresponding template

@app.route("/mydevices")
def mydevices():
    '''
    route for managing devices
    '''
    return flask.render_template('mydevices.html') #see templates directory for corresponding template

@app.route("/add_edit_device")
def add_edit_device():
    '''
    route for adding/editing devices
    '''
    return flask.render_template('add_edit_device.html')


#this line runs and initialize flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True) 


