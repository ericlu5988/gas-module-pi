#!/usr/bin/env python3
from mq2 import *
import sys, time

#try:
#    print("Press CTRL+C to abort.")
mq = MQ()
#except:
#    print("unable to calibrate...exiting")
#    exit()


while True:
    try:
        perc = mq.MQPercentage()
        print("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
        time.sleep(0.5)

    except:
        print("EXCEPTION HANDLING: PASS")
        pass
