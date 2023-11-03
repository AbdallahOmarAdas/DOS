from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect("my_database.db", check_same_thread=False)
cursor = conn.cursor()


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
        return jsonify(book_data)
    else:
        return jsonify({"error": "book not found"}, 404)


@app.route('/search/<topic>')
def querySearch(topic):
    cursor.execute("SELECT id, title FROM book WHERE topic = ?", (topic,))
    rows = cursor.fetchall()
    print(rows)
    user_list = []
    if rows == 0:
        return jsonify({"error": "there is no books belong this topic"}, 404)
    else:
        for row in rows:
            book_data = {
                "id": row[0],
                "title": row[1]
            }
            user_list.append(book_data)

    return jsonify(user_list)


if __name__ == '__main__':
    app.run(debug=True)
