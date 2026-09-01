from itertools import count
import os
from flask import Flask, jsonify, render_template, request
import json
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)

app = Flask("Mohit'sApplication")

@app.route("/")
def ping():
    # return render_template("form.html")
    return "Pong!"
    
# @app.route("/todo")
# def todo():
#     return render_template("todo.html")

@app.route("/api")
def api():
    try:
        with open("JsonDataFile.txt", "r") as file:
            list = json.load(file)
    except FileNotFoundError:
        list = {}
        # I will create file if it doesnt exist
        open("JsonDataFile.txt", "w").write(json.dumps(list))
    
    return list

@app.route("/data")
def data():
    db = client["flaskdb"]
    collection = db["flask"]
    items = list(collection.find())
    for item in items:
        item["_id"] = str(item["_id"])
    return jsonify(items)
# Note  : I dont know how the jsonify works underneath but its working in this case



@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No JSON payload received"}), 400

    payload = {
        "name": data.get("name"),
        "email": data.get("email"),
        "message": data.get("message")
    }

    try:
        db = client["flaskdb"]
        db["flask"].insert_one(payload)
        return jsonify({"message": "Success!"})
    except Exception as e:
        return jsonify({"message": "An error occurred while submitting the data"})


@app.route("/submittodoitem", methods=["POST"])
def submit2():
    data = {
        "name": request.form.get("name"),
       "description": request.form.get("description"),
       "itemID": request.form.get("itemID"),
       "itemUUID": request.form.get("itemUUID"),
       "itemHash": request.form.get("itemHash"),
    }

    try:
        db = client["flaskdb"]
        db["todos"].insert_one(data)
        return "Success!"
    except Exception as e:
        
        return "An error occurred while submitting the data"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)