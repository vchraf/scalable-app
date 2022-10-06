import pandas as pd
from flask import Flask, jsonify,request
app = Flask('worker')
data =  pd.read_csv("./db.csv")
def calcPrix(region_val,commune_val,type_val,surface_val):
    if type_val == "a":
        _type = "Prix_m2_appart_regression"
    elif type_val == "v":
        _type = "Prix_m2_villa_regression"
    _prix = data[_type][data.Region==region_val][data.Commune==commune_val].values.item()
    return float(surface_val) * float(_prix.replace('MAD', '').replace(' ', '')) 

@app.route("/", methods =["POST"])
def funPrix():
    region_val = request.json['region']
    commune_val = request.json["commune"]
    surface_val = request.json["surface"]
    type_val = request.json["type"]

    return jsonify(prix=calcPrix(region_val,commune_val,type_val,surface_val))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9773)