# Imports
from os.path import exists, expanduser
from os import mkdir, popen
from PySimpleGUI import Window, Input, change_look_and_feel, Text
from fuzzywuzzy import fuzz


# Configuration files and folders
print("Creating configurations if don't exist")
if not exists(expanduser("~\\.hmenu\\")):
    mkdir(expanduser("~\\.hmenu\\"))
if not exists(expanduser("~\\.hmenu\\hmenu.conf")):
    filenew = open(expanduser("~\\.hmenu\\hmenu.conf"), "a")


# Reading from configuration
print("Reading from configuration")
with open(expanduser("~\\.hmenu\\hmenu.conf"), "r") as conffile:
    cmdslist = conffile.read().split("\n")
cmddict = {}
for i in cmdslist:
    cmddict[str(i.split("**")[0])] = str(i.split("**")[1])
print(cmddict)


# Fuzzy searching
def return_fuzzy(command, iter):
    tempdict = {}
    for i in iter:
        tempdict[i] = fuzz.ratio(command, i)
    max_key = max(tempdict, key=tempdict.get)
    return max_key


# GUI
print("Creating GUI")
change_look_and_feel("Dark Green 7")
root = Window("billa", layout=[[Input(size=(40, 35)), Text("", key="meratext", size=(200, 35))]], no_titlebar=True, size=(1500, 40), keep_on_top=True, location=(0,0), return_keyboard_events=True)
temp_cmd = "dummy"
while True:
    event, val = root.read()
    if event == "None" or event == "Exit":
        break
    print("Event: {}, vals: {}".format(event, val))
    if event == "Escape:27":
        print("Killing program due to Escape Key pressed")
        break
    if event == "F1:112":
        print("Executing command '{}' due to F1 key being pressed".format(temp_cmd))
        cmd = "start {} {}".format(cmddict[temp_cmd], cmddict[temp_cmd])
        popen(str(cmd))
        break
    print("Updating Text field according to search")
    temp_cmd = (return_fuzzy(val[0], cmddict.keys()))
    print("Match: {}".format(temp_cmd))
    root["meratext"].update(value=temp_cmd)
root.close()