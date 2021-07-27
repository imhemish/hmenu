# Hmenu
Hmenu is a dmenu like program for Windows written in Python and PySimpleGUI library. It is very minimal now with a basic feature at all. More documentation and more features would be added in future.

# Installation
To install hmenu, clone or download the repo, copy the "hmenu.pyw" to some place that you will remember and then edit the listener.pyw file to edit where you placed the "hmenu.pyw" file in the line "start C:\\Users\\User......." whatever the path is.
You need to put double slashes as an escape sequence.
After that, put the listener file in your startup folder, generally availalbe at  C:\Users\User\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup where User is your username

# Configuration
Hmenu creates a folder and file on first run in your home directory. The directory would be named ".hmenu".
Inside it, you would find file "hmenu.conf". The syntax of configuration is:  
<the_name_by_which_you_will_call_command>**<command / shortuct path / binary path>  
The ** sepratior is necessary to separate both fields
You may contact the maintainer through email to know more

# Usage
When you will restart your computer, listener file would be activated automatically because of being placed in startup folder. Then hmenu is accesible through shortcut "Ctrl+Shift+Z". It would automatically focus to itself and you can give input in textob and it will show most matching command next to it. When you press F1: it executes most matching command. If you press Esc, it quits.