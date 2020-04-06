from flask import Flask, request, url_for, render_template, session, flash, redirect, send_from_directory, make_response, jsonify
from flask_cors import CORS
import json
import threading

class Tag:
    def __init__(self, name,value,state,desc):  
        self.Name = name
        self.Value = value  
        self.State = state
        self.Description = desc

lock = threading.Lock()

tags = {}
tags['TA1'] = Tag('TA1', 100, 'ok', '類比測試點1')
tags['TA2'] = Tag('TA2', 200, 'offline', '類比測試點2')
tags['TA3'] = Tag('TA3', 300, 'ok', '類比測試點3')
tags['TD1'] = Tag('TD1', 0, 'ok', '數位測試點1')
tags['TD2'] = Tag('TD2', 1, 'error', '數位測試點2')

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/tags', methods=['GET'])
def listTags():
    result = []
    lock.acquire()
    for key in tags:
        result.append({'Name': tags[key].Name, 'Value': tags[key].Value,
                       'State': tags[key].State, 'Description': tags[key].Description})
    lock.release()
    return jsonify(result)


@app.route('/writetag', methods=['GET'])
def writeTag():
    n = request.args.get('n')
    v = float(request.args.get('v'))
    print(n, v)

    lock.acquire()
    if tags.get(n)!=None:
        tags[n].Value=v
        lock.release()
        return 'ok'

    lock.release()
    return 'error'


@app.route('/readtags', methods=['POST'])
def readTags():
    # json data like: ["TD1","TA1","rr"]
    json_data = request.get_json()

    lock.acquire()
    result = []
    for key in json_data:
        if tags.get(key) == None:
            result.append({'Name': key, 'Value': None,
                       'State': None, 'Description': None})
        else:
            result.append({'Name': tags[key].Name, 'Value': tags[key].Value,
                       'State': tags[key].State, 'Description': tags[key].Description})
    lock.release()
    return jsonify(result)


@app.route('/writetags', methods=['POST'])
def writeTags():
     # json data like: [{"Name":"TA1","Value":80},{"Name":"TA2","Value":110}]
    json_data = request.get_json()
    lock.acquire()
    result = []
    for w in json_data:
        if tags.get(w['Name'])!=None:
            tags[w['Name']].Value=w['Value']

    lock.release()
    return jsonify(json_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=1, threaded=True)
