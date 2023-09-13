import sys
import os
import json
import subprocess

monitorMustBeAlone = False

def displayError(error):
    print(error)
    input("Press any key to exit...")
    exit()

if len(sys.argv) < 2:
    displayError("Usage: python script.py --search|--config|--submit")

# Fetching monitors and counting them
text = subprocess.check_output('cmd /c "WMIC /NameSpace:\\\\Root\\WMI Path WmiMonitorID Get /format:value"', shell=True, text=True)
splitArray = text.split()
arrayLength = len(splitArray)
amountOfMonitorsTotal = int(arrayLength / 9)

print(splitArray)


finalMonitorArray = [[],[],[]]
arrayCounter = 0

for i in range(0, amountOfMonitorsTotal):
    for j in range(0, 9):
        finalMonitorArray[i].append(splitArray[arrayCounter])
        arrayCounter += 1


if sys.argv[1] == "--search":
    print(f"\n{amountOfMonitorsTotal} screens were found connected to this system\n")
    for i in range(len(finalMonitorArray)):
        print(f"{i + 1}: {finalMonitorArray[i][1][21:28]}, from year: {finalMonitorArray[i][8][18:]}")

elif sys.argv[1] == "--config":
    print(f"\n{amountOfMonitorsTotal} screens were found connected to this system\n")
    for i in range(len(finalMonitorArray)):
        print(f"{i + 1}: {finalMonitorArray[i][1][21:28]}, from year: {finalMonitorArray[i][8][18:]}")
    
    chosenMonitorIndex = input("Choose which screen to configure: (integer): ")
    while True:
        try:
            chosenMonitorIndex = int(chosenMonitorIndex) - 1
            break
        except ValueError:
            displayError(f"\"{chosenMonitorIndex}\" is not a valid integer")
    
    if chosenMonitorIndex < 0 or chosenMonitorIndex > len(finalMonitorArray) - 1:
        displayError(f"\"{chosenMonitorIndex + 1}\" does not correspond to a screen on this device")

    chosenMonitorName = finalMonitorArray[chosenMonitorIndex][1][21:28]

    mustMonitorBeAlone = input(f"Do you want this screen: \"{chosenMonitorName}\" to be the only enabled screen to trigger a reaction? (y/n): ")

    if mustMonitorBeAlone.lower() in ["y", "yes", "yeah", "sure"]:
        monitorMustBeAlone = True
    elif mustMonitorBeAlone.lower() not in ["n", "no", "nope"]:
        displayError(f"Could not interpret user answer \"{mustMonitorBeAlone}\"")
    
    programPath = input("Please input the absolute path to your program (eg. C:\Program Files\program.exe): ")

    print(f"Selected program path: {programPath}")

    # initialize testing of program path
    testAnswer = input("Do you want to test the path to make sure it's working correctly? This will try to start selected program. (y/n): ")
    if testAnswer.lower() in ["y", "yes", "yeah", "sure"]:
        testWorked = False
        while testWorked == False:
            subprocess.Popen(programPath)
            testAnswer = input("If the program did not work and you want to change path and test again, type \"test\", otherwise press any key... ")
            if testAnswer.lower() == "test":
                programPath = input("Please re-input the absolute path to your program (eg. C:\Program Files\program.exe): ")
            else:
                testWorked = True
    elif testAnswer.lower() not in ["n", "no", "nope"]:
        displayError(f"Could not interpret user answer \"{mustMonitorBeAlone}\"")
    else:
        testWorked = True
    
    # save stuff into csv file
    config = {
        "chosenScreen": finalMonitorArray[chosenMonitorIndex][1],
        "chosenProgram": programPath,
        "mustMonitorBeAlone": monitorMustBeAlone
    }

    # Serialize
    configFile = json.dumps(config, indent=4)

    # Write to document
    with open("config.json", "w") as configDoc:
        configDoc.write(configFile)

    # done
    print("You are now configured! Please run \"python script.exe --submit\" to add it into Windows auto-startup")


elif sys.argv[1] == "--submit":
    pass

else:
    displayError(f"The following command-line argument: \"{sys.argv[1]}\" is not supported")









# print(finalMonitorArray)

# amountOfScreensTurnedOn = 0

if finalMonitorArray[0][1] == "InstanceName=DISPLAY\\PHL04C3\\5&amp;17341336&amp;0&amp;UID37125_0" and amountOfMonitorsTotal == 1:
    subprocess.Popen("C:\\Program Files (x86)\\Steam\\steam.exe -bigpicture")