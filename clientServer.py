from flask import Flask, Response, jsonify
import requests

class Book:
    def __init__(self, title, price, quantity, id):
        self.title = title
        self.price = price
        self.quantity = quantity
        self.id = id


app = Flask(__name__)

catalogIpPort = "172.17.0.4:5000"
orderIpPort = "172.17.0.3:5050"

bookCache = []
Book("How to get a good grade in DOS in 40 minutes a day", 30, 10, 1)
@app.route('/client/info/<itemNumber>')
def clientInfo(itemNumber):
    for book in bookCache:
        if book.id == int(itemNumber):
            print("from cache")
            return jsonify(title=book.title, price=book.price, quantity=book.quantity, id=book.id)

    api_url = 'http://'+catalogIpPort+'/info/'+itemNumber
    response = requests.get(api_url)
    if response.status_code == 200:
        with open("logFile.txt", "a") as file:
            file.write(api_url+"\n")
            file.write(response.text+"\n")
        book_data = response.json()
        book = Book(title=book_data['title'], price=book_data['price'], quantity=book_data['quantity'],
                    id=int(itemNumber))
        print("add to cache")
        bookCache.append(book)
        return jsonify(title=book.title, price=book.price, quantity=book.quantity, id=book.id)
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
    for book in bookCache:
        if book.id == int(itemNumber):
            print("remove from cache")
            bookCache.remove(book)
            # remove the book from cache to update the data in cache in the next Search by Id we will add this book to cache with the updated data
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
