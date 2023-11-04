from flask import Flask,Response, jsonify
import sqlite3
import requests


app = Flask(__name__)
conn = sqlite3.connect("my_database.db", check_same_thread=False)
cursor = conn.cursor()


clientIpPort = "localhost:5500"#input("Enter the IP:Port for the Front-end Server Ex:localhost:5500\n")
while 1:
    # Performs a request towards the ClientServer based on the Input
    UserInput = input("Enter the number of Operation:\n 1 --> Search by Topic \n 2--> Search by Id \n 3-->Purchase \n 4--> Exit \n")
    if UserInput == "1":
        topic = input("Enter Topic name\n")
        response = requests.get("http://"+clientIpPort + "/client/search/"+topic)
        print(response.text)

    elif UserInput == "2":
        ID = input("Enter Id of book\n")
        response = requests.get("http://"+clientIpPort + "/client/info/"+ID)
        print(response.text)

    elif UserInput == "3":
        ID = input("Enter Id of book\n")
        response = requests.put("http://"+clientIpPort + "/client/purchase/"+ID)
        print(response.text)

    elif UserInput == "4":
        break

    else:
        print("Wrong Input!, Try again")
