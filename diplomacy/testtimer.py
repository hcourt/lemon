#!/usr/bin/python
import sys
from threading import Timer

def go():
    while(True):
        print("GOGOGO")

t=Timer(30, go)

t.start()
while(True):
    c=raw_input("Enter c or d or q > ")
    if (c=="c"):
        print("Got c")
    if (c=="d"):
        print("Got d")
    if (c=="q"):
        print("Bye!")
        sys.exit(0)

    