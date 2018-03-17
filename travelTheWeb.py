from flask import Flask
from flask import request
from pymongo import MongoClient
from datetime import datetime
from hashlib import sha256
import random
import smtplib
import requests
app = Flask(__name__)

client = MongoClient()
db = client.TravelWeb

def putNewAccount(name, email, password):
	print(db.Clients.find({"Email": email}))
	if(db.Clients.find({"Email": email}).count() != 0):
		raise Exception("Email already exists")
	if(db.Clients.find({"Name": name}).count() != 0):
		raise Exception("Usename already exists")
	key = sha256((name+password+email+str(random.randint(0,500))).encode()).hexdigest()
	result = db.Clients.insert_one(
		{
			"Name": name,
			"Email": email,
			"Password": password,
			"key": key,
			"DateUpdated": datetime.now().strftime("%Y-%m-%d %H:%M"),
			"Coins": [],
			"Approved": "0"
		}
	)
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login("noreply.traveltheweb@gmail.com", "Mytraveltheweb321$")

	message = str("Click this link to confirm you account localhost:5000/confirm-account/"+key)
	server.sendmail("noreply.traveltheweb@gmail.com", email, message)
	server.quit()

@app.route("/")
def index():
	f = open("make-account.html")
	return f.read()

@app.route("/makeAccount", methods=["POST"])
def makeAccount():
	formData = [request.form["name"], request.form["email"], request.form["password"]]
	try:
		putNewAccount(formData[0],formData[1],formData[2])
	except Exception as exc:
		return str(exc)
	return "Account created, confirm your account by clicking the link we sent to your email<br>If you click the link in 5 days, your account will be deleted"

@app.route("/confirm-account/<key>")
def confirmAccount(key):
	result = db.Clients.update_one({"key": key}, {"$inc": {"Approved": "1"}})