#!/usr/bin/python

import sys
import webbrowser
import location
import adjudicator
from threading import Timer
import itertools

time_limit_list=[0,0,0]
country_player_list=[None,None,None,None,None,None,None]
neutral_country=None
all_country_list=[]

def error(str):
    print ("ERROR: "+str)
    return

class Game(object):
    def __init__(self,clist,tlist):
        for n in range(0,7):
            country_player_list[n]=clist[n]
        time_limit_list[0]=tlist[0]
        time_limit_list[1]=tlist[1]
        time_limit_list[2]=tlist[2]
        self.judge=adjudicator.Adjudicator()
        self.current_year=1901
        
    def start(self):
        neutral_country=location.Country("Neutral",0)
        neutral_country.start_provinces()
        for c in country_player_list:
            c.start_provinces()
            all_country_list.append(c)
        all_country_list.append(neutral_country)
        self.cycle()
        return
        
    def cycle(self):
        self.current_year=1901
        while (self.check_victory()==0):
            self.run_year()
            self.current_year+=1
        print("Victory for Player "+str(self.check_victory()))
        return        
        
    def run_year(self):
        print("The year is "+str(self.current_year)+".")
        self.run_spring()
        self.run_fall()
        return
    
    def run_spring(self):
        print("Spring has arrived.")
        self.expect_move()
        if (self.check_retreat()!=[]):
            print("Spring continues.")
            self.expect_retreat(self.check_retreat())
        return
        
    def run_fall(self):
        print("Fall has arrived.")
        self.expect_move()
        if (self.check_retreat()!=[]):
            print("Fall continues.")
            self.expect_retreat(self.check_retreat())
        if (self.check_build()!=[]):
            print("Fall continues.")
            self.expect_build(self.check_build())
        return
        
    def expect_move(self):
        t=Timer(time_limit_list[0]*60,self.process_move)
        print("Now accepting move orders.")
        print("Please enter orders into your appropriate player#.txt file.  Move adjudication will commence in "+str(time_limit_list[0])+" minutes.")
        t.start()
        if(self.interim_menu()=="go"):
            t.cancel()
            self.process_move()
        return
    
    def process_move(self):
        print("Orders are now in.")
        master_orders=self.judge.move(all_country_list)
        print("Orders processed.")
        self.end_state(master_orders)
        return
        
    def end_state(self,master_orders):
        for p in master_orders.keys():
            print("---Player "+str(p)+"'s Orders---")
            for o in master_orders[p]:
                print " ".join(o)
        self.execute_orders(master_orders)
        #confirm=""
        #while (True):
        #    confirm=raw_input("Are these orders acceptable? (y/n) > ")
        #    if (confirm=="y"):
        #        break
        #    elif (confirm=="n"):
        #        
        #    else:
        #        error("Invalid option")
        return
        
    def expect_retreat(self,players_to_retreat):
        t=Timer(time_limit_list[1]*60,self.process_retreat)
        print("Now accepting retreat and destroy orders.")
        print("Players who must retreat at least one unit:")
        self.judge.retreat_players=[]
        for p in players_to_retreat:
            print p
            self.judge.retreat_players.append(p)
        print("Please enter orders into your appropriate player#.txt file.  Retreat adjudication will commence in "+str(time_limit_list[1])+" minutes.")
        t.start()
        self.interim_menu()
        if(self.interim_menu()=="go"):
            t.cancel()
            self.process_retreat()
        return
        
    def process_retreat(self):
        print("Orders are now in.")
        units=[]
        for c in country_player_list:
            units=(c.dislodged_units)
        units=list(itertools.chain.from_iterable(units))
        master_orders=self.judge.retreat(country_player_list,units)
        print("Orders processed.")
        self.end_state(master_orders)
        return
        
    def expect_build(self, players_to_build):
        t=Timer(time_limit_list[2]*60,self.process_build)
        print("Now accepting build and destroy orders.")
        print("Players who must build or destroy at least one unit:")
        self.judge.build_players=[]
        for p in players_to_build:
            print p
            self.judge.build_players.append(p)
        print("Please enter orders into your appropriate player#.txt file.  Build adjudication will commence in "+str(time_limit_list[2])+" minutes.")
        t.start()
        self.interim_menu()
        if(self.interim_menu()=="go"):
            t.cancel()
            self.process_build()
        return
        
    def process_build(self):
        print("Orders are now in.")
        
        master_orders=self.judge.build(country_player_list,)
        print("Orders processed.")
        self.end_state(master_orders)
        return
    
    def interim_menu(self):
        i=""
        while(i!="P"):
            all_countries=["Austria", "England", "France", "Germany", "Italy", "Russia", "Turkey"]
            print("-----*---Interim Menu---*-----")
            print("+Manually [P]rogress")
            print("+Declare [T]ie Conditions")
            print("+Declare [S]urrender")
            i=raw_input(" > ")
            if (i=="T"):
                while(True):
                    print("Enter countries that will draw together.  Enter F to finish.")
                    countries=[]
                    country=""
                    while(country!="F"):
                        country=raw_input(" > ")
                        if (country in all_countries):
                            countries.append(country)
                            all_countries.remove(country)
                        elif(country!="F"):
                            error("Invalid country name")
            elif (i=="S"):
                country=""
                while(True):
                    country=raw_input("Which country will surrender? > ")
                    if (country in country_player_list):
                        country_player_list[country_player_list.index(country)].surrender()
                        break
                    else:
                        error("Invalid country name.")
            elif (i!="P"):
                error("Invalid option.")
        
        return("go")
    def check_victory(self):
        sc_values=[0,0,0,0,0,0,0]
        for c in country_player_list:
            for p in c.provinces:
                if p.is_sc:
                    sc_values[c.player-1]+=1
        for n in range(0,7):
            if sc_values[n]>17:
                return n+1
        return 0
    def check_retreat(self):
        ret=[]
        for c in country_player_list:
            if c.dislodged_units!=[]:
                ret.append(c.player)
        return ret
    def check_build(self):
        ret=[]
        sc_values=[0,0,0,0,0,0,0]
        for c in country_player_list:
            for p in c.provinces:
                if p.is_sc:
                    sc_values[c.player-1]+=1
        for n in range(0,7):
            if sc_values[n]!=len(country_player_list[n].unit_locations):
                ret.append(n+1)
        return ret
    def execute_orders(self,molist):
        for orders in molist.values():
            for olist in orders:
                if olist[0]=="Convoy resolved.":
                    cp=judge.get_province(olist[-2])
                    cm=judge.get_province(olist[-1])
                    u=cp.unit
                    u.loc=cm
                    cp.unit=None
                    cm.unit=u
                    u.country.unit_locations.remove(cp.name)
                    u.country.unit_locations.append(cm.name)
                elif olist[0]=="Support resolved.":
                    continue
                elif olist[0]=="Hold resolved.":
                    continue
                elif olist[0]=="Hold failed.":
                    u.country.dislodged_units.append(u)
                    u.loc.unit=None
                    u.loc.dislodged=u
                elif olist[0]=="Move resolved.":
                    p=judge.get_province(olist[-2])
                    fullname=olist[-1].split
                    i=0
                    back=""
                    m=None
                    mcoast=None
                    #parse full name
                    for word in fullname:
                        if (pdata.is_province(word+back)):
                            m=judge.get_province(word+back)
                            break
                        else:
                            back+=fullname[i]
                        i+=1
                    if (pdata.is_bi_coastal(m)):
                        if fullname==back+" "+m.coasts[0]:
                            mcoast=m.coasts[0]
                        elif fullname==back+" "+m.coasts[1]:
                            mcoast=m.coasts[1]
                    u=p.unit
                    u.loc=m
                    p.unit=None
                    m.unit=u
                    u.coast=mcoast
                    u.country.unit_locations.remove(p.name)
                    u.country.unit_locations.append(m.name)
                elif olist[0]=="Retreat failed." or olist[0]=="Destroy resolved." or olist[0]=="Order missing":
                    rp=judge.get_province(olist[-1])
                    ru=cp.unit
                    rp.unit=None
                    u.country.unit_locations.remove(rp.name)
                elif olist[0]=="Build resolved.":
                    fullname=olist[-1].split
                    i=0
                    back=""
                    p=None
                    pcoast=None
                    #parse full name
                    for word in fullname:
                        if (pdata.is_province(word+back)):
                            p=judge.get_province(word+back)
                            break
                        else:
                            back+=fullname[i]
                        i+=1
                    if (pdata.is_bi_coastal(p)):
                        if fullname==back+" "+p.coasts[0]:
                            pcoast=p.coasts[0]
                        elif fullname==back+" "+p.coasts[1]:
                            pcoast=p.coasts[1]
                    u=location.Unit(olist[-2],p.country,p,pcoast)
                    p.unit=u
                    u.country.unit_locations.append(p.name)
                elif olist[0]=="Retreat resolved.":
                    rm=judge.get_province(olist[-1])
                    rp=judge.get_province(olist[-2])
                    ru=rp.dislodged
                    rp.dislodged=None
                    rm.unit=ru
                    rmcoast=None
                    if (rm.coasts!=[] and ru.type=="Fleet"):
                        border1=rm.borders[rm.coasts[0]]
                        border2=rm.borders[rm.coasts[1]]
                        if rp.name in border1:
                            rmcoast=rm.coasts[0]
                        elif rp.name in border2:
                            rmcoast=rm.coasts[1]
                    u.coast=rmcoast
                    u.country.unit_locations.remove(rp.name)
                    u.country.unit_locations.append(rm.name)
        return
    