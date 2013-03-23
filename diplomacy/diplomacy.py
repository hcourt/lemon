#!/usr/bin/python
#Hazel Court
import sys
import webbrowser
import location
import game

countries=[None,None,None,None,None,None,None]
defaultplayers=["Austria", "England", "France", "Germany", "Italy", "Russia", "Turkey"]
defaulttimes=[10,10,10]
times=[0,0,0]

def error(str):
    print ("ERROR: "+str)
    return

#top menu, allows viewing rules, setting defaults, starting a game, and quitting
def top_menu ():
    i=""
    while (i!="Q"):
        print("-----*-----Top Menu-----*-----")
        print("+View [R]ules")
        print("+View [C]onditions")
        print("+Set [P]layer Locations")
        print("+Set [T]ime Limits")
        print("+Start [G]ame")
        print("+[Q]uit")
        i=raw_input(">")
        
        if (i=="R"):
            view_rules()
        elif (i=="C"):
            view_conditions()
        elif (i=="P"):
            set_loc("user")
        elif (i=="T"):
            set_time("user")
        elif (i=="G"):
            start_game()
        elif (i!="Q"):
            error("Invalid option.")
    return
#open a browser to the latest (2000) rules pdf    
def view_rules():
    new = 2
    webbrowser.open("http://www.diplomacy-archive.com/resources/rulebooks/2000AH4th.pdf", new=new)
    return
def view_conditions():
    print("The current starting conditions are:")
    print("Player....Country")
    print("----------------")
    pnum=1
    for c in countries:
        print(str(pnum)+"........."+c.name)
        pnum+=1
    print("Move Phase: "+str(times[0])+" minutes")
    print("Retreat Phase: "+str(times[1])+" minutes")
    print("Build Phase: "+str(times[2])+" minutes")
    return
#generate the starting countries through default (alphabetical order) or user input
def set_loc(mode):
    players=[]
    countrylist=[]
    for p in defaultplayers:
        countrylist.append(p)
    pnum=1
    if (mode=="user"):
        print("Set each player's starting country (Austria, England, France, Germany, Italy, Russia, Turkey).")
        num=0
        while (num<7):
            c=raw_input("Enter player "+str(num+1)+"'s starting country > ")
            if c in countrylist:
                players.append(c)
                countrylist.remove(c)
                num+=1
            else:
                error("Invalid country name.")
        for p in players:
            countries[pnum-1]=location.Country(p, pnum)
            pnum+=1
    elif (mode=="default"):
        for p in defaultplayers:
            countries[pnum-1]=location.Country(p, pnum)
            pnum+=1
    return
#ask for times through user input or set default times
def set_time(mode):
    if (mode=="user"):
        print("Set each phase's time limit, in integer minutes.")
        times[0]=int(raw_input("Enter time limit for move order submission > "))
        times[1]=int(raw_input("Enter time limit for retreat order submission > "))
        times[2]=int(raw_input("Enter time limit for build order submission > "))
    elif(mode=="default"):
        times[0]=defaulttimes[0]
        times[1]=defaulttimes[1]
        times[2]=defaulttimes[2]
    return
#begin a game
def start_game():
    print("-----*-----New Game-----*-----")
    g=game.Game(countries,times)
    g.start()    
    return
#welcome message that starts the top menu
def welcome():
    print("Welcome to Diplomacy!")
    print("A Game of International Intrigue, Trust, and Treachery")
    set_loc("default")
    set_time("default")
    top_menu()
    print("Goodbye!")
    
    
welcome()