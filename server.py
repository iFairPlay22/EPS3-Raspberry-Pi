from python.thermal_imaging import ThermalCamera
from python.normal_imaging import NormalCamera
from python.util import createFolderIfNotExists, readJsonFile, saveJsonFile
import os
from flask import Flask
app = Flask(__name__)

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
    createFolderIfNotExists(STORAGE_FOLDER)
    saveJsonFile(STORAGE_FULL_PATH, { "images": [] })
    
    TMP_FOLDER = "tmp"
    createFolderIfNotExists(TMP_FOLDER)
    
    NORMAL_CAMERA  = NormalCamera(TMP_FOLDER)
    THERMAL_CAMERA = ThermalCamera() 
    
    app.run(host="0.0.0.0")