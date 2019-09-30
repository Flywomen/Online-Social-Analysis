"""
cluster.py
community detection.
"""
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
from TwitterAPI import TwitterAPI
from collections import Counter, defaultdict, deque
import copy
import math
import urllib.request


def bfs(graph, root, max_depth):
    
    #initialization
    node2distances = defaultdict(int)
    node2num_paths = defaultdict(int)
    node2parents   = defaultdict(list)
    
    queue= deque()#queue to store nodes
    queue.append((root,0))
    
    node2distances[root]=0
    node2num_paths[root]=1
    
    #bfs
    while (len(queue)>0):
        node,depth = queue.popleft()#
        if depth >= max_depth:
            break
        for neighbornode in graph.neighbors(node):
            if neighbornode not in node2distances:
                node2distances[neighbornode] = node2distances[node] + 1
                if (node2distances[neighbornode]<max_depth):
                    queue.append((neighbornode,0))
            if node2distances[node] == node2distances[neighbornode] - 1:
                node2parents[neighbornode].append(node)
                node2num_paths[neighbornode] +=1
                
    return node2distances, node2num_paths, node2parents


def bottom_up(root, node2distances, node2num_paths, node2parents):
    nodedict = defaultdict(int)
    for node in node2distances.keys():
        nodedict[node] = 1
    nodedict[root] = 0

    edgedict = defaultdict(int)

    t = sorted(node2distances.items(), key=lambda d: -d[1])

    farbetween = []
    for i in t:
        farbetween.append(i[0])

    for node in farbetween:

        if node in node2parents:
            parentlist = node2parents[node]

            totalpath = 0
            for p in parentlist:
                totalpath += node2num_paths[p]

            for p in parentlist:

                edgecredit = node2num_paths[p] * nodedict[node] / totalpath

                nodedict[p] += edgecredit

                edgedict[tuple(sorted((node, p)))] += edgecredit

    return dict(edgedict)

def approximate_betweenness(graph, max_depth):
    result = defaultdict(int)
    for node in graph.nodes():
        node2distances, node2num_paths, node2parents = bfs(graph, node, max_depth)
        r = bottom_up(node, node2distances, node2num_paths, node2parents)
        for k, value in sorted(r.items()):
            if k not in result:
                result[k] = value
            else:
                result[k] = result[k] + value
    for k, value in result.items():
        result[k] = value/2.0
    return result


def partition_girvan_newman(graph, max_depth):
    cgraph = graph.copy()
    result = approximate_betweenness(cgraph, max_depth)
    lists = sorted(result.items(),key = lambda x: (-x[1],x[0]))
    components = [c for c in nx.connected_component_subgraphs(cgraph)]
    for i in lists:
        cgraph.remove_edge(*i[0])
        components = [c for c in nx.connected_component_subgraphs(cgraph)]
        if len(components)>1:
            break
    return components

def get_subgraph(graph, min_degree):
    cgraph= graph.copy()
    for node in graph.nodes():
        if graph.degree(node)< min_degree:
            cgraph.remove_node(node)
    return cgraph

def read_graph():
    """ Read 'edges.txt.gz' into a networkx **undirected** graph.
    Done for you.
    Returns:
      A networkx undirected graph.
    """
    return nx.read_edgelist('users.txt', delimiter='\t')


def main():
    """
    FYI: This takes ~10-15 seconds to run on my laptop.
    """
    graph = read_graph()
    subgraph = get_subgraph(graph, 2)

    clusters = partition_girvan_newman(subgraph, 3)

    text_file = open("community.txt", "w")
    text_file.write('graph has %d nodes and %d edges\n' % 
        (graph.order(), graph.number_of_edges()))
    text_file.write('We filter nodes which have less than 2 degrees to get subgraph\n')
    text_file.write('subgraph has %d nodes and %d edges\n' % 
        (subgraph.order(), subgraph.number_of_edges()))
    text_file.write('first partition: cluster 1 has %d nodes and cluster 2 has %d nodes\n' % 
        (clusters[0].order(), clusters[1].order()))
    text_file.write('Number of communities discovered: %d\n' % len(clusters))
    text_file.write('Average number of users per community: %.2f\n' % 
        (float((clusters[0].order() + clusters[1].order())) / float(len(clusters))))
    text_file.close()


if __name__ == '__main__':
    main()
    
