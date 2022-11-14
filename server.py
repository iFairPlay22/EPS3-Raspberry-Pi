from imaging.thermal import ThermalCamera
from imaging.normal import NormalCamera
import os
import json
from flask import Flask
app = Flask(__name__)

def createFolderIfNotExists(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
        
def readJsonFile(path: str):
    with open(path, "r") as infile:
        return json.load(infile)
    
def saveJsonFile(path: str, object: object):
    
    json_object = json.dumps(object, indent=4)
    with open(path, "w") as outfile:
        outfile.write(json_object)
 
@app.route('/')
def home():
    return "Connected!"
 
@app.route('/take-pictures')
def take_pictures():
    
    data_to_add = {
        "thermal_array": THERMAL_CAMERA.get(),
        "normal_array": NORMAL_CAMERA.get()
    }
    
    json_data = readJsonFile(STORAGE_FULL_PATH)
    json_data["images"].append(data_to_add)
    saveJsonFile(STORAGE_FULL_PATH, json_data)
    
    return data_to_add
    return "done"
    
if __name__ == '__main__':
    
    STORAGE_FOLDER      = "storage"
    STORAGE_FILE        = "data.json"
    STORAGE_FULL_PATH   = os.path.join(STORAGE_FOLDER, STORAGE_FILE)
    
    NORMAL_CAMERA  = NormalCamera()
    THERMAL_CAMERA = ThermalCamera() 
    
    createFolderIfNotExists(STORAGE_FOLDER)
    saveJsonFile(STORAGE_FULL_PATH, { "images": [] })
    
    app.run(host="0.0.0.0")