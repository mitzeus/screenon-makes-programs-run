![alt text](https://github.com/wootkennziz/cs50-final-project/blob/main/logo.png?raw=true)

# Screen-ON Makes Programs RUN

#### Video Demo: <URL HERE>

#### Platform: Windows

#### Description:

Screen-ON Makes Programs RUN (SONMPRUN) is an all-in-one IFTTT (If This Then That) solution for automating your screen-on state to run whatever you want on your PC whenever you turn it on!

This script is created with python together with standard libraries such as os and shutil and uses command-line arguments to control all currently implemented methods including:

### --search:

The `--search` argument will fetch all currently connected screens from your device and display them with name and year of manufacturing.

### --config:

The `--config` argument will allow the user to configure the behaviour of the script by giving the user several input prompts to ultimately setup a config.json file in the directory of the SONMPRUN script file. This includes configuring:

##### Selected Screen:

Takes an integer as input chosen out of the generated screen list

##### Chosen Program Path:

The absolute path to some file, eg. "C:\Program Files (x86)\{program-folder}\{program.exe}"

##### Chosen Program Arguments:

Takes a string formatted as "-startminimized -forcevsync" etc. to run the chosen program path with.

##### If Monitor must be the only enabled screen in order to trigger a reaction:

Takes a boolean value (y/n) to require/not require a screen to be the only one turned on to trigger the SONMPRUN script.

### --submit:

The `--submit` argument will create all necessary files to run the SONMPRUN script at PC startup with the configuration generated in `--config`, copying the configuration and script to a script folder located at "C:\custom-scripts\screenon-makes-programs-run" and creating a batch file in windows startup directory to execute the program when user logs in to the system.

##

With the use of a WMIC windows command-prompt script SONMPRUN can get the WmiMonitorID information into an unorganized string form and thereafter structures the data to be able to handle it appropriately in all steps. This also allows the script to further use and display appropriate data about every screen if this functionality is implemented in the future.

Although much of the process of developing the SONMPRUN script together with native OS screen device fetching was inherently quite difficult, the result of this implementation is quite satisfactory for the moment. The disadvantage of using WMIC to get data about the device is as mentioned before that the data is not formatted in any way, except converted into a simple string, which surely makes UX and further development quite complicated in some aspects.

There may be other, much better ways to implement the same functionality, but at the moment this way suffices for the simple purpose it has.

## Instructions

### 1. Extraction

Extract the files downloaded from `Github releases` into any folder, desirably it's own folder with the file: `screenon-makes-programs-run.py` in it.

### 2. Running

Open a Terminal window in the directory of the `screen-on-makes-programs-run.py` file. It could look something like

    Microsoft Windows [Version XX.X.XXXXX.XXXX]
    (c) Microsoft Corporation. All rights reserved.

    C:\Users\{current_user}\Downloads\screen-on-makes-programs-run> _

Before running the following command, make sure you have the latest version of Python installed on your PC first! (download at https://www.python.org/downloads/)

Then, in your Terminal run:

    python screenon-makes-programs-run.py

followed by what method to run: --search|--config|--submit.

## Configuring

To configure the script, run:

    python screenon-makes-programs-run.py --config

and go through all steps until `"You are now configured! Please run \"python script.exe --submit\" to add it into Windows auto-startup"` is displayed. More information about each setting is found under the `Description` title above.

## Submitting

To submit your configuration made in `Configuring` above, run:

    python screenon-makes-programs-run.py --submit

and it will ask you to verify the configuration by prompting for a y/n, and then will apply all changes to windows startup and copy the necessary files to it's directory.

## If I get an error or unusual behaviour

If any error message or similar is displayed, please try to download the script again from `Github Releases` and try again.

If the problem is not resolved after reinstall, you may experience issues because of some screen's behaviour of not being registered as disconnected when the screen is off, this should be resolved by physically unplugging the screen.

## Removing

To remove this script from your computer, you need to delete the following:

The folder:

    C:\custom-scripts\screenon-makes-programs-run\

with `script.py` and `config.json` inside it,

and the startup script located as:

    C:\Users\{current_user}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\screenon-makes-programs-run.bat

...

This folder can also be accessed by opening Run: `Windows + R` and typing

    shell:startup
