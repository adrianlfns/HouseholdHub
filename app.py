'''
See minimal flask application https://flask.palletsprojects.com/en/3.0.x/quickstart/#a-minimal-application
'''

import flask 

app = flask.Flask(__name__, static_url_path='/static')

@app.route("/")
def home():
    '''
    Initial route to land on the home page
    '''
    return flask.render_template('home.html')

@app.route("/mydevices")
def mydevices():
    '''
    route for managing devices
    '''
    return flask.render_template('mydevices.html')


#this line runs and initialize flask
if __name__ == "__main__":
    app.run('0.0.0.0', debug=True) 


