from flask import Flask, request, url_for, render_template, session, flash, redirect, send_from_directory, make_response, jsonify
from flask_cors import CORS
import json
import threading


class Tag:
    def __init__(self, name, value, state, desc):
        self.Name = name
        self.Value = value
        self.State = state
        self.Description = desc


class DataCenter:
    def __init__(self):
        self.tags = {}
        self.lock = threading.Lock()

    def Add(self, tag):
        self.lock.acquire()
        self.tags[tag.Name] = tag
        self.lock.release()

    def Remove(self, tagName):
        self.lock.acquire()
        self.tags.pop(tagName)
        self.lock.release()

    def Modify(self, tagName, value, state):
        if tagName in self.tags:
            self.lock.acquire()
            t = self.tags[tagName]
            t.Value = value
            t.State = state
            self.tags[tagName] = t
            self.lock.release()
            return True
        return False

    def Modify(self, tagName, value):
        if tagName in self.tags:
            self.lock.acquire()
            t = self.tags[tagName]
            t.Value = value
            self.tags[tagName]=t
            self.lock.release()
            return True
        return False

    def Read(self, tagNames):
        result = []
        self.lock.acquire()
        for key in tagNames:
            if self.tags.get(key) == None:
                result.append({'Name': key, 'Value': None,
                               'State': None, 'Description': None})
            else:
                result.append({'Name': self.tags[key].Name, 'Value': self.tags[key].Value,
                               'State': self.tags[key].State, 'Description': self.tags[key].Description})
        self.lock.release()
        return result

    def ReadAll(self):
        result = []
        self.lock.acquire()
        for key in self.tags:
            result.append({'Name': self.tags[key].Name, 'Value': self.tags[key].Value,
                       'State': self.tags[key].State, 'Description': self.tags[key].Description})
        self.lock.release()
        return result

dc=DataCenter()
dc.Add(Tag('TA1', 100, 'ok', '類比測試點1'))
dc.Add(Tag('TA2', 200, 'offline', '類比測試點2'))
dc.Add(Tag('TA3', 300, 'ok', '類比測試點3'))
dc.Add(Tag('TD1', 0, 'ok', '數位測試點1'))
dc.Add(Tag('TD2', 1, 'error', '數位測試點2'))

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/tags', methods=['GET'])
def listTags():
    result=dc.ReadAll()
    return jsonify(result)


@app.route('/writetag', methods=['GET'])
def writeTag():
    n = request.args.get('n')
    v = float(request.args.get('v'))
    print(n, v)

    if dc.Modify(n,v):
        return 'ok'
    return 'error'

@app.route('/readtags', methods=['POST'])
def readTags():
    # json data like: ["TD1","TA1","rr"]
    json_data = request.get_json()
    result = dc.Read(json_data)

    return jsonify(result)


@app.route('/writetags', methods=['POST'])
def writeTags():
    # json data like: [{"Name":"TA1","Value":80},{"Name":"TA2","Value":110}]
    json_data = request.get_json()
    for w in json_data:
        dc.Modify(w['Name'],w['Value'])

    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=1, threaded=True)
