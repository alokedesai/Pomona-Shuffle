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
	return render_template('index.html', course_list=course_list, length = length)



@app.route("/getmore")
def getmore():
	course_list = db.cols.find()
	course_list = course_list[:1]
	random.shuffle(course_list)
	print (course_list)
	print dict(course_list)
	return "x"

#test for learning ajax
@app.route('/_add_numbers')
def add_numbers():

    course_list = list(db.cols.find())
    
    random.shuffle(course_list)
    course_list = course_list[:12]

    resp = Response(json.dumps({'res': course_list}, default=json_util.default),
                mimetype='application/json')
    return resp


@app.route("/")
def index():
	return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)