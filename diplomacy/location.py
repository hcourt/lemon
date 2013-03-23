#!/usr/bin/python

import pdata
pdb=pdata.pdata()

def error(str):
    print ("ERROR: "+str)
    return
    
class Country(object):
    def __init__(self, name, player):
        self.name=name
        self.player=player
        self.provinces=[]
        self.province_names=[]
        self.unit_locations=[]
        self.surrendered=False
        self.dislodged_units=[]
    def surrender(self):
        if (self.surrendered==False):
            self.surrendered=True
            print(self.name+" (Player "+str(player)+") has surrendered.")
        else:
            error(self.name+" (Player "+str(player)+") has already surrendered.")
        return
    def start_provinces(self):
        if (self.name=="Austria"):
            self.provinces=[
                Province("Bohemia",False,self),
                Province("Budapest",True,self,"Army"),
                Province("Galicia",False,self),
                Province("Trieste",True,self,"Fleet"),
                Province("Tyrolia",False,self),
                Province("Vienna",True,self,"Army")]
            self.unit_locations.append("Budapest")
            self.unit_locations.append("Trieste")
            self.unit_locations.append("Vienna")
        elif (self.name=="England"):
            self.provinces=[
                Province("Clyde",False,self),
                Province("Edinburgh",True,self,"Fleet"),
                Province("Liverpool",True,self,"Army"),
                Province("London",True,self,"Fleet"),
                Province("Wales",False,self),
                Province("Yorkshire",False,self)]
            self.unit_locations.append("Edinburgh")
            self.unit_locations.append("Liverpool")
            self.unit_locations.append("London")
        elif (self.name=="France"):
            self.provinces=[
                Province("Brest",True,self,"Fleet"),
                Province("Burgundy",False,self),
                Province("Gascony",False,self),
                Province("Marseilles",True,self,"Army"),
                Province("Paris",True,self,"Army"),
                Province("Picardy",False,self)]
            self.unit_locations.append("Brest")
            self.unit_locations.append("Marseilles")
            self.unit_locations.append("Paris")
        elif (self.name=="Germany"):
            self.provinces=[
                Province("Berlin",True,self,"Army"),
                Province("Kiel",True,self,"Fleet"),
                Province("Munich",True,self,"Army"),
                Province("Prussia",False,self),
                Province("Ruhr",False,self),
                Province("Silesia",False,self)]
            self.unit_locations.append("Berlin")
            self.unit_locations.append("Kiel")
            self.unit_locations.append("Munich")
        elif (self.name=="Italy"):
            self.provinces=[
                Province("Apulia",False,self),
                Province("Naples",True,self,"Fleet"),
                Province("Piedmont",False,self),
                Province("Rome",True,self,"Army"),
                Province("Tuscany",False,self),
                Province("Venice",True,self,"Army")]
            self.unit_locations.append("Naples")
            self.unit_locations.append("Rome")
            self.unit_locations.append("Venice")
        elif (self.name=="Russia"):
            self.provinces=[
                Province("Finland",False,self),
                Province("Livonia",False,self),
                Province("Moscow",True,self,"Army"),
                Province("Saint Petersburg",True,self,"Fleet","South Coast",["North Coast","South Coast"]),
                Province("Sevastopol",True,self,"Fleet"),
                Province("Ukraine",False,self),
                Province("Warsaw",True,self,"Army")]
            self.unit_locations.append("Moscow")
            self.unit_locations.append("Saint Petersburg")
            self.unit_locations.append("Sevastopol")
            self.unit_locations.append("Warsaw")
        elif (self.name=="Turkey"):
            self.provinces=[
                Province("Ankara",True,self,"Fleet"),
                Province("Armenia",False,self),
                Province("Constantinople",True,self,"Army"),
                Province("Smyrna",True,self,"Army"),
                Province("Syria",False,self)]
            self.unit_locations.append("Ankara")
            self.unit_locations.append("Constantinople")
            self.unit_locations.append("Smyrna")
        elif (self.name=="Neutral"):
            self.provinces=[
                Province("Norway",True),
                Province("Sweden",True),
                Province("Denmark",True),
                Province("Holland",True),
                Province("Belgium",True),
                Province("Spain",True,None,None,None,["North Coast","South Coast"]),
                Province("Portugal",True),
                Province("North Africa",False),
                Province("Tunisia",True),
                Province("Rumania",True),
                Province("Serbia",True),
                Province("Albania",False),
                Province("Greece",True),
                Province("Bulgaria",True,None,None,None,["East Coast","South Coast"]),
                Province("Barents Sea",False),
                Province("Norwegian Sea",False),
                Province("North Atlantic",False),
                Province("North Sea",False),
                Province("Skagerrak",False),
                Province("Heligoland Bight",False),
                Province("Baltic Sea",False),
                Province("Gulf of Bothnia",False),
                Province("English Channel",False),
                Province("Irish Sea",False),
                Province("Mid Atlantic",False),
                Province("Gulf of Lyons",False),
                Province("Western Mediterranean Sea",False),
                Province("Tyrhenian Sea",False),
                Province("Adriatic Sea",False),
                Province("Ionian Sea",False),
                Province("Aegean Sea",False),
                Province("Black Sea",False),
                Province("East Mediterranean Sea",False)]
        else:
            error("Unknown country name.  Cannot construct provinces.")
            return
        for p in self.provinces:
            self.province_names.append(p.name)
        
class Province(object):
    def __init__(self, name, sc, country=None, u=None, ucoast=None,coasts=None):
        self.name=name
        self.country=country
        self.is_sc=sc #is supply center?
        if (u is not None):
            self.unit=Unit(u,country,self,ucoast)
        else:
            self.Unit=None
        self.coasts=coasts
        borders=pdb.get_borders(name)
        if (coasts is None):
            borders.sort()
        else:
            for b in borders.values():
                b.sort()
        self.borders=borders
        if coasts is None:
            self.expects={
                "Move":[],
                "Support":[],
                "Convoy":[],
                "Hold":[]
                }
        else:
            self.expects={
                "Move":[],
                ("Move "+coasts[0]):[],
                ("Move "+coasts[1]):[],
                "Support":[],
                "Convoy":[],
                "Hold":[]
                }
    def full_name(self,coast):
        if coast is None:
            return self.name
        else:
            return self.name+" "+coast
class Unit(object):
    def __init__(self, type, country, loc, coast=None):
        self.type=type
        self.country=country
        self.loc=loc
        self.coast=coast
        #temporary stats, used by adjudicator
        self.support=0
        self.convoyed=True
        self.intended_coast=None
        self.intended_convoy=None
        self.intended_support=None
        self.dislodged=None
