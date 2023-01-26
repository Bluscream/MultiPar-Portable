import sys
import os
import subprocess


# Set path of par2j
client_path = "../par2j64.exe"


# Return sub-process's ExitCode
def command(cmd):
    ret = subprocess.run(cmd, shell=True)
    return ret.returncode


# Return zero for empty folder
def check_empty(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += check_empty(entry.path)
            if total > 0:
                break
    return total


# Read arguments of command-line
for idx, arg in enumerate(sys.argv[1:]):
    one_path = arg
    one_name = os.path.basename(one_path)

    # Check the folder exists
    if os.path.isdir(one_path) == False:
        print(one_name + " isn't folder.")
        continue

    # Check empty folder
    if check_empty(one_path) == 0:
        print(one_name + " is empty folder.")
        continue

    print(one_name + " is folder.")

    # Path of creating PAR file
    par_path = one_path + "\\" + one_name + ".par2"

    # Check the PAR file exists already
    if os.path.exists(par_path):
        print(one_name + " includes PAR file already.")
        continue

    # Set command-line
    # Cover path by " for possible space
    cmd = "\"" + client_path + "\" c /sm2048 /rr20 /rd1 /rf3 \"" + par_path + "\" *"

    # Process the command
    print("Creating PAR files.")
    error_level = command(cmd)

    # Check error
    # Exit loop, when error occur.
    if error_level > 0:
        print("Error=", error_level)
        break

# If you don't confirm result, comment out below line.
input('Press [Enter] key to continue . . .')
