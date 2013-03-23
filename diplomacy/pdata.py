#!/usr/bin/python

#Master Province Data#
abbrev={
    "adr":"Adriatic Sea",
    "aeg":"Aegean Sea",
    "alb":"Albania",
    "ank":"Ankara",
    "apu":"Apulia",
    "arm":"Armenia",
    "bal":"Baltic Sea",
    "bar":"Barents Sea",
    "bel":"Belgium",
    "ber":"Berlin",
    "bla":"Black Sea",
    "boh":"Bohemia",
    "bre":"Brest",
    "bud":"Budapest",
    "bul":"Bulgaria",
    "bur":"Burgundy",
    "cly":"Clyde",
    "con":"Constantinople",
    "den":"Denmark",
    "eas":"East Mediterranean Sea",
    "edi":"Edinburgh",
    "eng":"English Channel",
    "fin":"Finland",
    "gal":"Galicia",
    "gas":"Gascony",
    "gre":"Greece",
    "lyo":"Gulf of Lyons",
    "bot":"Gulf of Bothnia",
    "hel":"Heligoland Bight",
    "ion":"Ionian Sea",
    "iri":"Irish Sea",
    "kie":"Kiel",
    "lvp":"Liverpool",
    "lvn":"Livonia",
    "lon":"London",
    "mar":"Marseilles",
    "mat":"Mid Atlantic",
    "mos":"Moscow",
    "mun":"Munich",
    "nap":"Naples",
    "nat":"North Atlantic",
    "naf":"North Africa",
    "nth":"North Sea",
    "nor":"Norway",
    "nwg":"Norwegian Sea",
    "par":"Paris",
    "pic":"Picardy",
    "pie":"Piedmont",
    "por":"Portugal",
    "pru":"Prussia",
    "rom":"Rome",
    "ruh":"Ruhr",
    "rum":"Rumania",
    "ser":"Serbia",
    "sev":"Sevastopol",
    "sil":"Silesia",
    "ska":"Skagerrak",
    "smy":"Smyrna",
    "spa":"Spain",
    "stp":"Saint Petersburg",
    "swe":"Sweden",
    "syr":"Syria",
    "tri":"Trieste",
    "tun":"Tunisia",
    "tus":"Tuscany",
    "tyr":"Tyrolia",
    "tys":"Tyrhenian Sea",
    "ukr":"Ukraine",
    "ven":"Venice",
    "vie":"Vienna",
    "wal":"Wales",
    "war":"Warsaw",
    "wes":"Western Mediterranean Sea",
    "yor":"Yorkshire",
    "nc":"North Coast",
    "sc":"South Coast",
    "ec":"East Coast",
    }
borders={
    "North Africa":["Western Mediterranean Sea","Tunisia","Mid Atlantic"],
    "Tunisia":["Tyrhenian Sea","Ionian Sea","North Africa","Western Mediterranean Sea"],
    "Bohemia":["Galicia","Munich","Silesia","Tyrolia","Vienna"],
    "Budapest":["Galicia","Rumania","Serbia","Trieste","Vienna"],
    "Galicia":["Bohemia","Budapest","Vienna","Warsaw","Ukraine","Rumania","Silesia"],
    "Trieste":["Vienna","Budapest","Serbia","Albania","Adriatic Sea","Venice","Tyrolia"],
    "Tyrolia":["Bohemia","Vienna","Trieste","Venice","Munich"],
    "Vienna":["Galicia","Budapest","Trieste","Tyrolia","Bohemia"],
    "Albania":["Serbia","Greece","Ionian Sea","Adriatic Sea","Trieste"],
    "Bulgaria":{
        "Land":["Rumania","Constantinople","Greece","Serbia"],
        "East Coast":["Rumania","Black Sea","Constantinople"],
        "South Coast":["Constantinople","Aegean Sea","Greece"]},
    "Greece":["Bulgaria","Aegean Sea","Ionian Sea","Albania","Serbia"],
    "Rumania":["Ukraine","Sevastopol","Black Sea","Bulgaria","Serbia","Budapest","Galicia"],
    "Serbia":["Budapest","Rumania","Bulgaria","Greece","Albania","Trieste"],
    "Clyde":["Norwegian Sea","Edinburgh","Yorkshire","Liverpool","North Atlantic"],
    "Edinburgh":["Norwegian Sea","North Sea","Yorkshire","Liverpool","Clyde"],
    "Liverpool":["Edinburgh","Yorkshire","Wales","Irish Sea","North Atlantic"],
    "London":["Yorkshire","North Sea","English Channel","Wales"],
    "Wales":["Liverpool","Yorkshire","London","English Channel","Irish Sea"],
    "Yorkshire":["Edinburgh","North Sea","London","Wales","Liverpool","Clyde"],
    "Brest":["English Channel","Picardy","Paris","Gascony","Mid Atlantic"],
    "Burgundy":["Belgium","Ruhr","Munich","Marseilles","Gascony","Paris","Picardy"],
    "Gascony":["Brest","Paris","Burgundy","Marseilles","Spain","Mid Atlantic"],
    "Marseilles":["Burgundy","Piedmont","Gulf of Lyons","Spain","Gascony"],
    "Paris":["Picardy","Burgundy","Gascony","Brest"],
    "Picardy":["Belgium","Burgundy","Paris","Brest","English Channel"],
    "Berlin":["Baltic Sea","Prussia","Silesia","Munich","Kiel"],
    "Kiel":["Denmark","Baltic Sea","Berlin","Munich","Ruhr","Holland","Heligoland Bight"],
    "Munich":["Berlin","Silesia","Bohemia","Tyrolia","Burgundy","Ruhr","Kiel"],
    "Prussia":["Livonia","Warsaw","Silesia","Berlin","Baltic Sea"],
    "Ruhr":["Kiel","Munich","Burgundy","Belgium","Holland"],
    "Silesia":["Prussia","Warsaw","Galicia","Bohemia","Munich","Berlin"],
    "Spain":{
        "Land":["Gascony","Marseilles","Portugal"],
        "North Coast":["Mid Atlantic","Gascony","Portugal"],
        "South Coast":["Marseilles","Gulf of Lyons","Western Mediterranean","Mid Atlantic","Portugal"]},
    "Portugal":["Spain","Mid Atlantic"],
    "Apulia":["Adriatic Sea","Ionian Sea","Naples","Rome","Venice"],
    "Naples":["Apulia","Ionian Sea","Tyrhenian Sea","Rome"],
    "Piedmont":["Tyrolia","Venice","Tuscany","Gulf of Lyons","Marseilles"],
    "Rome":["Venice","Apulia","Naples","Tyrhenian Sea","Tuscany"],
    "Tuscany":["Venice","Rome","Tyrhenian Sea","Gulf of Lyons","Piedmont"],
    "Venice":["Tyrolia","Trieste","Adriatic Sea","Apulia","Rome","Tuscany","Piedmont"],
    "Belgium":["Holland","Ruhr","Burgundy","Picardy","English Channel","North Sea"],
    "Holland":["Heligoland Bight","Kiel","Ruhr","Belgium","North Sea"],
    "Finland":["Norway","Saint Petersburg","Gulf of Bothnia","Sweden"],
    "Livonia":["Saint Petersburg","Moscow","Warsaw","Prussia","Baltic Sea","Gulf of Bothnia"],
    "Moscow":["Saint Petersburg","Sevastopol","Ukraine","Warsaw","Livonia"],
    "Sevastopol":["Moscow","Armenia","Black Sea","Rumania","Ukraine"],
    "Saint Petersburg":{
        "Land":["Moscow","Livonia","Finland","Norway"],
        "North Coast":["Barents Sea","Norway"],
        "South Coast":["Finland","Livonia","Gulf of Bothnia"]},
    "Ukraine":["Moscow","Sevastopol","Rumania","Galicia","Warsaw"],
    "Warsaw":["Livonia","Moscow","Ukraine","Galicia","Silesia","Prussia"],
    "Denmark":["Skagerrak","Sweden","Baltic Sea","Kiel","Heligoland Bight","North Sea"],
    "Norway":["Barents Sea","Saint Petersburg","Finland","Sweden","Skagerrak","North Sea","Norwegian Sea"],
    "Sweden":["Finland","Gulf of Bothnia","Baltic Sea","Denmark","Skagerrak","Norway"],
    "Ankara":["Black Sea","Armenia","Smyrna","Constantinople"],
    "Armenia":["Sevastopol","Syria","Smyrna","Ankara","Black Sea"],
    "Constantinople":["Black Sea","Ankara","Smyrna","Aegean Sea","Bulgaria"],
    "Smyrna":["Ankara","Armenia","Syria","East Mediterranean","Aegean Sea","Constantinople"],
    "Syria":["Armenia","East Mediterranean","Smyrna"],
    "Aegean Sea":["Bulgaria","Constantinople","Smyrna","East Mediterranean Sea","Ionian Sea","Greece"],
    "Barents Sea":["Saint Petersburg","Norway","Norwegian Sea"],
    "English Channel":["London","Belgium","Picardy","Brest","Mid Atlantic","Irish Sea","Wales"],
    "Heligoland Bight":["Denmark","Kiel","Holland","North Sea"],
    "Irish Sea":["North Atlantic","Liverpool","Wales","English Channel","Mid Atlantic"],
    "Mid Atlantic":["North Atlantic","Irish Sea","English Channel","Brest","Gascony","Spain","Portugal","Western Mediterranean"],
    "North Atlantic":["Norwegian Sea","Clyde","Liverpool","Irish Sea","Mid Atlantic"],
    "North Sea":["Norwegian Sea","Norway","Skagerrak","Denmark","Heligoland Bight","Holland","Belgium","English Channel","London","Yorkshire","Edinburgh"],
    "Norwegian Sea":["Barents Sea","Norway","North Sea","Edinburgh","Clyde","North Atlantic"],
    "Skagerrak":["Norway","Sweden","Denmark","North Sea"],
    "Baltic Sea":["Gulf of Bothnia","Livonia","Prussia","Berlin","Kiel","Denmark","Sweden"],
    "Gulf of Bothnia":["Finland","Saint Petersburg","Livonia","Baltic Sea","Sweden"],
    "Adriatic Sea":["Trieste","Albania","Ionian Sea","Apulia","Venice"],
    "Black Sea":["Sevastopol","Armenia","Ankara","Constantinople","Bulgaria","Rumania"],
    "East Mediterranean Sea":["Smyrna","Syria","Ionian Sea","Aegean Sea"],
    "Gulf of Lyons":["Marseilles","Piedmont","Tuscany","Tyrhenian Sea","Western Mediterranean","Spain"],
    "Ionian Sea":["Albania","Greece","Aegean Sea","East Mediterranean","Tunisia","Tyrhenian Sea","Naples","Apulia","Adriatic Sea"],
    "Tyrhenian Sea":["Tuscany","Rome","Naples","Ionian Sea","Tunisia","Western Mediterranean","Gulf of Lyons"],
    "Western Mediterranean Sea":["Gulf of Lyons","Tyrhenian Sea","Tunisia","North Africa","Mid Atlantic","Spain"]
    }
water_bodies=[
    "Barents Sea",
    "English Channel",
    "Heligoland Bight",
    "Irish Sea",
    "Mid Atlantic",
    "North Atlantic",
    "Norwegian Sea",
    "Skagerrak",
    "Baltic Sea",
    "Gulf of Bothnia",
    "Adriatic Sea",
    "Black Sea",
    "East Mediterranean Sea",
    "Gulf of Lyons",
    "Ionian Sea",
    "Tyrhenian Sea",
    "Western Mediterranean Sea"
    ]
bi_coastals={
    "Bulgaria":["East Coast","South Coast"],
    "Spain":["North Coast","South Coast"],
    "Saint Petersburg":["North Coast","South Coast"]
    }
starting_scs={
    "Austria":["Budapest","Trieste","Vienna"],
    "England":["Edinburgh","Liverpool","London"],
    "France":["Brest","Marseilles","Paris"],
    "Germany":["Berlin","Kiel","Munich"],
    "Italy":["Naples","Rome","Venice"],
    "Russia":["Moscow","Saint Petersburg","Sevastopol","Warsaw"],
    "Turkey":["Ankara","Constantinople","Smyrna"]
    }
class pdata(object):
    def __init__(self):
        return
    def get_borders(self,p,coast=""):
        if coast!="":
            return borders[p][coast]
        else:
            return (borders[p])
    def is_water(self,p):
        if p in water_bodies:
            return True
        return False
    def is_bi_coastal(self,p):
        if p in bi_coastals.keys():
            return True
        return False
    def is_province(self,p):
        if p in borders.keys():
            return True
        return False
    def is_coastal(self,p):
        for b in self.get_borders(p):
            if self.is_water(b):
                return True
        return False
    def is_starting_sc(self,c,p):
        if p in starting_scs[c]:
            return True
        return False
    def de_abbrev(self,a):
        if a in abbrev.keys():
            return abbrev[a]
        else:
            return a
    