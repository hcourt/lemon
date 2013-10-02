#!/usr/bin/python
#fsm

import sys
import ConfigParser
import re

file = sys.argv[1]
input = sys.argv[2]

class FSM (object):
    def __init__(self):
        self.states = []
        self.start = ""
        self.end = ""
        self.transitions = {} #transitions is a dictionary of (string, array of (destination-state, expected-value) tuples)

def readFSM(f):
    config = ConfigParser.ConfigParser()
    config.read(f)    
    result = FSM()
    names = config.get("states", "names")
    result.start = config.get("states", "start")
    result.end = config.get("states", "end")
    names = re.split('\W+', names)
    for n in names: #for each state
        if (n == ''):
            continue
        result.states.append(n)
        trans = config.get("transitions", n)
        trans=re.split('[^a-zA-Z0-9_\:\*]', trans)
        result.transitions[n] = []
        theseTrans = []
        for t in trans: #for each transition associated with the state
            if (t == ''):
                continue
            if (t in theseTrans):
                print("Error: FSM sent was non-deterministic")  #Error detection for non-deterministic FSMs
                return
            theseTrans.append(t)
            t = re.split('[^a-zA-Z0-9_\*]', t)
            #print t
            result.transitions[n].append((t[1], t[0]))
                
    result.states.append("error")
    return result
def runFSM(fsm, input):
    current = fsm.start
    last = fsm.end
    fsm.transitions
    default = "" #the default '*' state
    progress = 0
    accept = 0 #accept will be -1 if error state, 1 if accept state, and 0 if indeterminate.
    i=0
    while(accept == 0): #loop through elements of the input string while detecting the acceptance state
        if (current == last):
            accept = 1
            continue
        if (current == "error" or i == len(input)):
            accept = -1
            continue
        for j in range(0, (len(fsm.transitions[current]))):
            if (fsm.transitions[current][j][1] == "*"):
                default = fsm.transitions[current][j][0]
            if (fsm.transitions[current][j][1] == input[i]):
                current = fsm.transitions[current][j][0]
                progress = 1
                if (i == len(input) - 1):
                    accept = 1
                break
        if (default != ""):
            current = default
            default = ""
            continue
        if (progress != 1):
            print ("Error: FSM was non-exhaustive") #error detection for non-exhaustive FSMs.  I was not entirely sure what you meant by non-exhaustive, so this is how I am interpreting it: as a sequence-detector
            return 0
        progress = 0
        i=i+1
    return accept
r = runFSM(readFSM(file), input)
if (r == -1):
    print("Reject")
elif (r == 1):
    print("Accept")
else: print("Error.  Exitting...")