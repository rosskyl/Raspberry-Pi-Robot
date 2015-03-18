import os
from sys import argv


jobs = os.popen("ps aux | grep 'setMotors.py'").read().rstrip()

jobs = jobs.split('\n')

for i in range(len(jobs)):
    jobs[i] = jobs[i].split()


for job in jobs:
    os.popen("sudo kill " + job[1])

if len(argv) == 2:
    os.popen("sudo python3 setMotors.py " + argv[1] + " " + argv[2])
elif len(argv) == 1:
    os.popen("sudo python3 stopMotors.py")
