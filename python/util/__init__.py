
import os
import json


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


def deleteFile(path: str):
    if os.path.exists(path):
        os.remove(path)
