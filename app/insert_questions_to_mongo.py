import time
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.sj
col = db.questions

f = open('questions.txt', 'r')
item = {}
items = []
i = 0
for line in f:
	line = line.strip()
	print(line)
	if "Q:" in line:
		line = line.replace("Q: ", "")
		item['question'] = line
		item['_id'] = i
		print("Question: "+line)
	elif len(line) > 10:
		print("Explanation: "+line)
		item['explanation'] = line
		col.insert_one(item)
		i += 1

f.close()
