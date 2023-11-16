from flask import Flask, Response, jsonify
import requests


app = Flask(__name__)

catalogIpPort = "172.17.0.4:5000"
orderIpPort = "172.17.0.3:5050"


@app.route('/client/info/<itemNumber>')
def clientInfo(itemNumber):
    api_url = 'http://'+catalogIpPort+'/info/'+itemNumber
    response = requests.get(api_url)
    if response.status_code == 200:
        with open("logFile.txt", "a") as file:
            file.write(api_url+"\n")
            file.write(response.text+"\n")
        return response.json()
    elif response.status_code == 404:
        resource = jsonify({"error": "book not found"}, 404)
        resource.status_code = 404
        with open("logFile.txt", "a") as file:
            file.write(api_url+"\n")
            file.write(response.text+"\n")
        return resource
    else:
        with open("logFile.txt", "a") as file:
            file.write("({'error': 'Failed to fetch data from the API'}, 500)\n")
        return jsonify({'error': 'Failed to fetch data from the API'}, 500)


@app.route('/client/search/<topic>')
def clientSearch(topic):
    api_url = 'http://'+catalogIpPort+'/search/'+topic
    response = requests.get(api_url)
    if response.status_code == 200:
        with open("logFile.txt", "a") as file:
            file.write(api_url+"\n")
            file.write(response.text+"\n")
        return response.json()
    elif response.status_code == 404:
        resource = jsonify({"error": "there is no books belong this topic"}, 404)
        resource.status_code = 404
        with open("logFile.txt", "a") as file:
            file.write(api_url+"\n")
            file.write(response.text+"\n")
        return resource
    else:
        with open("logFile.txt", "a") as file:
            file.write("({'error': 'Failed to fetch data from the API'}, 500)\n")
        return jsonify({'error': 'Failed to fetch data from the API'}, 500)


@app.route('/client/purchase/<itemNumber>', methods=['PUT'])
def clientPurchase(itemNumber):
    api_url = 'http://'+orderIpPort+'/purchase/'+itemNumber
    response = requests.put(api_url)
    if response.status_code == 200:
        with open("logFile.txt", "a") as file:
            file.write(api_url+"\n")
            file.write(response.text+"\n")
        return response.json()
    elif response.status_code == 404:
        resource = jsonify({"error": "book not found"}, 404)
        resource.status_code = 404
        print(response.text)
        return resource
    else:
        with open("logFile.txt", "a") as file:
            file.write("({'error': 'Failed to fetch data from the API'}, 500)\n")
        return jsonify({'error': 'Failed to fetch data from the API'}, 500)


if __name__ == '__main__':
    app.run('0.0.0.0', 5500, debug=True)
