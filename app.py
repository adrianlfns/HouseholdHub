'''
Initial module for initializing the flask app
For flask documentation see https://flask.palletsprojects.com/en/3.0.x/
'''

import flask 
 
from routes_blueprints.home_blueprint import home_blueprint
from routes_blueprints.categories_blueprint import categories_blueprint
from routes_blueprints.devices_blueprint import devices_blueprint


app = flask.Flask(__name__, static_url_path='/static')
app.secret_key = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcb1'


#Blueprints registration. 
#Blueprints are simply modules where related code can be placed.
#Blueprints are very helpful for organization.
#see blueprint documentation https://flask.palletsprojects.com/en/stable/blueprints/
app.register_blueprint(home_blueprint)
app.register_blueprint(categories_blueprint)
app.register_blueprint(devices_blueprint)
 

#this line runs and initialize flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True) 


