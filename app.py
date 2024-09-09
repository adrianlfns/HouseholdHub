'''
See minimal flask application https://flask.palletsprojects.com/en/3.0.x/quickstart/#a-minimal-application
'''

from flask import Flask 

app = Flask(__name__)



@app.route("/")
def hello_word():
    return "hello2"



#this line runs and initialize flask
if __name__ == "__main__":
    app.run('0.0.0.0', debug=True) 


