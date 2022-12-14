from python.thermal_imaging import ThermalCamera
from python.normal_imaging import NormalCamera
from python.obstacle_avoidance import DistanceDetector
from python.drone_health import DroneHealth
from python.util import createFolderIfNotExists, readJsonFile, saveJsonFile, deleteFile
import os
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Connected!", 200

@app.route('/send-pictures')
def send_pictures():

    json_data = readJsonFile(STORAGE_FULL_PATH)

    # Reset JSON file, because the wall was analyzed
    deleteFile(STORAGE_FULL_PATH)
    saveJsonFile(STORAGE_FULL_PATH, {"images": []})

    return json_data, 200

@app.route('/take-pictures/<row>/<col>')
def take_pictures(row, col):

    data_to_add = {
        "thermal_array": THERMAL_CAMERA.get(),
        "normal_array": NORMAL_CAMERA.get(),
        "row": row,
        "col": col
    }

    # Add the data in the JSON file
    json_data = readJsonFile(STORAGE_FULL_PATH)
    json_data["images"].append(data_to_add)
    saveJsonFile(STORAGE_FULL_PATH, json_data)

    return data_to_add, 200

@app.route('/detect-obstacles')
def detect_obstacles():
    return DISTANCE_DETECTOR.get(), 200

@app.route('/battery')
def getBattery():
    return str(DRONE_HEALTH.decrement_battery()), 200

@app.route('/altitude')
def getAltitude():
    return str(DRONE_HEALTH.increment_altitude()), 200

@app.route('/launch-mission')
def launchMission():
    json_data = readJsonFile(STORAGE_FULL_PATH)

    if (len(json_data["images"]) > 0):
        return "Error old images need to be download", 500

    DRONE_HEALTH.launch()
    return '', 200

@app.route('/mission-status')
def getMissionStatus():
    return DRONE_HEALTH.getStatus(), 200

if __name__ == '__main__':

    STORAGE_FOLDER    = "storage"
    STORAGE_FILE      = "data.json"
    STORAGE_FULL_PATH = os.path.join(STORAGE_FOLDER, STORAGE_FILE)
    
    # Create JSON data
    createFolderIfNotExists(STORAGE_FOLDER)
    saveJsonFile(STORAGE_FULL_PATH, {"images": []})

    # Create TMP folder
    TMP_FOLDER = "tmp"
    createFolderIfNotExists(TMP_FOLDER)

    # Instanciating objects
    NORMAL_CAMERA     = NormalCamera(TMP_FOLDER)
    THERMAL_CAMERA    = ThermalCamera()
    DISTANCE_DETECTOR = DistanceDetector()
    DRONE_HEALTH      = DroneHealth()

    # Server accessible in the network (via the private + public IP adress)
    app.run(host="0.0.0.0")
