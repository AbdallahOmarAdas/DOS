from flask import Flask,Response, jsonify
import sqlite3
import requests


app = Flask(__name__)
conn = sqlite3.connect("my_database.db", check_same_thread=False)
cursor = conn.cursor()

clientIpPort = "localhost:6000"
catalogIpPort = "localhost:5000"
orderIpPort = "localhost:5050"


@app.route('/client/info/<itemNumber>')
def clientInfo(itemNumber):
    api_url = 'http://'+catalogIpPort+'/info/'+itemNumber
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        resource = jsonify({"error": "book not found"}, 404)
        resource.status_code = 404
        return resource
    else:
        return jsonify({'error': 'Failed to fetch data from the API'}, 500)


@app.route('/client/search/<topic>')
def clientSearch(topic):
    api_url = 'http://'+catalogIpPort+'/search/'+topic
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        resource = jsonify({"error": "there is no books belong this topic"}, 404)
        resource.status_code = 404
        return resource
    else:
        return jsonify({'error': 'Failed to fetch data from the API'}, 500)


@app.route('/client/purchase/<itemNumber>')
def clientPurchase(itemNumber):
    api_url = 'http://'+orderIpPort+'/purchase/'+itemNumber
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return jsonify({'error': 'Failed to fetch data from the API'}, 500)


if __name__ == '__main__':
    app.run('localhost', 5500, debug=True)
