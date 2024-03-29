from flask import Flask,Response, jsonify
import sqlite3
import requests

app = Flask(__name__)
conn = sqlite3.connect("my_database.db", check_same_thread=False)
cursor = conn.cursor()

second_catalog_server = 'http://172.17.0.5:5000'

@app.route('/info/<itemNumber>')
def queryInfo(itemNumber):
    cursor.execute("SELECT title, quantity, price FROM book WHERE id = ?", (itemNumber,))
    row = cursor.fetchone()
    print(row)
    if row:
        book_data = {
            "title": row[0],
            "quantity": row[1],
            "price": row[2]
        }
        print(book_data)
        return jsonify(book_data)
    else:
        msg = jsonify({"error": "book not found"}, 404)
        msg.status_code = 404
        print(msg)
        return msg


@app.route('/search/<topic>')
def querySearch(topic):
    cursor.execute("SELECT id, title FROM book WHERE topic = ?", (topic,))
    rows = cursor.fetchall()
    print(rows)
    user_list = []
    if len(rows) == 0:
        msg = jsonify({"error": "there is no books belong this topic"}, 404)
        msg.status_code = 404
        print(msg)
        return msg
    else:
        for row in rows:
            book_data = {
                "id": row[0],
                "title": row[1]
            }
            user_list.append(book_data)
        print(user_list)
        return jsonify(user_list)


@app.route('/update/<itemNumber>', methods=['PUT'])
def queryUpdate(itemNumber):
    cursor.execute("SELECT title, quantity, price FROM book WHERE id = ?", (itemNumber,))
    row = cursor.fetchone()
    if row[1] >= 1:
        api_url = second_catalog_server + '/dbUpdate/Subtract/' + itemNumber
        print('send queryUpdate(purchase) to the second server')
        response = requests.put(api_url)
        print("second server response: " + response.text)
        cursor.execute("UPDATE book set quantity=quantity-1 WHERE id = ? ", (itemNumber,))
        conn.commit()
        print("{'msg': 'The book was purchased successfully'}")
        return jsonify(
            {'msg': 'The book was purchased successfully'})
    else:
        print("{'error': 'can not purchase this book because it out of stock.'}")
        return jsonify(
            {'error': 'can not purchase this book because it out of stock.'})


@app.route('/dbUpdate/<operation>/<itemNumber>', methods=['PUT'])
def dbUpdate(operation, itemNumber):   # this endpoint for database consistency
    if operation == "Add":
        cursor.execute("UPDATE book set quantity=quantity+1 WHERE id = ? ", (itemNumber,))
    else:
        cursor.execute("UPDATE book set quantity=quantity-1 WHERE id = ? ", (itemNumber,))
    conn.commit()
    return jsonify(
            {'msg': 'done  updated second Database successfully'})


@app.route('/AddOneToStock/<itemNumber>', methods=['PUT'])
def queryAddOneToStock(itemNumber):
    api_url = second_catalog_server + '/dbUpdate/Add/' + itemNumber
    response = requests.put(api_url)
    print('send queryAddOneToStock to the second server')
    print("second server response: " + response.text)
    cursor.execute("UPDATE book set quantity=quantity+1 WHERE id = ? ", (itemNumber,))
    conn.commit()
    print("{'msg': 'A book has been added successfully'}")
    return jsonify(
        {'msg': 'A book has been added successfully'})


if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
