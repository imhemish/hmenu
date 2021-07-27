# Imports
from os.path import exists, expanduser, isdir, isfile, join
from os import mkdir, listdir, startfile
from PySimpleGUI import Window, Input, change_look_and_feel, Text
from fuzzywuzzy import fuzz
from toml import load, dump


# Configuration files and folders
def check_configs():
    print("Creating configurations if don't exist")
    if not exists(expanduser("~\\.hmenu.toml")):
        filenew = open(expanduser("~\\.hmenu.toml"), "a")
        new_config_dict = {"read_user_start_items": True, "read_system_start_items": True, "read_user_custom_commands":True, "commands":{"command": "\\path\\to\\binary"}}
        dump(new_config_dict, filenew)
        filenew.close()

# Reading from configuration
def read_config():
    try:
        global read_user_start_items
        global read_system_start_items
        global read_user_custom_commands
        print("Reading from configuration")
        loaded_data = load(expanduser("~\\.hmenu.toml"))
        read_user_start_items = loaded_data["read_user_start_items"]
        read_system_start_items = loaded_data["read_system_start_items"]
        read_user_custom_commands = loaded_data["read_user_custom_commands"]
        cmddict = loaded_data["commands"]
        if read_user_custom_commands:
            return cmddict
        else:
            return {}
    except:
        "Some error occured in configuration parsing"
        exit()



# Functions to parse start menu
def merge_dict(dict1, dict2):
    res = {**dict1, **dict2}
    return res

def get_items(dirName): 
    listOfFile = listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if isdir(fullPath):
            allFiles = allFiles + get_items(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles

def filter_shortcut_files(arr):
    return list(filter(lambda x: x.endswith(".lnk"), arr))

def create_dict_of_commands(arr):
    newdict = {}
    for item in arr:
        newdict[str(item.split("\\")[-1]).replace(".lnk", "")] = item
    return newdict

def parse_start_menu(dir):
    try:
        return create_dict_of_commands(filter_shortcut_files(get_items(dir)))
    except:
        print("Some error occured in parsing start menu items")
        exit()



# Fuzzy searching
def return_fuzzy(command, iter):
    tempdict = {}
    for i in iter:
        tempdict[i] = fuzz.ratio(command, i)
    max_key = max(tempdict, key=tempdict.get)
    return max_key



check_configs()
cmddict = read_config()
if read_user_start_items:
    cmddict = merge_dict(cmddict, parse_start_menu(expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\")))
if read_system_start_items:
    cmddict = merge_dict(cmddict, parse_start_menu("C:\\ProgramData\\Microsoft\\Windows\\Start Menu"))
print(cmddict)
# GUI
print("Creating GUI")
try:
    change_look_and_feel("Dark Green 7")
except:
    print("Some error occured in configuring PySimpleGUI theme")
    exit()
root = Window("Hmenu", layout=[[Input(size=(40, 35)), Text("", key="meratext", size=(200, 35))]], no_titlebar=True, size=(1500, 40), keep_on_top=True, location=(0,0), return_keyboard_events=True)
temp_cmd = "dummy_hmenu_command"
while True:
    try:
        event, val = root.read()
    except:
        print("Some error occured while initialising GUI")
        exit()
    if event == "None" or event == "Exit":
        break
    print("Event: {}, vals: {}".format(event, val))
    if event == "Escape:27":
        print("Killing program due to Escape Key pressed")
        break
    if event == "F1:112":
        print("Executing command '{}' due to F1 key being pressed".format(temp_cmd))
        startfile(cmddict[temp_cmd])
        break
    print("Updating Text field according to search")
    temp_cmd = (return_fuzzy(val[0], cmddict.keys()))
    print("Match: {}".format(temp_cmd))
    root["meratext"].update(value=temp_cmd)
root.close()