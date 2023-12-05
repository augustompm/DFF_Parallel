from classes import *
import sys
import numpy as np


def read_edge_list(tailp,headp, path):
    max_edges = 25
	
    f = open(path,'r')
    tailp = max_edges*[0]
    headp = max_edges*[0]
    nedges = 0
    list_edges = [[*a.split(' ')] for a in f.read().split("\n") if len(a)>1]
    list_edges = [[int(a[0]),int(a[1])] for a in list_edges]

    if len(list_edges)> max_edges:
        print(f'Limit of edges {max_edges} exceeded.\n')
        return 


    for pair in list_edges:
        tailp[nedges] = pair[0]
        headp[nedges] = pair[1]
        nedges+=1
	        
    return tailp,headp, nedges
    
def graph_from_edge_list(tail, head, nedges):
	G = Graph()                                                                                                 
	G.ne = nedges	
	maxv = max([t for t in tail if t != None]) if max([t for t in tail if t != None])>max([h for h in head if h != None]) else max([h for h in head if h != None])     
	G.nv = maxv+1
	G.nbr = G.ne*[0]
	G.firstnbr = (G.nv+1)*[0]
     
    
	for e in range(G.ne): 
		G.firstnbr[tail[e]+1]+=1

	for v in range(G.nv):
		G.firstnbr[v+1] += G.firstnbr[v]
	
	for e in range(G.ne): 
		i = G.firstnbr[tail[e]]
		G.firstnbr[tail[e]]+=1
		G.nbr[i] = head[e]

	for v in reversed(range(2,G.nv+1)):
		G.firstnbr[v] = G.firstnbr[v-1]

	return  G

def print_CSR_graph(G):
	vlimit = 20;
	elimit = 50;
	
	print(f'\n Graph has {G.nv} vertices and {G.ne} edges.\n')
	print("firstnbr =");
	if G.nv < vlimit: vlimit = G.nv
	for v in range(vlimit+1): print(f'{G.firstnbr[v]}')
	if G.nv > vlimit: print(" ...")
	print("\n");
	print("nbr =");
	if G.ne < elimit: elimit = G.ne
	for e in range(elimit): print(f'{G.nbr[e]}')
	if G.ne > elimit: print(" ...")
	print("\n\n")




	

def process_layer(G, in_bag, out_bag, thislevel,level,parent, grainsize):

	if in_bag.size() < grainsize:	
		bag_array = in_bag.write_array()
		size = in_bag.size()

		for i in range(size):
			current_node = bag_array[i]
			end = G.firstnbr[current_node+1]
			for j in range(G.firstnbr[current_node],end):
				current_neighbor = G.nbr[j]
				if level[current_neighbor] == -1:
					parent[current_neighbor] = current_node
					level[current_neighbor] = thislevel+1
					out_bag.insert(current_neighbor)
         
		del bag_array
		return
	
	new_bag = in_bag.split()
	process_layer(G, new_bag, out_bag, thislevel, level, parent,grainsize)
	process_layer(G, in_bag, out_bag, thislevel, level, parent,grainsize)


def pbfs(s, G, levelp,nlevelsp, levelsizep, parentp, grainsize):	

	level = G.nv*2*[None]
	levelsize = G.nv*2*[None]
	parent = G.nv*2*[None]

	for v in range(G.nv): level[v] = -1
	for v in range(G.nv): parent[v] = -1

	thislevel = 0
	level[s] = 0
	levelsize[0] = 1
	bag = Bag()
	bag.insert(s)
	while not bag.empty():
		levelsize[thislevel] = bag.size()
		out_bag = Bag()
		process_layer(G, bag, out_bag, thislevel, level, parent, grainsize)
		thislevel+=1
		bag.clear()
		for i in range(bag.forest_size):
			if out_bag.forest[i] != None:
				bag.forest[i] = out_bag.forest[i]
		
	
	nlevelsp = thislevel




def main(path, grain_size):
	startvtx = 0
	tail=[]
	head=[]
	level=None
	nlevels=None
	levelsize=None
	parent=None

	tail, head,nedges = read_edge_list(tail, head, path)
	G = graph_from_edge_list(tail, head,nedges)


	pbfs(startvtx, G, level, nlevels, levelsize, parent, grain_size)
	print_CSR_graph(G)



if __name__ == '__main__':
	path = "C:\\Users\\0331413\\Desktop\\src\\sample.txt" #sys.argv[1]
	grain_size = 20 # int(sys.argv[2])
	main(path,grain_size)




