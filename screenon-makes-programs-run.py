import sys
import os
import json
import shutil
import subprocess

monitorMustBeAlone = False


def displayError(error):
    print(error)
    # input("Press any key to exit...")
    exit()


if len(sys.argv) < 2:
    displayError(
        "Usage: python screenon-makes-programs-run.py --search|--config|--submit|--remove"
    )

# Fetching monitors and counting them
text = subprocess.check_output(
    'cmd /c "WMIC /NameSpace:\\\\Root\\WMI Path WmiMonitorID Get /format:value"',
    shell=True,
    text=True,
)
splitArray = text.split()
arrayLength = len(splitArray)
amountOfMonitorsTotal = int(arrayLength / 9)

# print(splitArray)


finalMonitorArray = []
for i in range(amountOfMonitorsTotal):
    finalMonitorArray.append([])
arrayCounter = 0

for i in range(0, amountOfMonitorsTotal):
    for j in range(0, 9):
        finalMonitorArray[i].append(splitArray[arrayCounter])
        arrayCounter += 1


if sys.argv[1] == "--search":
    print(f"\n{amountOfMonitorsTotal} screens were found connected to this system\n")
    for i in range(len(finalMonitorArray)):
        print(
            f"{i + 1}: {finalMonitorArray[i][1][21:28]}, from year: {finalMonitorArray[i][8][18:]}"
        )
        # print(f"{i + 1}: {finalMonitorArray[i][1]}, from year: {finalMonitorArray[i][8][18:]}") # remove!

    print(
        "\nTIP: In order to know which screen is which you can try to turn of or disconnect one or more screens and run this command again."
    )

elif sys.argv[1] == "--config":
    print(f"\n{amountOfMonitorsTotal} screens were found connected to this system\n")
    print(
        "\n❗Remember that depending on some screens not registered as disconnected when turned off could lead to some functionality of this script to not work as intended! This is due to how some connections are constantly registered as turned on even though the screen itself is turned off. \n"
    )
    for i in range(len(finalMonitorArray)):
        print(
            f"{i + 1}: {finalMonitorArray[i][1][21:28]}, from year: {finalMonitorArray[i][8][18:]}"
        )

    chosenMonitorIndex = input("Choose which screen to configure: (integer): ")
    while True:
        try:
            chosenMonitorIndex = int(chosenMonitorIndex) - 1
            break
        except ValueError:
            displayError(f'"{chosenMonitorIndex}" is not a valid integer')

    if chosenMonitorIndex < 0 or chosenMonitorIndex > len(finalMonitorArray) - 1:
        displayError(
            f'"{chosenMonitorIndex + 1}" does not correspond to a screen on this device'
        )

    chosenMonitorName = finalMonitorArray[chosenMonitorIndex][1][21:28]

    mustMonitorBeAlone = input(
        f'Do you want this screen: "{chosenMonitorName}" to be the only enabled screen in order to trigger a reaction? (y/n): '
    )

    if mustMonitorBeAlone.lower() in ["y", "yes", "yeah", "sure"]:
        monitorMustBeAlone = True
    elif mustMonitorBeAlone.lower() not in ["n", "no", "nope"]:
        displayError(f'Could not interpret user answer "{mustMonitorBeAlone}"')

    programPath = input(
        "Please input the absolute path to your program (eg. C:\\Program Files\\program.exe): "
    )

    print(f"Selected program path: {programPath}")

    addFlags = input(
        "Do you want to add any arguments to start the file with? (eg. -f, -bigpicture) (y/n): "
    )
    if addFlags.lower() in ["y", "yes", "yeah", "sure"]:
        flags = input(
            'Please input your arguments as follows: "-i -force -startminimized": '
        )
        print(f"You arguments are now registered as: {flags}")
    elif addFlags.lower() in ["n", "no", "nope"]:
        print("No arguments will be added.")
        flags = ""
    else:
        displayError(f'Could not interpret user answer "{addFlags}"')

    # initialize testing of program path
    testAnswer = input(
        "Do you want to test the path and arguments to make sure it's working correctly? This will try to start selected program. (y/n): "
    )
    if testAnswer.lower() in ["y", "yes", "yeah", "sure"]:
        testWorked = False
        while testWorked == False:
            print(programPath + flags)
            subprocess.Popen(programPath + " " + flags)
            # try:
            # except:
            #     print("Some error was thrown, make sure the selected path is correct and you have permission to access selected file.")
            testAnswer = input(
                'If the program did not work and you want to change path or arguments and test again, type "test", otherwise press any key..: '
            )
            if testAnswer.lower() == "test":
                programPath = input(
                    "Please re-input the absolute path to your program (eg. C:\\Program Files\\program.exe): "
                )
                flags = input(
                    'Please re-input your arguments as follows: "-i -force -startminimized" (keep empty if no arguments should be used): '
                )
            else:
                testWorked = True
    elif testAnswer.lower() not in ["n", "no", "nope"]:
        displayError(f'Could not interpret user answer "{mustMonitorBeAlone}"')
    else:
        testWorked = True

    # save stuff into csv file
    config = {
        "chosenScreen": finalMonitorArray[chosenMonitorIndex][1],
        "chosenProgram": programPath,
        "chosenArgs": flags,
        "mustMonitorBeAlone": monitorMustBeAlone,
    }

    # Serialize
    configFile = json.dumps(config, indent=4)

    # Write to document
    with open("config.json", "w") as configDoc:
        configDoc.write(configFile)

    # done
    print(
        'You are now configured! Please run "python screenon-makes-programs-run.py --submit" to add it into Windows auto-startup'
    )


elif sys.argv[1] == "--submit":
    # importing current settings
    fileConfig = open("config.json")
    submitJsonData = json.load(fileConfig)
    # print(submitJsonData)

    try:
        print("Are you sure you want to submit and plant this configuration?: \n")
        print(f"Selected Screen: {submitJsonData['chosenScreen'][21:28]}")
        print(f"Chosen Program Path: {submitJsonData['chosenProgram']}")
        print(f"Chosen Program Arguments: {submitJsonData['chosenArgs']}")
        print(
            f"Must Monitor be the only enabled screen in order to trigger a reaction?: {submitJsonData['mustMonitorBeAlone']}"
        )
    except KeyError:
        displayError(
            'Oops! Something went wrong, are you sure you have ran "python screenon-makes-programs-run.py --config" yet?'
        )

    submitAnswer = input("\nType y/n: ")
    if submitAnswer.lower() in ["y", "yes", "yeah", "sure"]:
        fileConfig.close()
        username = os.getenv("USERNAME")
        currentDirectory = os.getcwd()

        print(f"Applying for user: {username}")
        print(f"from current directory: {currentDirectory}\n")

        if not os.path.exists("C:/custom-scripts/screenon-makes-programs-run/"):
            try:
                if not os.path.exists("C:/custom-scripts"):
                    os.mkdir("C:/custom-scripts")
                os.mkdir("C:/custom-scripts/screenon-makes-programs-run")
                print("✅ Created script directory")
            except:
                displayError(
                    "❌ Could not create script directory, please make sure you have permission to write to your C:\\ drive"
                )

        try:
            shutil.move(
                "config.json",
                "C:/custom-scripts/screenon-makes-programs-run/config.json",
            )
            print("✅ Moved config to script file.")
        except:
            displayError(
                "❌ Could not move config to script folder, please make sure you have permission to write to your C:\\ drive"
            )

        try:
            shutil.copyfile(
                "screenon-makes-programs-run.py",
                "C:/custom-scripts/screenon-makes-programs-run/script.py",
            )
            print("✅ Copied script to script file")
        except:
            displayError(
                "❌ Could not copy script to script folder, please make sure you have permission to write to your C:\\ drive"
            )

        try:
            fullPath = f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\screenon-makes-programs-run.bat"
            batScript = open(rf"{fullPath}", "w+")
            batScript.write(
                "@ECHO OFF\n python C:\\custom-scripts\\screenon-makes-programs-run\\script.py --run"
            )
            batScript.close()
            print("✅ Created Batch file to run on autostart.")
            print(fullPath)
        except:
            displayError(
                "❌ Could not create batch file in windows autorun folder, please make sure you have permission to write to C:\\ drive"
            )

        print("\n\n✅ Done!")

    elif submitAnswer.lower() not in ["n", "no", "nope"]:
        displayError("Canceled Submission.")
    else:
        displayError(f'Could not interpret user answer "{submitAnswer}"')

elif sys.argv[1] == "--remove":
    removeAll = input("Remove SONMPRUN script and all it's configured files? (y/n): ")
    print("\n")

    if removeAll.lower() in ["y", "yes", "yeah", "sure"]:
        # removing script
        if os.path.exists("C:/custom-scripts/screenon-makes-programs-run/"):
            try:
                shutil.rmtree("C:/custom-scripts/screenon-makes-programs-run/")
                print("✅ Successfully removed script directory")
            except:
                displayError(
                    "❌ Could not remove script directory, please make sure you have permission to write to your C:\\ drive"
                )
        else:
            print("✅ No script directory was found")

        # removing startup
        fullPath = f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\screenon-makes-programs-run.bat"
        if os.path.exists(fullPath):
            try:
                os.remove(fullPath)
                print("✅ Successfully removed startup script")
            except:
                displayError(
                    "❌ Could not remove startup script, please make sure you have permission to write to your C:\\ drive"
                )
        else:
            print("✅ No startup script was found")

        print("\n")
        print("✅ Successfully removed all active configurations of SONMPRUN!")
    else:
        displayError("❌ Cancelled.")

elif sys.argv[1] == "--run":

    # import settings
    fileConfig = open("config.json")
    config = json.load(fileConfig)

    # print(finalMonitorArray)

    if config["mustMonitorBeAlone"] == True:
        if (
            finalMonitorArray[0][1] == config["chosenScreen"]
            and amountOfMonitorsTotal == 1
        ):
            subprocess.Popen(config["chosenProgram"] + " " + config["chosenArgs"])
    else:
        nameList = []
        for i in range(len(finalMonitorArray)):
            nameList.append(finalMonitorArray[i][1])
        # print(nameList)
        if config["chosenScreen"] in nameList:
            subprocess.Popen(config["chosenProgram"] + " " + config["chosenArgs"])


else:
    displayError(
        f'The following command-line argument: "{sys.argv[1]}" is not supported'
    )


# print(finalMonitorArray)

# amountOfScreensTurnedOn = 0
