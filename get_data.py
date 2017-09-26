# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 18:34:19 2017

@author: IKRAM
"""
import xml.etree.cElementTree as ET
from collections import defaultdict

FILENAME="doha_qatar.osm"

def sorted_dict_by_val(input_dict):
    return sorted(input_dict.items(), key = lambda x: x[1], reverse=True)

def get_tag_types(filename):
    tot_tag_count=0
    tag_count=defaultdict(int)
    for event,elem in ET.iterparse(filename):
        tot_tag_count+=1
        tag_count[elem.tag]+=1
    print "There is a total of {} tags in the Doha osm file".format(tot_tag_count)
    print "The breakdown of those tags is:-"
    return sorted_dict_by_val(tag_count)

def iter_get_tag_types(filename):
    tag_count=defaultdict(int)
    tot_tag_count=0
    for event,elem in ET.iterparse(filename):
        tag_count[elem.tag]+=1
        tot_tag_count+=1
    print "There is a total of {} tags (parent and child) in the Doha osm file".format(tot_tag_count)
    print "The breakdown of those tags is:"
    return sorted_dict_by_val(tag_count)
    
def elem_tag_types(filename,type_elem):
    tag_types=defaultdict(int)
    
    for event,elem in ET.iterparse(filename):
        if elem.tag==type_elem:
            for k in elem:
                tag_types[k.get("k")]+=1
    return sorted_dict_by_val(tag_types)

#This function prints elements containing a given tag key for inspection.
def inspect_by_tag(filename,type_elem,tag):
    elements_interest=[]
    for event,elem in ET.iterparse(filename):
        for k in elem:
            if k.get("k")==tag:
                    elements_interest.append(elem)
    return elements_interest

def disp_complete_elem(elements,max_disp=3):
    for i,elem in enumerate(elements):
        if i>=max_disp:
            break
        print"Inspecting Element {}:".format(i)
        print elem.items()
        print "Tags in this element:"
        for k in elem:
            print k.items()
        
def created_by_users(elements):
    elements=inspect_by_tag(FILENAME,"node","created_by")
    users={}
    for point in elements:
        user=point.get("user")
        for k in point:
            if k.get("k")=="created_by":
                contrib=k.get("v")
                users[user]=contrib
    output=sorted_dict_by_val(users)
    return output

def test():
    #root=read_osm(FILENAME)
    #get_tag_types(FILENAME)
    #show_sample_elements(root,"node",5)
    #iter_get_tag_types(FILENAME)
    #elem_tag_types(FILENAME,"node")
    pass
    #print len(elements)
    #disp_complete_elem(elements)
    
    

if __name__=="__main__":
    test()