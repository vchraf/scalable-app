import redis
import hashlib
import json
import requests

from flask import Flask, jsonify,request

app = Flask('webapp')

redis_host = "localhost"
redis_port = 6379
redis_password = ""


r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)   

@app.route('/', methods=['POST'])
def predict_endpoint():
    _request = request.get_json()
    key = hashlib.sha256(f"ss{json.dumps(_request)}".encode()).hexdigest()
    print(key)
    if r.exists(key):
        val = r.get(key)
    else:
        val = requests.post(url = "http://127.0.0.1:9773", json = _request).json()['prix']
        r.set(key, val)
    result = {
        'prix': val #model.predict(list(_request.values()))
    }
    return jsonify(result)

@app.route("/v", methods =["GET", "POST"])
def visits():
    v = int(r.get("v")) + 1
    r.set("v", v)
    return str(v)    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9772)
