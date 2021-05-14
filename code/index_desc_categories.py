#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 13:01:50 2021

@author: cbadenes
"""

import networkx as nx
import obonet
import pysolr
import re

# Read the taxrank ontology
url = '/Users/cbadenes/Dropbox/Trabajo/Carlos/OEG/Projects/MESINESP/data/DeCS2020.obo'
graph = obonet.read_obo(url)

print("reading graph from obo file..")
print(nx.info(graph))


def get_name(id):
    return  re.search("\"(.*)\"", id).group(1)

    
nodes = list(graph.nodes(data=True))
root_node = nodes[0][0]

print("build hierarchy..")
hierarchy = {}
counter = 0
pending_nodes = []
for node in nodes:
    id = get_name(node[0])
    deep = nx.shortest_path_length(graph, source=node[0], target=root_node)
    name = get_name(node[1]['name'])
    definition = ""
    if 'def' in node[1]:
        definition = get_name(node[1]['def'])
    synonyms = []
    if 'synonym' in node[1]:
        for synonym in node[1]['synonym']:
            synonyms.append(get_name(synonym))        
    parents = []
    if ('is_a' in node[1]):
        parents = node[1]['is_a']
    hierarchy[id]={ 'name': name, 'deep': deep, 'parents': [get_name(parent) for parent in parents], 'definition': definition, 'synonyms':synonyms}
    counter += 1
    if (counter % 100 == 0):
        print(counter,"nodes analyzed")




# Create a client instance. The timeout and authentication options are not required.
solr = pysolr.Solr('http://librairy.linkeddata.es/data/decs', always_commit=True, timeout=50)

print("saving to solr..")
counter = 0
documents = []
for category in hierarchy.keys():
    data = hierarchy[category]
    document = { 'id': category, 'name_s': data['name'], 'deep_i': data['deep'], 'parents':data['parents'], 'definition_s':data['definition'], 'synonyms':data['synonyms'] }
    documents.append(document)
    counter += 1
    if (counter % 100 == 0):
        solr.add(documents)
        print(counter,"docs saved")
        documents = []
        
        
        
        
        
        