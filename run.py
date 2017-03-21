#!/usr/bin/env python
from __future__ import print_function
import os.path
import sys
import uuid
import yaml
import importlib
import inspect
import click
from flask import Flask, Response, jsonify, request, abort
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


@app.route('/notebook')
def notebook():
    notebookname = 'PythonAssignment.ipynb'
    notebookpath = os.path.join('/data', notebookname)
    if os.path.isfile(notebookpath):
        nb_content = open(notebookpath).read()
    elif os.path.isfile(notebookname):
        # look in current directory
        nb_content = open(notebookname).read()
    return Response(nb_content, 'application/x-ipynb+json')


@app.route('/yaml')
def yamlfile():
    yamlfile.seek(0)
    yaml_content = yamlfile.read()
    return Response(yaml_content, 'text/vnd.yaml')


@app.route('/testlist', methods=['GET'])
def testlist():
    print(tests)
    return jsonify(list(tests.keys()))

@app.route('/getkey', methods=['POST'])
def register_or_login():
    content = request.get_json()
    if 'email' not in content:
        abort(404)
    else:
        email = content['email']
    user = mongo.db.students.find_one({'email': email})
    if user is None:
        key = uuid.uuid4()
        user = dict(email=email, key=key)
        mongo.db.students.insert_one(user)
    else:
        key = user['key']
    return(jsonify(dict(email=email, key=key)))


def empty_answer(testtype):
    if testtype == 'list':
        return []
    elif testtype == 'str':
        return ''
    elif testtype == 'int':
        return 0
    else:
        return None


@app.route('/submit_notebook', methods=['POST'])
def accept_notebook():
    content = request.get_json()
    if 'notebook' in content and 'key' in content:
        notebook = content['notebook']
        key = content['key']
        assignment = dict(notebook=notebook, key=key)
        mongo.db.assignments.insert_one(assignment)
        print(mongo.db.name)
        return jsonify(dict(success=True))
    else:
        abort(404)


@app.route('/getmark/<key>', methods=['GET'])
def getmark(key):
    marks = mongo.db.answers.find(dict(key=key))
    total = 0
    tests_correct = []
    for mark in marks:
        correct = mark.get('correct', False)
        if correct:
            tests_correct.append(mark.get('testname', 'unknown'))
            total += mark.get('marks', 0)
    return jsonify(dict(total=total, tests_correct=tests_correct))


@app.route('/test_<testname>', methods=['POST'])
def testrunner(testname):
    print('testing:', testname)
    if testname not in tests:
        reason = 'Unknown test'
        response = dict(correct_answer=None, correct=False, reason=reason)
        return jsonify(response)
    content = request.get_json()
    if 'key' not in content:
        reason = 'No login key'
        response = dict(correct_answer=None, correct=False, reason=reason)
        return jsonify(response)
    else:
        key = content['key']
    parameters = content.get('parameters', [])
    print(parameters)
    test = tests[testname]
    testtype = test['answer_type']
    answer = content.get('answer', empty_answer(testtype))
    correct_answer = test['function'](*parameters)
    print(correct_answer)
    if type(answer) != type(correct_answer):
        correct = False
    elif (testtype == 'list' or testtype == 'str') and len(answer) != len(correct_answer):
        correct = False
    elif answer != correct_answer:
        correct = False
    else:
        correct = True
    print("marks type:", type(test['marks']))
    current_score = mongo.db.answers.find_one(dict(key=key, testname=testname))
    if current_score is None:
        score = dict(key=key, testname=testname, correct=correct, marks=test['marks'])
    else:
        score = current_score
        score['correct'] = correct
    mongo.db.answers.save(score)
    response = dict(correct_answer=correct_answer, correct=correct, reason='')
    return jsonify(response)

if __name__ == '__main__':
    print("run the app:", 1489650645)
    init_tests()
    # app.run(host='0.0.0.0')
