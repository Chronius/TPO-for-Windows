import subprocess
import os

diskpart = 'DISKPART /s listdisk.txt'
format_script = 'diskpart /s outputscript.txt'

dir_stressdisk = "resources\soft\stressdisk\\"
cmd = "stressdisk.exe -duration 1s run " #Длительность задается в формате XXhXXmXXsXXusXXns
"""
Full options:
  -cpuprofile string
        Write cpu profile to file
  -duration duration
        Duration to run test (default 24h0m0s)
  -logfile string
        File to write log to set to empty to ignore (default "stressdisk.log")
  -maxerrors uint
        Max number of errors to print per file (default 64)
  -nodirect
        Don't use O_DIRECT
  -s int
        Size of the check files (default 1000000000)
  -stats duration
        Interval to print stats (default 1m0s)
  -statsfile string
        File to load/store statistics data (default "stressdisk_stats.json")
"""

disks_to_check = []

import string
from ctypes import windll

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives

def format_disk():
    with subprocess.Popen(format_script, stdout=subprocess.PIPE) as f:
        for x in f.stdout.readlines():
            print(x.decode("CP866"))

def stressdiskgo(disk_name):
    err_count = 0
    elapsed_t = None
    str = dir_stressdisk + cmd + disk_name+":"

    with subprocess.Popen(str, stderr=subprocess.PIPE) as f:
        while f.poll() is None:
            x = f.stderr.readline()
            #print(x)
            if b"Bytes read" in x or b"Reading file" in x \
                    or b"Writing file" in x or b"Bytes written" in x:
                print(x.decode("CP866"))
            if b"Errors" in x:
                err_count = int(x[24:25])
            if b"Elapsed" in x:
                elapsed_t = x

    if not err_count:
        print("Test OK\n" + elapsed_t.decode("CP866"))
    else:
        print("Test failed\nErrors: ", err_count, "\nElapsed time: ", elapsed_t)

if __name__ == '__main__':

    with subprocess.Popen(diskpart, stdout=subprocess.PIPE) as f:
        for x in f.stdout.readlines():
            print(x.decode("CP866"))

    disk = input("Select testing disk:\t")
    print(disk)

    disk_name = input("Enter the name of the drive:\t")

    output = open("outputscript.txt", "w")

    with open("diskscript.txt", "r") as script:
        for line in script.readlines():
            if "select disk" in line:
                line = "select disk " + disk + '\n'
            if "assign letter=" in line:
                line = "assign letter=" + disk_name + '\n'
            output.writelines(line)
    output.close()

    #uncomment this line if you want to format the drive
    #format_disk()

    print(get_drives())
    stressdiskgo(disk_name)


