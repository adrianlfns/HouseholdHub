import flask

from routes_bluprints import route_utils

from business_rules.device_manager import Device_Manager #imports a package from the module device_manager, the class Device_Manager is used for every data access with the device.
from business_rules.device import Device

from business_rules.categories_manager import Categories_Manager
from business_rules.category import Category

#this creates the home blueprint object. See app.py for registration
home_blueprint = flask.Blueprint('home_blueprint',__name__,static_url_path='/static')



@home_blueprint.get("/")
@home_blueprint.get("/home")
@home_blueprint.get("/dashboard")
def home():
    '''
    Initial route to land on the home page.
    This page contains a couple of dashboards
    '''    
    try:
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
    except:        
        return route_utils.handle_route_error()
    
