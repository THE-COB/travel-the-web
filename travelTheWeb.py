from flask import Flask
from flask import request
from pymongo import MongoClient
from datetime import datetime
from hashlib import sha256
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from coin import Coin
import random
import smtplib
import requests
app = Flask(__name__)

client = MongoClient()
db = client.TravelWeb

def putNewAccount(params):
	name = params["name"]
	email = params["email"]
	password = params["password"]
	counterTop = params["counterTop"]
	if(name.find('/') != -1 or name.find('\\') != -1):
		raise Exception("Illegal character used")
	if(db.Clients.find({"Email": email}).count() != 0):
		raise Exception("Email already exists")
	if(db.Clients.find({"Name": name}).count() != 0):
		raise Exception("Usename already exists")
	key = sha256((name+password+email+counterTop+str(random.randint(0,500))).encode()).hexdigest()
	result = db.Clients.insert_one(
		{
			"Name": name,
			"Email": email,
			"Password": sha256(password.encode()).hexdigest(),
			"key": key,
			"DateUpdated": datetime.now().strftime("%Y-%m-%d %H:%M"),
			"Coins": [],
			"Coins-Clicked": [],
			"Counter-Top": counterTop,
			"Approved": 0
		}
	)
	fromaddr = "noreply.traveltheweb@gmail.com"
	toaddr = email
	confirmLink = "http://localhost:5000/confirm-account/"+key+"j3uy8ed09m4"
	msg = MIMEText("<p>Hello, "+name+"!<br><a href='"+confirmLink+"'>Click here</a> to confirm your Travel the Web account!",'html')
	msg["From"] = fromaddr
	msg["to"] = toaddr
	msg["Subject"] = "Link to confirm your new Travel the Web Account"


	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login("noreply.traveltheweb@gmail.com", "Mytraveltheweb321$")
	text = msg.as_string()
	server.sendmail(fromaddr, email, text)
	server.quit()

@app.route("/")
def index():
	f = open("login.html")
	return f.read()

@app.route("/login")
def login():
	f = open("login.html")
	return f.read()

@app.route("/home", methods=["POST"])
def homePage():
	if(request.form["username"] != ""):
		user = db.Clients.find_one({"Name":request.form["username"]})
	elif(request.form["email"] != ""):
		user = db.Clients.find_one({"Email": request.form["email"]})
	else:
		return "Make sure you fill out either username or email"

	if(user == None):
		return "Make sure you typed in the correct username or email, because you don't seem to exist"
	password = request.form["password"]
	if(sha256(password.encode()).hexdigest() != user["Password"]):
		return "Your password is incorrect"
	createHtml = "<input type='button' onclick='location.href=\"/"+user["Name"]+"/kurghy6592"+user["key"]+"hfu334j59g3o0/create-coin\";' value='Create Coin' />"
	return createHtml

@app.route("/create-account")
def createAccount():
	f = open("make-account.html")
	return f.read()

@app.route("/makeAccount", methods=["POST"])
def makeAccount():
	formData = {"name":request.form["name"], "email":request.form["email"], "password":request.form["password"], "counterTop":request.form["counter-top"]}
	try:
		putNewAccount(formData)
	except Exception as exc:
		return str(exc)
	return "Account created, confirm your account by clicking the link we sent to your email<br>If you don't click the link in 5 days, your account will be deleted"

@app.route("/confirm-account/j4s0kl1lk8q<key>j3uy8ed09m4")
def confirmAccount(key):
	result = db.Clients.update_one({"key": key}, {"$set": {"Approved": 1}})
	return "Your account has been approved"

@app.route("/<username>/kurghy6592<key>hfu334j59g3o0/create-coin")
def createCoin(username, key):
	user = db.Clients.find_one({"Name": username})
	if(user["key"] != key):
		return "Something is wrong with the url"
	newCoin = Coin(user["key"])
	newCoin.updateDb()
	return "Coin was successfully created"
