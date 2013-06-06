from flask import Flask
from flask import request
import prepa

app = Flask(__name__)

@app.route('/getdata', methods=['Get'])
def getAllData():
    json_response = prepa.getAll()
    return json_response

@app.route('/getdata/municipios/<municipio>', methods=['Get'])
def getData(municipio):
    if municipio is None:
        return "error: municipio can't be empty"
    else:
        json_response = prepa.getByCity(municipio)
        return json_response

if __name__ == "__main__":
    app.debug=True
    app.run()
