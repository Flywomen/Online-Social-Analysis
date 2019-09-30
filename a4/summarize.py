"""
sumarize.py
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
    queue.append((root,0))f
    
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

def read_graph(filename):
    """ Read 'edges.txt.gz' into a networkx **undirected** graph.
    Done for you.
    Returns:
      A networkx undirected graph.
    """
    return nx.read_edgelist(filename, delimiter='\t')

def get_subgraph(graph, min_degree):
    cgraph= graph.copy()
    for node in graph.nodes():
        if graph.degree(node)< min_degree:
            cgraph.remove_node(node)
    return cgraph

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


def number_of_users(filename, output):
	number_of_users = 0
	f = open(filename)
	for line in f:
		number_of_users += 1
	w = open(output, "w")
	w.write('Number of users collected: %d\n' % number_of_users)
	w.close()

def number_of_messages(output):
	w = open(output, "a")
	w.write('\nNumber of messages collected: 100\n')
	w.close()


def number_of_communities(filename, output):
	graph = read_graph(filename)
	subgraph = get_subgraph(graph, 2)
	clusters = partition_girvan_newman(subgraph, 3)
	w = open(output, "a")
	w.write('\nNumber of communities discovered: %d\n' % len(clusters))
	w.close()


def average_number_of_users_per_community(filename, output):
	total = 0
	graph = read_graph(filename)
	subgraph = get_subgraph(graph, 2)
	clusters = partition_girvan_newman(subgraph, 3)
	for i in range(len(clusters)):
		total += clusters[i].order()
	w = open(output, "a")
	w.write('\nAverage number of users per community: %.2f\n' % (float(total) / float(len(clusters))))
	w.close()


def number_of_instance_per_class_found(filename1, filename2, filename3, output):
	n1 = 0
	n2 = 0
	n3 = 0
	for line in open(filename1):
		n1 += 1
	for line in open(filename2):
		n2 += 1
	for line in open(filename3):
		n3 += 1
	w = open(output, "a")
	w.write('\nNumber of instances per class found:\n')
	w.write('Good emotion: %d\n' % (n1 / 2))
	w.write('Neutral emotion: %d\n' % (n2/2))
	w.write('Bad emotion: %d\n' % (n3/2))
	w.close()


def example_from_each_class(filename1, filename2, filename3, output):
    w = open(output, "a")
    w.write("\nOne example from each class:\n")
    f1 = open(filename1,"r")
    w.write("example from Good emotion: %s\n" % str(f1.readline()))
    f1.close()
    f2 = open(filename2,"r")
    w.write("example from Neutral emotion: %s\n" % str(f2.readline()))
    f2.close()
    f3 = open(filename3,"r")
    w.write("example from Bad emotion: %s\n" % str(f3.readline()))
    f3.close()
    w.close()


def main():
	output = open("summary.txt", "w")
	output.close()
	number_of_users('candidates4a4.txt', "summary.txt")
	number_of_messages("summary.txt")
	number_of_communities('users.txt', "summary.txt")
	average_number_of_users_per_community('users.txt', "summary.txt")
	number_of_instance_per_class_found('good.txt', 'neutral.txt', 'bad.txt', "summary.txt")
	example_from_each_class('good.txt', 'neutral.txt', 'bad.txt', "summary.txt")

if __name__ == '__main__':
    main()
