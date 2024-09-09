'''
See minimal flask application https://flask.palletsprojects.com/en/3.0.x/quickstart/#a-minimal-application
'''

from flask import Flask, render_template

app = Flask(__name__)

#initial route (home page)
@app.route("/")
def home():
    return render_template('home.html')



#this line runs and initialize flask
if __name__ == "__main__":
    app.run('0.0.0.0', debug=True) 


