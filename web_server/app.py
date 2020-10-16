from flask import Flask, render_template
import requests
import json
from urllib.parse import unquote
from flask import jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show_details/<country>')
def get_data(country):

    webhook_url = 'https://1vdyaldse4.execute-api.us-east-1.amazonaws.com/dev/search'
    payload = {'country': unquote(country.strip())}

    res = requests.post(webhook_url, data=json.dumps(payload))
       
    return render_template('table.html', show_details=res.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0")
