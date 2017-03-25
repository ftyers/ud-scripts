import sys

# --------------------------------------------------------------------------------- #

def _input(buffer): #{
	weights = {}
	names = {}
	nodes = {};
	comments = [];
	for f in buffer: #{
		for line in buffer[f].split('\n'): #{
			if line.strip() == '': #{
				break;
			#}
			if line[0] == '#': #{
				comments.append(line.strip('\n'));
				continue;
			#}
			#print('§', line, file=sys.stderr);
			row = line.rstrip().split('\t');
			if row[0].count('-') > 0: #{
				continue;
			#}
			name = row[7]
			src = int(row[6])
			dst = int(row[0])
			weight = 1.0
			t = (src,dst)
			if t in weights: #{
				weights[t] -= weight;
			else: #{
				weights[t] = weight;
			#}
			names[t] = name;
			nodes[dst] = row[1:6];
		#}
	#}	
	comments = list(set(comments));
	for c in comments: #{
		print(c);
	#}
	return weights,names,nodes;
#}

def _load(arcs,weights):
	g = {}
	for (src,dst) in arcs: #{
		if src in g: #{
			g[src][dst] = weights[(src,dst)]
		else: #{
			g[src] = { dst : weights[(src,dst)] }
		#}
	#}
	return g

def _reverse(graph):
	r = {}
	for src in graph: #{
		for (dst,c) in list(graph[src].items()): #{
			if dst in r: #{
				r[dst][src] = c
			else: #{
				r[dst] = { src : c }
			#}
		#}
	#}
	return r

def _getCycle(n,g,visited=set(),cycle=[]): #{
	visited.add(n)
	cycle += [n]
	if n not in g: #{
		return cycle
	#}
	for e in g[n]: #{
		if e not in visited: #{
			cycle = _getCycle(e,g,visited,cycle)
		#}
	#}
	return cycle
#}

def _mergeCycles(cycle,G,RG,g,rg):
	allInEdges = []
	minInternal = None
	minInternalWeight = sys.maxsize

	# find minimal internal edge weight
	for n in cycle: #{
		for e in RG[n]: #{
			if e in cycle: #{
				if minInternal is None or RG[n][e] < minInternalWeight: #{
					minInternal = (n,e)
					minInternalWeight = RG[n][e]
					continue
				#}
			else: #{
				allInEdges.append((n,e))		
			#}
		#}
	#}

	# find the incoming edge with minimum modified cost
	minExternal = None
	minModifiedWeight = 0
	for s,t in allInEdges: #{
		u,v = rg[s].popitem()
		rg[s][u] = v
		w = RG[s][t] - (v - minInternalWeight)
		if minExternal is None or minModifiedWeight > w: #{
			minExternal = (s,t)
			minModifiedWeight = w
		#}
	#}

	u,w = rg[minExternal[0]].popitem()
	rem = (minExternal[0],u)
	rg[minExternal[0]].clear()

	if minExternal[1] in rg: #{
		rg[minExternal[1]][minExternal[0]] = w
	else: #{
		rg[minExternal[1]] = { minExternal[0] : w }
	#}

	if rem[1] in g: #{
		if rem[0] in g[rem[1]]: #{
			del g[rem[1]][rem[0]]
		#}
	#}

	if minExternal[1] in g: #{
		g[minExternal[1]][minExternal[0]] = w
	else: #{
		g[minExternal[1]] = { minExternal[0] : w }
	#}
#}

# --------------------------------------------------------------------------------- #

def mst(root,G): #{
	""" The Chu-Lui/Edmond's algorithm

	arguments:

	root - the root of the MST
	G - the graph in which the MST lies

	returns: a graph representation of the MST

	"""

	RG = _reverse(G)
	if root in RG:
		RG[root] = {}

	g = {}
	# for node in the reversed graph
	for n in RG: #{
		if len(RG[n]) == 0: #{
			continue
		#}
		minimum = sys.maxsize
		s,d = None,None 
		# for edge in the list 
		for e in RG[n]: #{ 
			if RG[n][e] < minimum: #{
				minimum = RG[n][e]
				s,d = n,e
			#}
		#}
		if d in g: #{
			g[d][s] = RG[s][d]
		else: #{
			g[d] = { s : RG[s][d] } 
		#}
	#}	

	# graph now has only the lowest weight arcs incoming arcs
	
	cycles = []
	visited = set()
	for n in g: #{
		if n not in visited: #{
			cycle = _getCycle(n,g,visited) 
			cycles.append(cycle)
		#}
	#}

	rg = _reverse(g)
	for cycle in cycles: #{
		if root in cycle: #{
			continue 
		#}
		_mergeCycles(cycle, G, RG, g, rg) 
	#}	

	return g
#}

# --------------------------------------------------------------------------------- #

if __name__ == "__main__": #{
	filenames = [];
	filenames = sys.argv[1:]

	if len(filenames) < 2: #{
		sys.stderr.write('no input and/or root node specified\n')
		sys.stderr.write('usage: python3 conllu-voting.py <file1> <file2> ...\n')
		sys.exit(1)
	#}


	fds = {};
	for f in filenames: #{
		fds[f] = open(f);
	#}

	buffer = {};
	while True: #{
			
		for f in fds: #{
			if f not in buffer: #{
				buffer[f] = '';
			#}
			while True: #{
				line = fds[f].readline();
				buffer[f] += line;
				if line.strip() == '': #{
					break;
				#}
			#}
		#}	
		eof = False;
		for f in buffer: #{
			if buffer[f] == '': #{
				eof = True;
			#}
		#}
		if eof: #{
			break;
		#}

		#print(buffer);
		weights,names,nodes = _input(buffer)

		#print('@',names, file=sys.stderr)
		#print('@',weights, file=sys.stderr);
		#print('@',nodes, file=sys.stderr);
		g = _load(weights,weights);
		h = mst(0, g)
		heads = {};
		for s in h: #{
			for t in h[s]: #{
				heads[t] = s;
			#}
		#}
	
		for t in nodes: #{
			ord = nodes[t][0];
			lem = nodes[t][1];
			upos = nodes[t][2];
			xpos = nodes[t][3];
			mor = nodes[t][4];
			deprel = names[(heads[t], t)];
			misc = '_';
			misc = 'ArcWeight=' + str(weights[(heads[t], t)]);
			#     idx sur lem  up  xp mor hed dep deps mis
			#      0   1   2   3   4  5    6   7   8    9  
			print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (t, ord, lem, upos, xpos, mor, heads[t], deprel, '_', misc));
		#}	
		print('');
	
		buffer = {};
	#}
#}

