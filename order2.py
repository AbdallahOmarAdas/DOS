from flask import Flask, Response, jsonify
import sqlite3
import requests

app = Flask(__name__)
conn = sqlite3.connect("my_database.db", check_same_thread=False)
cursor = conn.cursor()

catalog = 'http://172.17.0.4:5000'
catalog2 = 'http://172.17.0.6:5000'

lastCatalogServerUsed = 1


@app.route('/purchase/<itemNumber>', methods=['PUT'])
def queryPurchase(itemNumber):
    global lastCatalogServerUsed
    base_api_url = ''
    if lastCatalogServerUsed == 1:
        lastCatalogServerUsed = 2
        base_api_url = catalog
    else:
        lastCatalogServerUsed = 1
        base_api_url = catalog2
    api_url = base_api_url+'/info/'+itemNumber
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data['quantity'] >= 1:
            api_url = base_api_url+'/update/' + itemNumber
            response = requests.put(api_url)
            print(response.text)
            return response.json()
        else:
            print("{'error': 'can not purchase this book because it out of stock.'}")
            return jsonify(
                {'error': 'can not purchase this book because it out of stock.'})
    elif response.status_code == 404:
        resource = jsonify({"error": "book not found"}, 404)
        resource.status_code = 404
        print(response.text)
        return resource
    else:
        print("({'error': 'Failed to fetch data from the API'}, 500)")
        return jsonify({'error': 'Failed to fetch data from the API'}, 500)


if __name__ == '__main__':
    app.run('0.0.0.0', 5050, debug=True)
