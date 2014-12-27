import os
import logging
import time
import json
import urllib
import urllib.request

SCHEDULE_FOLDER = __file__+"/schedules/"
SCHEDULE_URL = "https://events.ccc.de/congress/2014/Fahrplan/schedule.json"

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

def numFiles(directory):
    return len(next(os.walk(directory))[2])


def openSchedule(path, fileNr):
    path = os.sep.join([path, str(fileNr)])
    data = open(path).read()
    return json.loads(data)


def saveSchedule(path, fileNr, jData):
    data = json.dumps(jData)
    path = os.sep.join([path, str(fileNr)])
    f = open(path, "w")
    f.write(data)
    f.close()
    
    
def downloadSchedule(url):
    try:
        res = urllib.request.urlopen(SCHEDULE_URL)
        data = res.read().decode("utf-8")
        return json.loads(data)
    except Exception as e:
        logger.error(e)
        return None

def main():
    logger.debug("Startup...")
    files = numFiles(SCHEDULE_FOLDER)
    last_file = None
    if files > 0:
        last_file = openSchedule(SCHEDULE_FOLDER, files-1)
    while True:
        logger.debug("Next try...")
        new_file = downloadSchedule(SCHEDULE_URL)
        if new_file == None:
            logger.error("Internet kaputt")
            time.sleep(15)
            continue
        if files == 0 or new_file['schedule']['version'] != last_file['schedule']['version']:
            logger.debug("Found new one!")
            last_file = new_file
            saveSchedule(SCHEDULE_FOLDER, files, new_file)
            files += 1
        time.sleep(60)


if __name__ == '__main__':
    main()
    
    