from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    print ("Hello. This should be local")
    return 'Hello, World!'