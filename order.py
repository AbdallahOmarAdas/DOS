from flask import Flask, Response, jsonify
import sqlite3
import requests

app = Flask(__name__)
conn = sqlite3.connect("my_database.db", check_same_thread=False)
cursor = conn.cursor()


@app.route('/purchase/<itemNumber>')
def queryPurchase(itemNumber):
    api_url = 'http://localhost:5000/info/'+itemNumber
    response = requests.get(api_url)
    if response.status_code == 200:
        print("hhhhhhhhhhhhhhh")
        data = response.json()
        if data['quantity'] >= 1:
            cursor.execute("UPDATE book set quantity=quantity-1 WHERE id = ? ", (itemNumber,))
            conn.commit()
            return jsonify(
                {'msg': 'The book was purchased successfully'})
        else:
            return jsonify(
                {'error': 'can not purchase this book because it out of stock.'})
    elif response.status_code == 404:
        resource = jsonify({"error": "book not found"}, 404)
        resource.status_code = 404
        return resource
    else:
        return jsonify({'error': 'Failed to fetch data from the API'}, 500)


if __name__ == '__main__':
    app.run('localhost', 5050, debug=True)
