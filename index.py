from flask import Flask, render_template
app = Flask(__name__)

from flask_bootstrap import Bootstrap
boorstrap = Bootstrap(app)

import json

def get_last_date():
    f = open('time.dat', 'r')
    time = f.read()
    f.close()
    return time

def get_account_data():
    f = open('info.dat', 'r')
    data = json.load(f)
    f.close()
    return data

@app.route('/')
def index():
    return render_template('index.html', last_date = get_last_date(), account_data = get_account_data())
    
if '__main__' == __name__:
    app.run(debug = True)
