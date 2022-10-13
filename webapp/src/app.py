import os

import redis
import hashlib
import json
import requests
import psycopg2
from flask import Flask, jsonify,request

app = Flask('webapp')

redis_host = os.getenv('REDIS_HOST')#"localhost"
redis_port = os.getenv('REDIS_PORT')
redis_password = ""

postgres_host = os.getenv('PG_HOST')
postgres_db = os.getenv('PG_DB')
postgres_user = os.getenv('PG_USER')
postgres_password = os.getenv('PG_PASSWORD')

worker_adress = os.getenv('WORKER_ADRESS')

conn = psycopg2.connect(host=postgres_host, database=postgres_db, user=postgres_user, password=postgres_password)
conn.autocommit = True
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS requests(ID  SERIAL PRIMARY KEY, hash TEXT NOT NULL, region TEXT NOT NULL, \
    commune TEXT NOT NULL, type TEXT NOT NULL, surface REAL NOT NULL, prix REAL NOT NULL, date timestamp NOT NULL DEFAULT NOW())')
conn.commit()

r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)   

@app.route('/', methods=['POST'])
def predict_endpoint():
    _request = request.get_json()
    key = hashlib.sha256(f"ss{json.dumps(_request)}".encode()).hexdigest()
    if r.exists(key):
        val = r.get(key)
    else:
        _request['hash'] = key
        val = requests.post(url = worker_adress, json = _request).json()['prix']
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