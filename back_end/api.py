import json
from pymongo import MongoClient
from flask import Flask
from flask import request
from flask import Flask, make_response, Response
from flask_cors import CORS, cross_origin

app = Flask(__name__)

# Pass cross-origin thingy
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

mongo = MongoClient("localhost", 27017)
db = mongo.sj
col_q = db.questions
col_a = db.answers

def create_txt(request):
    qs = col_q.find({})
    questions = []
    for item in qs:
        questions.append(item['question'])
    answers = [item[1] for item in request.form.items() if 'q' in item[0]]
    data = zip(questions, answers)
    text = ""
    for i, item in enumerate(data):
        question = item[0]
        answer = item[1]
        text += "Q{} -- ".format(i+1) + question + "\n\n"
        text += answer + "\n\n"
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    return "Hi bro!"

@app.route('/judge', methods=['GET', 'POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def judge():
    if request.method == 'POST':
    	print(" > New form insert ... ")
    	print(request.form)
        # save to mongodb
    	col_a.insert_one(dict(request.form))
        # export txt
        text = create_txt(request)
        print(text)
        response = make_response(text)
        response = Response(text,
                       mimetype="text/plain",
                       headers={"Content-Disposition":
                                    "attachment;filename=test.txt"})

        response.headers["Content-Disposition"] = 'attachment;filename="idea_judge.txt"'
    return response

@app.route('/rq', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])  # cross-origin again!!
def retrieve_questions():
    qs = col_q.find({})
    qs = qs[0:2]
    return json.dumps(list(qs))


if __name__ == "__main__":
    app.run(debug=False,
	        host="0.0.0.0",
	        port=5555)
