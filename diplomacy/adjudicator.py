#!/usr/bin/python
import pdata
pdata=pdata.pdata()

def a_print(str):
    print("ADJUDICATOR: "+str)
    return
class Adjudicator (object):
    def __init__(self):
        self.countries=None
        self.retreat_units=[] #a list of units to retreat
        self.retreat_players=[] #a list of players who must retreat
        self.build_surplus=0 #the surplus or debt of supply centers
        self.build_players=[] #a list of players who must resolve their surplus or deficit
        self.conflict_provinces=[]
        return
    def last(self,list,reverse_index=1):
        if (len(list)>=reverse_index):
            return list[-reverse_index]
        else:
            return None
    def get_province(self,name):
        for p in self.get_all_provinces():
            if (p.name==name):
                return p
    def get_all_provinces(self):
        plist=[]
        for c in self.countries:
            for p in c.provinces:
                plist.append(p)
        return plist
    def resolve_moves(self,units):
        supports=[]
        for u in units:
            supports.append(u.support + 1)
        supports.sort()
        if (self.last(supports)==self.last(supports,2)):
            return None
        else:
            for u in units:
                if u.support+1==self.last(supports):
                    return u
    def move(self,countries):
        self.countries=countries
        player_orders=[None,None,None,None,None,None,None]
        total_orders=[]
        for p in range(1,8):
            o=self.load_orders(p,"move")
            player_orders[p-1]=o
            total_orders.append(o)
        master_orders=self.process_orders(player_orders,total_orders,"move")
        return master_orders
    def retreat(self,countries,units):
        self.countries=countries
        self.retreat_units=units
        player_orders=[None,None,None,None,None,None,None]
        total_orders=[]
        for p in self.retreat_players:
            o=self.load_orders(p,"retreat")
            player_orders[p-1]=o
            total_orders.append(o)
        self.process_orders(player_orders,total_orders,"retreat")
        return
    def build(self,countries,surplus):
        self.countries=countries
        self.build_surplus=surplus
        player_orders=[None,None,None,None,None,None,None]
        total_orders=[]
        for p in build_players:
            o=self.load_orders(p,"build")
            player_orders[p-1]=o
            total_orders.append(o)
        self.process_orders(player_orders,total_orders,"build")
        return
    #loads all player#.txt files and parses each line into orders
    def load_orders(self,player,mode):
        orders=[]
        f=open("player"+str(player)+".txt",'r')
        #move orders
        if(mode=="move"):
            for line in iter(f.readline, b''):
                linelist=line.split()
                linemode=""
                unittype=""
                unitprovince=""
                unitcoast=""
                moveprovince=""
                movecoast=""
                #if linemode=support, use these for supported order:
                support_mode=""
                support_unittype=""
                support_unitprovince=""
                support_unitcoast=""
                support_moveprovince=""
                support_movecoast=""
                valid=True
                for n in range(0, len(linelist)):
                    word=linelist[n]
                    if (n==0): #Unittype
                        if (word=="Army" or word=="Fleet"):
                            unittype=word
                        else:
                            valid=False
                            break
                    elif (n==1): #Unitprovince
                        word=pdata.de_abbrev(word)
                        if (word in self.countries[player-1].unit_locations): #ensure the given province is the location of a unit
                            unitprovince=word
                        else:
                            valid=False
                            break
                    elif (n==2): #Support or Convoy or Hold, or Unitcoast or Moveprovince
                        if (word=="Hold" or word=="Support" or word=="Convoy"):
                            linemode=word
                        else:
                            word=pdata.de_abbrev(word)
                            if (pdata.is_province(word)):
                                moveprovince=word
                                linemode="Move"
                            elif (pdata.is_bi_coastal(unitprovince)):
                                p=self.get_province(unitprovince)
                                if word in p.coasts:
                                    unitcoast=word
                            else:
                                valid=False
                                break
                    elif (n==3): #Hold or Support or Moveprovince or Movecoast or Support_Unittype
                        if (word=="Support" or word=="Hold"):
                            linemode=word
                        elif (unitcoast is not None):
                            word=pdata.de_abbrev(word)
                            if (pdata.is_province(word)):#ensure the given province is a province
                                moveprovince=word
                                linemode="Move"
                        elif (pdata.is_bi_coastal(moveprovince)):
                            
                            p=self.get_province(moveprovince)
                            if word in p.coasts:
                                movecoast=word
                        elif ((linemode=="Support" or linemode=="Convoy") and (word=="Army" or word=="Fleet")):
                            support_unittype=word
                        else:
                            valid=False
                            break
                        
                        
                    elif (n==4): #Support_Unittype or Support_Unitprovince
                        if (linemode=="Support" and unitcoast is not None):
                            if (word=="Army" or word=="Fleet"):
                                support_unittype=word
                            else:
                                valid=False
                                break
                        elif (linemode=="Support" or linemode=="Convoy" and unitcoast is None):
                            word=pdata.de_abbrev(word)
                            if (word in countries[player-1].unit_locations): #ensure the given province is the location of a unit
                                support_unitprovince=word
                            else:
                                valid=False
                                break
                    elif (n==5): #Hold or Support_Unitprovince or Support_Moveprovince or Support_Unitcoast
                        if (linemode=="Support" and word=="Hold"):
                            support_mode=word
                        elif (linemode=="Support" or linemode=="Convoy"):
                            word=pdata.de_abbrev(word)
                            if (word in countries[player-1].unit_locations and unitcoast is not None): #ensure the given province is the location of a unit
                                support_unitprovince=word
                            elif (pdata.is_bi_coastal(support_unitprovince)):
                                p=self.get_province(support_unitprovince)
                                if word in p.coasts:
                                    support_unitcoast=word
                            elif (pdata.is_province(word)):#ensure the given province is a province
                                support_moveprovince=word
                                support_mode="Move"
                    elif (n==6): #Hold or Support_Moveprovince or Support_Movecoast
                        if (linemode=="Support"):
                            if (word=="Hold"):
                                support_mode=word
                            else:
                                word=pdata.de_abbrev(word)
                                if (pdata.is_bi_coastal(    support_moveprovince)):
                                    p=self.get_province(support_moveprovince)
                                    if word in p.coasts:
                                        support_movecoast=word
                                elif (pdata.is_province(word)):
                                    support_moveprovince=word
                                    support_mode="Move"
                #Order validity checks
                if (valid==True):
                    for p in self.get_all_provinces():
                        if (unitprovince==p.name):
                            if (p.unit.type==unittype and p.unit.country.name==self.countries[player-1].name):
                                if (linemode=="Hold"):
                                    if (unittype=="Fleet" and (pdata.is_coastal(unitprovince) or pdata.is_water(unitprovince))):
                                        orders.append(["Fleet",unitprovince,"Hold"])
                                    elif (not pdata.is_water(unitprovince)):
                                        orders.append(["Army",unitprovince,"Hold"])
                                elif (linemode=="Move"):
                                    m=self.get_province(moveprovince)
                                    if (unittype=="Fleet"):
                                        if (unitcoast!="" and movecoast=="" and moveprovince in pdata.get_borders(unitprovince,unitcoast)):
                                            orders.append(["Fleet",unitprovince,unitcoast,moveprovince])
                                        elif (unitcoast=="" and movecoast=="" and unitprovince in pdata.get_borders(moveprovince,movecoast)):
                                            orders.append(["Fleet",unitprovince,moveprovince,movecoast])
                                        elif (unitcoast=="" and movecoast==""):
                                            orders.append(["Fleet",unitprovince,moveprovince])
                                        elif (pdata.is_water(m.name) or pdata.is_coastal(m.name)):
                                            orders.append(["Fleet",unitprovince,moveprovince])
                                    elif (unittype=="Army"):
                                        if (not pdata.is_water(m.name)):
                                            orders.append(["Army",unitprovince,moveprovince])
                                elif (linemode=="Support"):
                                    if (support_mode=="Hold"):
                                        m=self.get_province(support_unitprovince)
                                        #must support a bordering province the unit can move into
                                        if (m.name in pdata.get_borders(p.name)):
                                            if (unittype=="Fleet"):
                                                if (pdata.is_water(m.name) or pdata.is_coastal(m.name)):
                                                    orders.append(["Fleet",unitprovince,"Support",support_unittype,support_unitprovince,"Hold"])
                                                    break
                                            elif (unittype=="Army"):
                                                if (not pdata.is_water(m.name)):
                                                    orders.append(["Army",unitprovince,"Support",support_unittype,support_unitprovince,"Hold"])
                                                    break
                                    elif (support_mode=="Move"):
                                        m=self.get_province(support_moveprovince)
                                        #must support a move into a bordering province the unit can move into
                                        if (m.name==support_moveprovince and m.name in pdata.get_borders(p.name)):
                                            if (unittype=="Fleet"):
                                                if (pdata.is_water(m.name) or pdata.is_coastal(m.name)):
                                                    orders.append(["Fleet",unitprovince,"Support",support_unittype,support_unitprovince,support_moveprovince])
                                                    break
                                            elif (unittype=="Army"):
                                                if (not pdata.is_water(m.name)):
                                                    orders.append(["Army",unitprovince,"Support",upport_unittype,support_unitprovince,support_moveprovince])
                                                    break
                                elif (linemode=="Convoy"):
                                    if (unittype=="Fleet" and support_unittype=="Army" and pdata.is_water(unitprovince)):
                                        orders.append(["Fleet",unitprovince,"Convoy Army",support_unitprovince,support_moveprovince])
        #retreat orders            
        elif(mode=="retreat"):
            for line in iter(f.readline, b''):
                linelist=line.split()
                linemode=""
                unittype=""
                unitprovince=""
                moveprovince=""
                valid=True
                for n in range(0, len(linelist)):
                    word=linelist[n]
                    if (n==0): #Retreat
                        if (word=="Retreat"):
                            linemode=word
                        else:
                            linemode=="Destroy" #Retreat orders turn into Destroy orders if not formatted correctly
                    elif (n==1): #Unittype
                        if (word=="Army" or word=="Fleet"):
                            unittype=word
                        else:
                            valid=False
                            break
                    elif (n==2): #Unitprovince
                        word=pdata.de_abbrev(word)
                        if (word in countries[player-1].unit_locations): #ensure the given province is the location of a unit
                            unitprovince=word
                        else:
                            valid=False
                            break
                    elif (n==3): #Unitcoast or Moveprovince
                        word=pdata.de_abbrev(word)
                        if (pdata.is_province(word)):#ensure the given province is a province
                            moveprovince=word
                        elif (pdata.is_bi_coastal(unitprovince)):
                            p=self.get_province(unitprovince)
                            if word in p.coasts:
                                unitcoast=word
                        else:
                            valid=False
                            break
                    elif (n==4): #Moveprovince or Movecoast
                        word=pdata.de_abbrev(word)
                        if (unitcoast is not None and pdata.is_province(word)):
                            moveprovince=word
                        elif(unitcoast is None and moveprovince is not None):
                            p=self.get_province(moveprovince)
                            if word in p.coasts:
                                movecoast=word
                        else:
                            valid=False
                            break
                #Order validity checks
                if (valid==True):
                    for p in countries[player-1].provinces:
                        if (unitprovince==p.name):
                            if (p.unit.type==unittype and p.unit.country==countries[player-1].name):
                                if (linemode=="Retreat"):
                                    m=self.get_province(moveprovince)
                                    #must move into a bordering province
                                    if (unittype=="Fleet"):
                                        if (pdata.is_water(m.name) or pdata.is_coastal(m.name)):
                                            if (unitcoast is not None and movecoast is None and moveprovince in pdata.get_borders(unitprovince)[unitcoast]):
                                                orders.append(["Retreat", "Fleet",unitprovince,unitcoast,moveprovince])
                                            elif (unitcoast is None and movecoast is None and unitprovince in pdata.get_borders(moveprovince)[movecoast]):
                                                orders.append(["Retreat", "Fleet",unitprovince,moveprovince,movecoast])
                                            elif (unitcoast is None and movecoast is None):
                                                orders.append(["Retreat", "Fleet",unitprovince,moveprovince])
                                    elif (unittype=="Army"):
                                        if ((pdata.is_coastal(p.name) and m.name in pdata.get_borders(p.name)["Land"]) or m.name in pdata.get_borders(p.name)):
                                            if (not pdata.is_water(m.name)):
                                                orders.append("Retreat", "Army",unitprovince,moveprovince)
                                elif (linemode=="Destroy"):
                                    orders.append("Destroy",unittype,unitprovince)
                            break
        #build orders            
        elif(mode=="build"):
            for line in iter(f.readline, b''):
                wordlist=line.split()
                linemode=""
                unittype=""
                unitprovince=""
                unitcoast=""
                valid=True
                for n in range(0, len(wordlist)):
                    word=wordlist[n]
                    if (n==0):
                        if (word=="Build" or word=="Destroy"):
                            linemode=word
                        else:
                            valid=False
                            break #Build orders are ignored if not formatted correctly
                    elif (n==1):
                        if (word=="Army" or word=="Fleet"):
                            unittype=word
                        else:
                            valid=False
                            break
                    elif (n==2):
                        word=pdata.de_abbrev(word)
                        if (word in countries[player-1].province_names):
                            unitprovince=word
                        else:
                            valid=False
                            break
                    elif (n==3):
                        word=pdata.de_abbrev(word)
                        p=self.get_province(unitprovince)
                        if word in p.coasts:
                            unitcoast=word
                #Order validity checks
                if (valid==True):
                    for p in countries[player-1].province_names:
                        if (unitprovince==p.name):
                            if (linemode=="Build"):
                                if (p.is_sc and p.unit==None and pdata.is_starting_sc(countries[player-1],p.name)): #Must be built in an unoccupied home supply center
                                    if (unittype=="Fleet"):#Fleets must be built on coastal supply centers
                                        if (pdata.is_coastal(p.name)):
                                            if (unitcoast is not None):
                                                orders.append(["Build", "Fleet",unitprovince,unitcoast])
                                            else:
                                                orders.append(["Build", "Fleet",unitprovince])
                                    else:
                                        orders.append("Build", "Army",unitprovince)
                            elif (linemode=="Destroy"):
                                if (p.unit.type==unittype and p.unit.country==countries[player-1].name):
                                    orders.append("Destroy",unittype,unitprovince)
                            break
        f.close()
        return orders
    #process orders and assign expects
    def process_orders(self,player_orders,total_orders,mode):
        master_orders={1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
        if (mode=="move"):
            player=1
            #initial pass.  Ignore convoy and support orders.
            for orders in player_orders:
                for olist in orders:
                    if (len(olist)>5 and (olist[2]=="Support" or olist[2]=="Convoy" or olist[3]=="Support")):
                        continue
                    #hold expects
                    elif (olist[2]=="Hold" or (len(olist)==4 and olist[3]=="Hold")):
                        p=self.get_province(olist[1])
                        p.unit.support=0
                        p.expects["Hold"].append(p.unit)
                        if (p not in self.conflict_provinces):
                            self.conflict_provinces.append(p)
                    #move expects
                    else:
                        p=self.get_province(olist[1])
                        p.unit.support=0
                        if (p.coasts is not None and p.unit.type=="Fleet"):
                            m=self.get_province(olist[3])
                            m.expects["Move"].append(p.unit)
                        else:
                            m=self.get_province(olist[2])
                            if (m.coasts is not None and p.unit.type=="Fleet"):
                                m.expects["Move "+olist[3]].append(p.unit)
                            else:
                                m.expects["Move"].append(p.unit)
                        if (m not in self.conflict_provinces):
                            self.conflict_provinces.append(m)
                player+=1
            player=1
            #second pass.  Deal with convoys and supports here.
            for orders in player_orders:
                for olist in orders:
                    #support expects
                    if (olist[2]=="Support"):
                        print("A")
                        sp=self.get_province(olist[4])
                        su=sp.unit
                        p=self.get_province(olist[1])
                        if (p not in conflict_provinces):
                            conflict_provinces.append(p)
                        #support hold expects
                        if (olist[5]=="Hold" or olist[6]=="Hold"):
                            if su in sp.expects["Hold"]:
                                su.support+=1
                                p.unit.intended_support="Hold"
                                p.expects["Support"].append(su) #support expects are contained in the supporting unit's province and point to the supported unit
                            else: #invalid
                                p.expects["Hold"].append(p.unit)
                        #support move expects
                        else:
                            if (sp.coasts is not None):
                                sm=self.get_province(olist[6])
                                if (su in sm.expects["Move"]):
                                    p.unit.intended_support="Move "+sm.name
                                    su.support+=1
                                    p.expects["Support"].append(su)
                            else:
                                sm=self.get_province(olist[5])
                                if (olist[6] is not None and su in sm.expects["Move "+olist[6]]):
                                    p.unit.intended_support="Move "+sm.name+" "+olist[6]
                                    su.support+=1
                                    p.expects["Support"].append(su)
                                elif(su in sm.expects["Move"]):
                                    p.unit.intended_support="Move "+sm.name
                                    su.support+=1
                                    p.expects["Support"].append(su)
                                else: #invalid
                                    p.expects["Hold"].append(p.unit)
                    #unit is a Fleet on a bi-coastal province
                    elif (len(olist)>5 and olist[3]=="Support"):
                        print("B")
                        sp=self.get_province(olist[5])
                        su=sp.unit
                        p=self.get_province(olist[1])
                        if (p not in conflict_provinces):
                            conflict_provinces.append(p)
                        #support hold expects
                        if (olist[6]=="Hold"):
                            if (su in sp.expects["Hold"]):
                                p.unit.intended_support="Hold"
                                su.support+=1
                                p.expects["Support"].append(su)
                            else:
                                p.expects["Hold"].append(p.unit)
                        else:
                            sm=self.get_province(olist[6])
                            if (sm.expects["Move"].append(su)):
                                p.unit.intended_support="Move "+sm.name
                                su.support+=1
                                p.expects["Support"].append(su)
                            else: #invalid
                                p.expects["Hold"].append(p.unit)
                    elif (olist[2]=="Convoy"):
                        print("C")
                        p=self.get_province(olist[1])
                        cp=self.get_province(olist[4])
                        cm=self.get_province(olist[5])
                        if (p not in conflict_provinces):
                            conflict_provinces.append(p)
                        if (cp.unit in cm.expects["Move"]):
                            p.expects["Convoy"].append(cp.unit) #convoy expects are contained in the convoying unit's province and point to the convoyed unit
                            cp.unit.intended_convoy=cm.name
                        else: #invalid
                            p.expects["Hold"].append(p.unit)                    
                        
                player+=1
            #Resolve all expects.
            self.resolve_move_expects(master_orders,"Support")
            self.resolve_move_expects(master_orders,"Convoy")
            self.resolve_move_expects(master_orders,"Move")
            self.resolve_move_expects(master_orders,"Hold")
            self.resolve_move_expects(master_orders,"Hold")
            self.resolve_move_expects(master_orders,"Finish")
        elif (mode=="retreat"):
            player=1
            retreat_provinces=[]
            for orders in player_orders:
                for olist in orders:
                    u=self.get_province(olist[2]).unit
                    if (u in self.retreat_units): #unit must be in list of units to retreat
                        if olist[0]=="Retreat":
                            m=self.get_province(olist[3])
                            retreat_provinces.append(m)
                            if (m.unit==None and m.expects["Retreat"]==None):
                                m.expects["Retreat"]=u
                            else: #both units bounce and are destroyed
                                u2=m.expects["Retreat"]
                                master_orders[player].append(["Retreat failed.","Destroy",u.type,u.loc.name])
                                if (m.expects["Retreat"]!="placeholder"): #avoid overlapping orders if more than two attempt to retreat into the province
                                    master_orders[u2.country.player].append(["Retreat failed.","Destroy ",u2.type,u2.loc])
                                m.expects["Retreat"]="placeholder"
                        elif olist[0]=="Destroy":
                            master_orders[player].append(["Destroy resolved.","Destroy",u.type,u.loc.name])
                        self.retreat_units.remove(u)
                player+=1
                #remove u from retreat_units
                #send master_order on success
            for p in retreat_provinces:
                if p.expects["Retreat"]!="" and p.expects["Retreat"]!="placeholder":
                    u=p.expects["Retreat"]
                    master_orders[player].append(["Retreat resolved.","Retreat",u.type,u.loc.name,p.name])
                    self.retreat_units.remove(u)
            for u in self.retreat_units:
                master_orders[player-1].append(["Order missing.","Destroy",u.type,u.loc.name])
        elif (mode=="build"):
            player=1
            for orders in player_orders:
                for olist in orders:
                    coast=None
                    p=self.get_province(olist[2])
                    if (olist[3] is not None):
                        coast=olist[3]
                    if (build_surplus>0 and olist[0]=="Build"):
                        master_orders[player].append(["Build resolved.","Build",olist[1],p.full_name(coast)])
                        build_surplus-=1
                    elif (build_surplus<0 and olist[0]=="Destroy"):
                        master_orders[player].append(["Destroy resolved.","Destroy",olist[1],p.name])
                        build_surplus+=1
                if (build_surplus<0):
                    for p in countries[player].unit_locations:
                        p=self.get_province(p)
                        if (build_surplus==0):
                            break
                        if (p.unit is not None):
                            master_orders[player].append(["Order missing.","Destroy",p.unit.type,p.name])
                            build_surplus+=1
                player+=1
        return master_orders
    #resolve all move expects in the given mode
    def resolve_move_expects(self,master_orders,mode):
        for p in self.conflict_provinces:
            elist=p.expects
            h_unit=self.last(elist["Hold"]) #should theoretically be only one Hold unit, so grabs the "last" one
            s_unit=self.last(elist["Support"]) #also should only be supporting one unit if any
            c_unit=self.last(elist["Convoy"]) #also can only convoy one unit
            m_units=elist["Move"] #may be multiple units moving in
            m_c1_units=[]
            m_c2_units=[]
            all_ms=m_units+m_c1_units+m_c2_units
            if (p.coasts is not None):
                m_c1_units=elist["Move "+p.coasts[0]]
                for u in m_c1_units:
                    u.intended_coast(p.coasts[0])
                m_c2_units=elist["Move "+p.coasts[1]]
                for u in m_c2_units:
                    u.intended_coast(p.coasts[1])
                
            if (c_unit is not None and mode=="Convoy"): #Convoys
                if (self.resolve_moves(m_units) is not None):
                    h_unit=p.unit
                    a_print("Convoy cut in "+p.name+".")
                    c_unit.convoyed=-1 #convoy was cut
                else:
                    a_print("Convoy through "+p.name+" resolved.")
                    master_orders[p.country.player].append(["Convoy resolved.","Fleet",p.name,"Convoy",c_unit.type,c_unit.loc.name,c_unit.intended_convoy])
                    c_unit.convoyed=1 #convoy was successful
            if (s_unit is not None and mode=="Support"): #Supports
                u=self.resolve_moves(all_ms)
                if (u is not None and u.convoyed>-1):
                    h_unit=p.unit
                    a_print("Support in "+p.name+" cut.")
                    s_unit.support-=1
                else:
                    a_print("Support from "+p.name+" resolved.")
                    if (p.unit.intended_support=="Hold"):
                        master_orders[p.country.player].append(["Support resolved.",p.unit.type,p.name,"Support",s_unit.type,s_unit.loc.name,"Hold"])
                    else:
                        master_orders[p.country.player].append(["Support resolved.",p.unit.type,p.name,"Support",s_unit.type,s_unit.loc.full_name(s_unit.intended_coast)])
            if (len(all_ms)>1 and mode=="Move"): #Moves conflicting with moves
                lead_u=self.resolve_moves(all_ms)
                if (lead_u != None):
                    a_print("Move from "+lead_u.loc.name+" into "+p.name+" was not bounced by other moves.")
                for u in all_ms:
                    if (lead_u is None or u!=lead_u):
                        a_print("Move from "+u.loc.name+" into "+p.name+" bounced.")
                        u.loc.expects["Hold"].append(u)
                        u.support=0
                        if (u in m_units):
                            p.expects["Move"].remove(u)
                        elif (u in m_c1_units):
                            p.expects["Move "+p.coasts[0]].remove(u)
                        elif (u in m_c2_units):
                            p.expects["Move "+p.coasts[1]].remove(u)
            if (h_unit is not None and mode=="Hold"):
                lead_u=self.resolve_moves(m_units+m_c1_units+m_c2_units)
                if (lead_u is not None):
                    if (h_unit.support+1>=lead_u.support+1):
                        a_print ("Move from "+lead_u.loc.name+" into "+p.name+" bounced.")
                        lead_u.loc.expects["Hold"].append(lead_u)
                        lead_u.support=0
                        master_orders[h_unit.country.player].append(["Hold resolved.",h_unit.type,p.name,"Hold"])
                        if (lead_u.loc in m_units):
                            p.expects["Move"].remove(lead_u)
                        elif (lead_u in m_c1_units):
                            p.expects["Move "+p.coasts[0]].remove(lead_u)
                        elif (lead_u in m_c2_units):
                            p.expects["Move "+p.coasts[1]].remove(lead_u)
                    else:
                        a_print ("Unit in "+p.name+" dislodged by move from "+lead_u.loc+".")
                        master_orders[h_unit.country.player].append(["Hold failed.",h_unit.type,p.name,"Dislodged"])
                        master_orders[lead_u.country.player].append(["Move resolved.",lead_u.type,lead_u.loc.name,p.full_name(lead_u.intended_coast)])
            else:
                if(h_unit is None and len(m_units)==1 and mode=="Finish"):
                    u=self.last(m_units)
                    master_orders[u.country.player].append(["Move","resolved.",u.type,u.loc.name,p.full_name(u.intended_coast)])
        return master_orders
            