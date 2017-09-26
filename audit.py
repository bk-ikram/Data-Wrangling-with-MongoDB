# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 15:09:13 2017

@author: IKRAM
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import json
import codecs



FILENAME="doha_qatar.osm"

problem_words=["school","district","compound","office","schule","mall","mart","center","parking",
               "clinic","station","kindergarten","centre","complex","lounge","restaurant","grocery",
               "supermarket","cafeteria","group","village","villa","villas","hotel","nursery"]
test_string="Rohingya madrasa"
pattern = re.compile('|'.join(r'\b{}\b'.format(word) for word in problem_words))
alt_street_types=["avenue","av","ave","av.","ave.","boulevard","bvd","bvd.","way"]
st_pattern = re.compile('|'.join(r'\b{}\b'.format(word) for word in alt_street_types))

def sorted_dict_by_val(input_dict):
    return sorted(input_dict.items(), key = lambda x: x[1], reverse=True)

def get_street_names(filename):
    names=[]
    for event,elem in ET.iterparse(filename):
        if elem.tag =="way":
            for k in elem:
                if k.get("k")=="name":
                    names.append(k.get("v"))
    return names

def check_problem_streets(names):
    problems=[]
    for street in names:
        if (pattern.search(street.lower()) != None) and ("street" not in street.lower()):
            problems.append(street)
    return problems

def check_alt_streets(names):
    alt_street=[]
    for street in names:
        if (st_pattern.search(street.lower()) != None):
            alt_street.append(street)
    return alt_street

def audit_nodes(filename,key):
    key_values=defaultdict(int)
    for event,elem in ET.iterparse(filename):
        if elem.tag=="node":
            for k in elem:
                if k.get("k")==key:
                    key_values[k.get("v")]+=1
    return sorted_dict_by_val(key_values)

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def process_element(elem):
    if elem.tag=="node" or elem.tag=="way":
        entry={}
        entry["id"]=elem.get("id")
        entry["tag_type"]=elem.tag
        entry["visible"]=elem.get("visible")
        entry["created"]={}
        for doc in CREATED:
            entry["created"][doc]=elem.get(doc)
        if elem.get("lat") and elem.get("lon"):
            position=[float(elem.get("lat")),float(elem.get("lon"))]
            if position:
                entry["pos"]=position
        for k in elem.iter("tag"):
            #ignore false streets
            if elem.tag=="way":
                if k.get("k")=="name":
                    street=k.get("v")
                    if ((pattern.search(street.lower()) == None) and (st_pattern.search(street.lower()) != None)):
                        return
            if ":" not in k.get("k"):
                entry[k.get("k")]=k.get("v")
            else:
                key_parts=k.get("k").split(":")
                if len(key_parts)==2:
                    entry[key_parts[0]]={}
                    entry[key_parts[0]][key_parts[1]]=k.get("v")
                else:
                    entry[key_parts[0]]={}
                    entry[key_parts[0]][key_parts[1]]={}
                    entry[key_parts[0]][key_parts[1]][key_parts[2]]=k.get("v")
                    if elem.tag=="way":
                        references=[]
                        for nd in elem.iter("nd"):
                            references.append(nd.get("ref"))
                        if references:
                            entry["node_ref"]=references
        if (entry.has_key("name")) and (type(entry.has_key("name"))==list) and (entry["name"].has_key("en")):
            engname=entry["name"]["en"]
            entry["othernames"]=entry["name"]
            entry["name"]=engname
        if (entry.has_key("addr") and entry["addr"].has_key("city")):
            entry["addr"]["city"]="Doha"
        return entry

def process_map(filename):
    data=[]
    outfile = "{0}.json".format(filename)
    with codecs.open(outfile, "w") as fo:
        for _, element in ET.iterparse(filename):
            el = process_element(element)
            if el:
                data.append(el)
                fo.write(json.dumps(el) + "\n")
    print "done"
    print len(data)
    
def test():
    #streets=get_street_names(FILENAME)
    #names=get_street_names(FILENAME)
    #print names
    #problems=check_problem_streets(names)
    #print len(problems)
    #alt_streets=check_alt_streets(names)
    #print alt_streets[1:50]
    #print len(alt_streets)
    #int alt_streets
    #print audit_nodes(FILENAME,"addr:city")
    #print len(problems)
    #print problems
    #process_map(FILENAME)
    pass

if __name__=="__main__":
    test()