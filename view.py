#!/usr/bin/env python
from __future__ import print_function
import os.path
import sys
import uuid
import yaml
import importlib
import inspect
import click
from flask import Flask, Response, jsonify, request, abort, render_template
from flask_pymongo import PyMongo

sys.path.append('/data')

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'testserver'
mongo = PyMongo(app)

tests = None
yamlfile = None


def find_function(module, name):
    for (function_name, function_object) in inspect.getmembers(module, inspect.isfunction):
        if function_name == name:
            return function_object


@click.command()
@click.argument('testsfile', type=click.File('r'))
def init_tests(testsfile):
    global tests
    global yamlfile
    yamlfile = testsfile
    data = yaml.load(testsfile)
    tests = data['tests']
    print(data)
    tests_module = importlib.import_module(data['modulename'])
    for testname in tests:
        func = find_function(tests_module, testname)
        if func == None:
            exit('Could not find implementation for {}'.format(testname))
        tests[testname]['function'] = func
    app.run(host='0.0.0.0', debug=data.get('debug', False))

# @app.route('/static/scripts/js/<path>')
# def send_js(path):
#     print("here:", path)
#     return send_from_directory('static/scripts/js', path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students', methods=['GET'])
def students():
    students = mongo.db.students.find()
    emails = [ dict(email=student['email'], key=str(student['key'])) for student in students ]
    print(emails)
    return jsonify(emails)

@app.route('/getmark/<key>', methods=['GET'])
def getmark(key):
    print("called with:", key)
    marks = mongo.db.answers.find(dict(key=key))
    total = 0
    tests_correct = []
    for mark in marks:
        correct = mark.get('correct', False)
        if correct:
            tests_correct.append(mark.get('testname', 'unknown'))
            total += mark.get('marks', 0)
    return jsonify(dict(total=total, tests_correct=tests_correct))


@app.route('/student_notebook/<key>')
def getnotebook(key):
    notebook = mongo.db.assignments.find_one(dict(key=key))
    if notebook is not None:
        return Response(response=notebook.get('notebook', ''),
        status=200,
        mimetype='application/x-ipynb+json')
    else:
        abort(404);


if __name__ == '__main__':
    print("run the app:", 1489650645)
    init_tests()
