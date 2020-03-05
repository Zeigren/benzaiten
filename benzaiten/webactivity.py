#!/opt/venv/bin python
import glob
import json
import os
import time


def activitySave(activity):
    filename = f"./data/{time.time()}.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as outfile:
        try:
            json.dump(activity, outfile)
        except OSError:
            print("Error while writing : ", filename)


def activityClean():
    # Deletes all files except the 6 newest ones
    files = glob.glob("./data/*")
    files.sort(key=os.path.getmtime, reverse=True)
    del files[:6]
    for file in files:
        try:
            os.remove(file)
        except OSError:
            print("Error while deleting file : ", file)
