from flask import make_response
from flask import Flask, request
import json
app = Flask(__name__)


@app.route('/user')
def user():
    user_name = request.args.get('name')
    resp = make_response(f"Hello, {user_name}!")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/')
def read_json():
    req = request.args.get('read')
    if req[:4] == 'true':
        with open('test_server.json') as f:
            memory = json.load(f)
        print(memory)
        resp = make_response(memory)
    else:
        resp = make_response('No resp')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/update', methods=['post'])
def write_json():
    data = json.dumps(request.form)
    print(data)
    # print(type(data.json))
    with open('test_server.json', 'w') as f:
        f.write(data)
    resp = make_response('Update success!')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.run()
