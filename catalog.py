from flask import Flask,jsonify
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect("my_database.db",check_same_thread=False)
cursor = conn.cursor()
@app.route('/info/<itemNumber>')
def getInfo(itemNumber):
    cursor.execute("SELECT title, quantity, price FROM book WHERE id = ?",(itemNumber,))
    row = cursor.fetchone()
    print(row)
    if row:
        user_data = {
            "title": row[0],
            "quantity": row[1],
            "price": row[2]
        }
        return jsonify(user_data)
    else:
        return jsonify({"error": "User not found"}, 404)


if __name__ == '__main__':

    app.run(debug=True)