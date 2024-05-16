import os
import subprocess
from datetime import datetime
import time
import signal
from time import gmtime
from subprocess import DEVNULL

directory = os.path.abspath("C:/NetworkUpTimeDetector")
directoryFile = os.path.abspath("C:/NetworkUpTimeDetector/log.txt")


# Make folder if possible
if not os.path.exists(directory):
    # Create the directory
    os.makedirs(directory)
    print("Directory created successfully!")
else:
    print("Found directory! : " + directory)

# Make file if possible
if not os.path.isfile(directoryFile):
    #Create the txt file
    f=open(directoryFile,"w+")
    f.write("Network Uptime Detector\n")
    f.write("Author: Sam Quackels\n")
    f.write("Made on: 16/05/2024\n")
    f.write("|       Date       |       Time started       |       Time ended       |       Duration       |\n")
    f.close()
    print("Log file created successfully! : " + directoryFile)
else:
    print("Found log file!")
    

# Starting detection
address = "8.8.8.8"
ttl = "20"
command = "ping " + address + " -i " + ttl + " -n 1"
while True:
    p = subprocess.Popen(command, stdout=DEVNULL)
    p.wait()
    code = (p.returncode)
    # Could not ping
    if code == 1:

        date = datetime.now().strftime("%d/%m/%Y")
        startTime = datetime.now().strftime("%H:%M:%S")
        startTimeObject = datetime.now()
        
        print("Lost connection at : " + startTime)
        while code == 1 :
            p = subprocess.Popen(command, stdout=DEVNULL)
            p.wait()
            code = (p.returncode)
            time.sleep(2)
        stopTime = datetime.now().strftime("%H:%M:%S")
        stopTimeObject = datetime.now()
        print("Connection restored at : " + stopTime)
        durationFallout = int((stopTimeObject - startTimeObject).seconds)
        durationFallout = time.strftime("%H:%M:%S", gmtime(durationFallout))
        print("Duration fallout : " + durationFallout)
        f=open(directoryFile,"a+")
        stringWrite = "|    {0}    |        {1}          |        {2}        |       {3}       |\n".format(date, startTime, stopTime, durationFallout)
        f.write(stringWrite)
        f.close()

    time.sleep(2)