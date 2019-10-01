#!/usr/bin/env python3
# libraries
import networkx as nx
import matplotlib.pyplot as plt
import json, sys, io

data = json.load(sys.stdin)

# Build a dataframe with your connections
froms = []
tos = []
weights = []

gr = nx.DiGraph()

for key in data:
    sum = 0
    print(data[key])
    for prev_key in data[key]:
        if prev_key == "START":
            continue
        sum += data[key][prev_key]
    for prev_key in data[key]:
        if prev_key == "START":
            continue
        froms.append(prev_key)
        tos.append(key)
        weights.append(data[key][prev_key]/sum*100)
        gr.add_edge(prev_key, key, weight=data[key][prev_key]/sum)


print("ciao")

# nx.draw(gr,with_labels=True, )
# plt.draw()
# plt.show()

# use one of the edge properties to control line thickness
edgewidth = [ d['weight'] for (u,v,d) in gr.edges(data=True)]

# layout
pos = nx.spring_layout(gr, iterations=50, k=0.05)
#pos = nx.random_layout(G)

# rendering
# plt.figure(1)
# plt.subplot(211); plt.axis('off')
nx.draw_networkx_nodes(gr, pos, node_size=1000)
nx.draw_networkx_edges(gr, pos, width=edgewidth, node_size=1000)
nx.draw_networkx_labels(gr,pos, node_size=1000)
# nx.draw(gr, pos, width=edgewidth, node_size=1000)
plt.show()
