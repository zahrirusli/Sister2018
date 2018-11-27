from flask import Flask, request
from zatt.client import DistributedDict
from json import dumps

app = Flask(__name__)

d = DistributedDict('127.0.0.1', 5254)

@app.route('/', methods=['GET'])
def index():
	arr = {}
	for key, val in d.items():
		if key != 'cluster':
			arr[key] = val
	return dumps(arr)

@app.route('/<ko>', methods=['GET'])
def call(ko):
	arr = {}
	for key, val in d.items():
		if key != 'cluster':
			arr[key] = val
			if key == ko:
				return dumps(val)

@app.route('/', methods=['POST'])
def create():
	data = request.get_json(force=True)
	print(data)
	key = list(data.keys())[0]
	print(key)
	val = data[key]
	d[key] = val
	#key = val
	return dumps(d[key])

@app.route('/<id>', methods=['DELETE'])
def delete(id):
	del d[id]
	return "BERHASIL"


if __name__ == '__main__':
    app.run(debug=True)
