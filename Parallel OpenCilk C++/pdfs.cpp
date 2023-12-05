#include "Bag.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <sys/time.h>
#include <iostream>
#include <cilk/cilk.h>
using namespace std;

double getTime(struct timeval arg)
{
	return arg.tv_sec + (arg.tv_usec / 1000000.0);
}
double getCurrentTime()
{
	struct timeval t;
	gettimeofday(&t, NULL);
	return getTime(t);
}

typedef struct graphstruct { // A graph in compressed-adjacency-list (CSR) form
	int nv;            // number of vertices
	int ne;            // number of edges
	int *nbr;          // array of neighbors of all vertices
	int *firstnbr;     // index in nbr[] of first neighbor of each vtx
} graph;


int read_edge_list (int **tailp, int **headp, const char *fname) {
	int max_edges = 100000000; // 20 mil, atm
	int nedges, nr, t, h;
	FILE *fp = fopen(fname, "r");


	*tailp = (int *) calloc(max_edges, sizeof(int));
	*headp = (int *) calloc(max_edges, sizeof(int));
	nedges = 0;
	nr = fscanf(fp, "%i %i",&t,&h);
	while (nr == 2) {
		if (nedges >= max_edges) {
			printf("Limit of %d edges exceeded.\n",max_edges);
			exit(1);
		}
		(*tailp)[nedges]= t;
		(*headp)[nedges++] = h;
		nr = fscanf(fp, "%i %i",&t,&h);
	}
	return nedges;
}

graph * graph_from_edge_list (int *tail, int* head, int nedges) {
	graph *G;
	int i, e, v, maxv;
	G = (graph *) calloc(1, sizeof(graph));
	G->ne = nedges;
	maxv = 0;

	// count vertices
	for(e = 0; e < G->ne; e++) {
		if (tail[e] > maxv) maxv = tail[e];
		if (head[e] > maxv) maxv = head[e];	
	}
	G->nv = maxv+1;
	G->nbr = (int *) calloc(G->ne, sizeof(int));
	G->firstnbr = (int *) calloc(G->nv+1, sizeof(int));

	// count neighbors of vertex v in firstnbr[v+1],
	for(e = 0; e < G->ne; e++) G->firstnbr[tail[e]+1]++;

	// cumulative sum of neighbors gives firstnbr[] values
	for(v = 0; v < G->nv; v++) G->firstnbr[v+1] += G->firstnbr[v];

	// pass through edges, slotting each one into the CSR structure
	for(e = 0; e < G->ne; e++) {
		i = G->firstnbr[tail[e]]++;
		G->nbr[i] = head[e];	
	}
	// the loop above shifted firstnbr[] left; shift it back right
	for (v = G->nv; v > 1; v--) G->firstnbr[v] = G->firstnbr[v-1];
	//G->firstnbr[0] = 0;
	return G;
}


void print_CSR_graph (graph *G) {
	int vlimit = 20;
	int elimit = 50;
	int e,v;
	printf("\nGraph has %d vertices and %d edges.\n",G->nv,G->ne);
	printf("firstnbr =");
	if (G->nv < vlimit) vlimit = G->nv;
	for (v = 0; v <= vlimit; v++) printf(" %d",G->firstnbr[v]);
	if (G->nv > vlimit) printf(" ...");
	printf("\n");
	printf("nbr =");
	if (G->ne < elimit) elimit = G->ne;
	for (e = 0; e < elimit; e++) printf(" %d",G->nbr[e]);
	if (G->ne > elimit) printf(" ...");
	printf("\n\n");
}





void process_layer(graph *G, Bag* & in_bag, Bag_reducer* & out_bag, int* & parent)
{	
	
	int *bag_array = in_bag->write_array();
	int size = in_bag->size();
	for(int i = 0; i < size; i++)
	{
		int current_node = bag_array[i];
		int end = G->firstnbr[current_node+1];
		for(int j = G->firstnbr[current_node]; j < end; j++)
		{
			int current_neighbor = G->nbr[j];
			if(parent[current_neighbor] == -1)
			{
				parent[current_neighbor] = current_node;				
				out_bag->insert(current_neighbor);

			}
		}
	}
	delete [] bag_array;
	return;
	
}



void dfs(graph *G, Bag_reducer* & out_bag, int* & parent)
{
	int *array_bag = out_bag->write_array();
	int size = out_bag->size();
	

	cilk_for(int i = 0; i < size; i++){
		int node = array_bag[i];
		Bag *in_bag_new = new Bag();
		Bag_reducer* out_bag_new = new Bag_reducer();
		in_bag_new->insert(node);

		 cilk_spawn  process_layer(G, in_bag_new, out_bag_new, parent);
		cilk_sync;

		if(~out_bag_new->empty()){

			cilk_spawn dfs(G,out_bag_new, parent);
			
			
		}
		
	}
	cilk_sync;

			 
	
	return;


}


void pbfs (int s, graph *G, int **parentp) {
	int *parent;	

	parent = *parentp = (int *) calloc(G->nv, sizeof(int));
	for(int v = 0; v < G->nv; v++) parent[v] = -1;	
	
	Bag* bag = new Bag();
	bag->insert(s);
	
	Bag_reducer* out_bag = new Bag_reducer();
	process_layer(G, bag, out_bag, parent);	
	dfs(G, out_bag, parent);

		

}



int main () {
	cout<<"running";
	graph *G;
	int  *parent;
	int *tail, *head;
	int nedges;
	int startvtx;
	int i, v, reached;
	const char* file ="./language.txt";
	

	cout << "Iniciando";

	startvtx = 0; 

	double begin = getCurrentTime();

	nedges = read_edge_list(&tail, &head, file);
	G = graph_from_edge_list(tail, head, nedges);
	free(tail);
	free(head);

	// PARALLEL BFS WITH TIMING
	pbfs (startvtx, G, &parent)
	cout << getCurrentTime()-begin << endl;

	return 0;
}
