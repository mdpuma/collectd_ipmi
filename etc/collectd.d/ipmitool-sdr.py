#!/usr/bin/python

import os
import subprocess
import time

# subprocess.check_output is not exist in python 2.6 which is on centos6
# hostname = os.getenv("COLLECTD_HOSTNAME", subprocess.check_output(["hostname",  "-f"]).strip())

p = subprocess.Popen(["hostname", "-f"], stdout=subprocess.PIPE)
out, err = p.communicate()

hostname = os.getenv("COLLECTD_HOSTNAME", out.strip())
interval = os.getenv("COLLECTD_INTERVAL", "10")
interval = float(interval)

def gettype(name):
    type = name.split(" ")[0]
    if type == "Temp": return "temperature"
    if type == "Fan": return "fanspeed"
    if type == "Power": return "power"
    return "gauge"


while True:
    # out = subprocess.check_output(["ipmitool", "sdr"])
    p = subprocess.Popen(["sudo", "ipmitool", "sdr"], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.split("\n"):
        try:
            name, value, status = line.split("|")
            name = name.strip()
            value = value.strip()
            status = status.strip()

            if status == "ok":
                for word in value.split(" "):
                    try:
                        float(word)

                        print("PUTVAL \"{0}/ipmi/{1}-{2}\" interval={3} N:{4}".format(hostname, gettype(name), name, interval, word))
                        continue
                    except ValueError:
                        pass  # Not a number
        except ValueError:
            pass  # Skip invalid lines
    time.sleep(int(interval))
