import flask

from routes_blueprints.route_utils import handle_route_error

from business_rules.categories_manager import Categories_Manager
from business_rules.category import Category

#this creates the category blueprint object. See app.py for registration
categories_blueprint = flask.Blueprint('categories_blueprint',__name__,static_url_path='/static')

  


@categories_blueprint.get("/my_categories")
def my_categories():
    '''
    Route for managing categories
    '''
    try:
        categories_col = Categories_Manager.get_all_categories()
        return flask.render_template('my_categories.html',categories_col=categories_col)
    except:
        return handle_route_error()

@categories_blueprint.get("/add_edit_category/")
@categories_blueprint.get("/add_edit_category/<category_id>")
def add_edit_category_get(category_id:int=None):
    '''
    Entry route for adding/editing categories
    Note: if category_id ==0 or category_id == NONE, it will be treated as insert.
          if category_id > 0 it will be treated as edit.
    '''
    try:
        data=None
        if category_id:
            try:
                category_id = int(category_id)
            except ValueError:
                raise ValueError(f"Invalid post data. Expected parameter category_id to be int")
            
            if category_id < 0:
                raise ValueError(f"Invalid post data. Expected parameter category_id to be zero or greather than zero.")
            
            if category_id > 0:
                category = Categories_Manager.get_category_by_id(category_id)
                if not category:
                    raise ValueError(f"Category with ID {category_id} not found.")
                data = category.to_dictionary()   
            
        return flask.render_template('add_edit_category.html', data=data)
    except:
        return handle_route_error()
 
@categories_blueprint.post("/add_edit_category")
def add_edit_category_post():
    '''
    POST route for receiving category information
    '''
    try:
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
    except:
        return handle_route_error()

@categories_blueprint.post("/remove_category")
def remove_category():
    '''
    POST route for removing a category
    '''
    try:
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
    except:
        return handle_route_error()

