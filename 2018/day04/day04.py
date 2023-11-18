from collections import defaultdict

import re

guard  = re.compile(R"\[.*\] Guard #(.*) begins shift")
asleep = re.compile(R"\[.* 00:(.*)\] falls asleep")
wakes  = re.compile(R"\[.* 00:(.*)\] wakes up")

filename = "input.txt"

with open(filename) as f:
    lines = sorted(line.strip() for line in f)
    gid = None
    sleepytime = defaultdict(int)
    minutes = defaultdict(lambda: defaultdict(int))
    fellasleep = None
    
    for line in lines:
        if m := guard.match(line):
            gid = int(m.group(1))
            #print(gid)
        if m := asleep.match(line):
            fellasleep = int(m.group(1))
            #print(fellasleep)
        if m := wakes.match(line):
            wokeup = int(m.group(1))
            sleepytime[gid] += wokeup - fellasleep

            for m in range(fellasleep, wokeup):
                minutes[gid][m] += 1

    _,sleepiest = max((sleep,gid) for gid,sleep in sleepytime.items())
        
    _,m = max((time,minu) for minu,time in minutes[sleepiest].items())

    print(sleepiest)
    print(m)
    print(m * sleepiest)

    _,gid,minu = max((minutes[guard][minu],guard,minu)
        for minu in range(60)
        for guard in minutes.keys())

    print(gid * minu)
