from flask import Flask, render_template, request, jsonify, Response
import random
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import BSON
from bson import json_util
import json

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')
app.jinja_env.add_extension('jinja2.ext.loopcontrols')



connection = MongoClient("ds029638.mongolab.com", 29638) 
db = connection["api"]
db.authenticate("alokedesai","domino")
# userdb = client.db
# user_cols = userdb.cols

@app.route('/results', methods=["POST","GET"])
def results():
	major = request.form["major"]
	lessnum = (request.form["less"])
	greaternum = (request.form["greater"])

	if len(lessnum) == 0:
		lessnum = 10000
	else:
		lessnum = int(lessnum)
	if len(greaternum) == 0:
		greaternum = 0 
	else:
		greaternum = int(greaternum)
	course_list = list(db.cols.find( {"major" : major, "number" : { "$gte" : greaternum, "$lte" : lessnum } }))
	length = len(course_list)
	if length >= 13:
		length = 13
	return render_template('shuffle.html', course_list=course_list, length = length)

# @app.route('/remove', methods=['GET'])
# def remove():
# 	userdb.user_cols.remove()
# 	user_course_list = list(userdb.user_cols.find())
# 	return render_template('results.html', user_course_list=user_course_list)
@app.route('/<major>/<lownum>/<highnum>/<school>', methods=["GET"])
def all(major,lownum,highnum,school):
	try:
		lownum2 = int(lownum)
		highnum2 = int(highnum)
	except ValueError:
		lownum2 = 0
		highnum2 = 1000 
	if major == "any" and school == "any":
		course_list = list(db.cols.find( {"number" : { "$gte" : lownum2, "$lte" : highnum2}}))
	elif major == "any" :
		course_list = list(db.cols.find( {"number" : { "$gte" : lownum2, "$lte" : highnum2}, "school" : school }))	
	elif school == "any" :
		course_list = list(db.cols.find( {"major" : major, "number" : { "$gte" : lownum2, "$lte" : highnum2 } }))	
	else:
		course_list = list(db.cols.find( {"major" : major, "number" : { "$gte" : lownum2, "$lte" : highnum2 }, "school" : school }))	
	length = len(course_list)
	size = length
	if length >= 13:
		length = 13

	random.shuffle(course_list)

	return render_template("shuffle.html", course_list = course_list, length =length, size=size)
@app.route("/getmore")
def getmore():
	course_list = db.cols.find()
	course_list = course_list[:1]
	random.shuffle(course_list)
	print (course_list)
	print dict(course_list)
	return "x"
	

@app.route("/test")
def test():
	return render_template("text.html")
#test for learning ajax
@app.route('/_add_numbers')
def add_numbers():

    course_list = list(db.cols.find())
    
    random.shuffle(course_list)
    course_list = course_list[:12]

    resp = Response(json.dumps({'res': course_list}, default=json_util.default),
                mimetype='application/json')
    return resp

	
	 
@app.route('/class/setfavorite/<course_id>', methods=['POST','GET'])
def setFavorite(course_id):
	#course = list(client.db.cols.find_one({"_id['ObjectId']": class_id}))
	#return str(course_id)
	if course_id is not None:
		db.cols.update({"_id": ObjectId(course_id)},
		{
			'$set': { 'favorite': True }
		}
		)
	return str((db.cols.find_one({"_id": ObjectId(course_id)})))
	# str(client.db.collection_names())
	
@app.route('/class/unsetfavorite/<course_id>', methods=['POST','GET'])
def unsetFavorite(course_id):
	#course = list(client.db.cols.find_one({"_id['ObjectId']": class_id}))
	#return str(course_id)
	if course_id is not None:

		db.cols.update({"_id": ObjectId(course_id)},
		{
			'$set': { 'favorite': False }
		}
		)
	return str((db.cols.find_one({"_id": ObjectId(course_id)})))
	# str(client.db.collection_names())

@app.route('/hong')
def hong():
	course_list = list(db.cols.find())
	random.shuffle(course_list)
	return render_template('index.html', course_list=course_list)

@app.route('/')
def index():
	course_list = list(db.cols.find())
	random.shuffle(course_list)
	return render_template('index.html', course_list=course_list)

if __name__ == '__main__':
    app.run(debug=True)