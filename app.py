from flask import render_template, Flask, send_from_directory, request
from os import path
from glob import glob
import random
import json


app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')


def all_kapitel():
    return sorted([f.split("/")[-1] for f in glob("./static/questionfiles/*.json")])

def questions(file):
    data_sheet = json.load(open(f"./static/questionfiles/{file}"))
    return data_sheet["questions"]

def get_title(file):
    data_sheet = json.load(open(f"./static/questionfiles/{file}"))
    return data_sheet["title"]

def get_random(size:int):
    all_questions =  [question for kapitel in all_kapitel() for question in questions(kapitel)]
    return random.sample(all_questions, k=size)


@app.route('/' , methods=['GET'])
def main_route():
    return render_template('main.html',items=all_kapitel())


@app.route('/q' , methods=['GET'])
def kapitel_route():
    kap = request.args.get("kapitel")
    return render_template('questions.html',items=list(enumerate(questions(kap))), title=get_title(kap))


@app.route('/r' , methods=['GET'])
def random_questions_route():
    size = int(request.args.get("size")) if request.args.get("size").isnumeric() else 15
    return render_template('questions.html', items=list(enumerate(get_random(size))), title="random_questions")



@app.route('/style.css')
def style():
    return send_from_directory(path.join(app.root_path, 'static'),
                               'css/style.css', mimetype='text/css')

app.run(debug= True, port= 3000, host="0.0.0.0")
