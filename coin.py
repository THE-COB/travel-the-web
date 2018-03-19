from pymongo import MongoClient
from hashlib import sha256
import math
import random

client = MongoClient()
db = client.TravelWeb

class Coin:
	@staticmethod
	def takeOut(userId, coinId):
		db.Clients.update_one({"key": userId}, {"$pull": {"Coins": \
			{
			"CoinId": coinId
			}
		}})

	def updateDb(self):
		db.Clients.update_one({"_id": self.user["_id"]}, {"$push": {"Coins": \
			{
			"CoinId": self.coinId,
			"Clicks": []
			}}}
		)
	def __init__(self, userId):
		self.user = db.Clients.find_one({"key": userId})
		if(self.user["Approved"] == 0):
			raise Exception("Not approved")
		totalClicks = 0
		for i in self.user["Coins"]:
			totalClicks+=len(i["Clicks"])
		numCoins = len(self.user["Coins"])
		if(math.floor(numCoins/3) < totalClicks):
			raise Exception("Not enough clicks")
		coinIdStr = self.user["Email"]+self.user["Password"]+str(numCoins)+str(random.randint(0,500))
		self.coinId = sha256(coinIdStr.encode()).hexdigest()