from asyncore import read
import telnetlib
from datetime import date
# telnetlib documentation https://docs.python.org/3/library/telnetlib.html

# guide to use python3 scripts in linux
# step 1: navigate to a memorable folder where you will store the script (good examples would be home directory or /usr/local/bin)
# step 2: use curl (client URL) to download the script from my github. command = curl -LJO raw.githubusercontent.com/JDFSHU/lab_code/master/nsmc_backup.py
# step 4: check file has downloaded by using command ls, notice that it is in white, needs to be in green to be recognised as a script that is executable
# step 5: give execute permissions to the file with command sudo chmod +x nsmc_backup.py
# step 6: ensure the HOST and tn.write(b"cisco\n") lines 15 and 31 match your switch/lab
# step 7: run script by using command = python3 nsmc_backup.py

today = date.today()
HOST = "10.1.1.254"  # Device IP address goes here

# will prompt upon script being ran, enter local username and passwords to access device via telnet
user = input("Enter Username: ")
password = input("Enter Password: ")

# telnet library connecting to host
tn = telnetlib.Telnet(HOST)
tn.read_until(b"Username: ")
tn.write(user.encode("ascii") + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode("ascii") + b"\n")

# each tn.write line will write the command in quotes to the device. * must be prepended with a b to specify bytes type.
tn.write(b"enable\n")
tn.write(b"cisco\n")  # put your enable mode password in here
# enables the device to print the full running config to the terminal without paging
tn.write(b"terminal length 0\n")
tn.write(b"show run\n")
tn.write(b"exit\n")

readOutput = tn.read_all()  # reads everything the script has output
# saves to file consisting of (IP) Running Config (Todays Date)
saveOutput = open(f"{HOST} :config backup: {today}", "w")
saveOutput.write(readOutput.decode("ascii"))
saveOutput.write("\n")
saveOutput.close
