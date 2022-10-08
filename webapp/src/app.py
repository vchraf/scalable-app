import redis
import hashlib
import json
import requests
import psycopg2
from flask import Flask, jsonify,request

app = Flask('webapp')

redis_host = "localhost"
redis_port = 6379
redis_password = ""

conn = psycopg2.connect(host="localhost", database="regdb", user="admin", password="admin")
conn.autocommit = True
cursor = conn.cursor()

r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)   

@app.route('/', methods=['POST'])
def predict_endpoint():
    _request = request.get_json()
    key = hashlib.sha256(f"ss{json.dumps(_request)}".encode()).hexdigest()
    if r.exists(key):
        val = r.get(key)
    else:
        _request['hash'] = key
        val = requests.post(url = "http://127.0.0.1:9773", json = _request).json()['prix']
        r.set(key, val)
    result = {
        'prix': val #model.predict(list(_request.values()))
    }
    cursor.execute(f'''INSERT INTO requests(hash, region, commune, type, surface, prix) VALUES ('{key}','{_request['region']}','{_request['commune']}','{_request['type']}',{_request['surface']},{val})''')
    conn.commit()
    return jsonify(result)

@app.route("/v", methods =["GET", "POST"])
def visits():
    v = int(r.get("v")) + 1
    r.set("v", v)
    return str(v)    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9772)


# docker run --name postgresql -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -p 5432:5432 -v /data:/var/lib/postgresql/data -d postgres