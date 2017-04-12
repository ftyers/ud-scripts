import copy, sys

class DependencyTreeNode: #{
	"""
	class which is a node of the dependency tree
	"""
	def __init__(self):
		"""
		initialises the variables and fields of the node
		"""

		self.fields = {
			"id": None, #id
			"form": None, #form
			"lemma": None, #lemma
			"upostag": None, #universal part-of-speech tag
			"xpostag": None, #language specific part-of-speech tag
			"feats": None, #list of morphological features
			"head": None, #head of the current word (val of ID or 0)
			"deprel": None, #universal dependency relation to the HEAD (root iff HEAD = 0)
			"deps": None, #enchanced dependency graph (list of head-deprel pairs)
			"misc": None, #any other annotation
			"children": [] #points to the children
		}

		self.features = {}

		self.score = []

		self.neighbouring_nodes = { # indices of nodes that are +n -> nchildren, -n -> nparents
			"-2": [],
			"-1": [],
			"0": [],
			"1": [],
			"2": []
		}

		self.domain = [] # words that are direct children and the node itself
		self.agenda = None  # word order beam
		self.beam = []  # beam for a node

	def update_field(self, id, val):
		"""
		changes the value of a certain field
		:param id: id of a field
		:param val: value to which it's changed
		:return: None
		"""
		self.fields[id] = val

	def give_domain(self):
		"""
		returns a domain for a given node
		:return: self.domain
		"""
		return self.domain

	def extract_features(self):
		"""
		extracts all the features from the feats field
		:return: None
		"""
		if self.fields["feats"] == "_":
			return

		temp = self.fields["feats"].split('|') #split features
		for feat in temp:
			temp1 = feat.split('=') # splits into a feature and value
			self.features[temp1[0]] = temp1[1]

#}

class DependencyTree: #{
	"""
	a class that holds the whole dependency tree
	"""

	def __init__(self):
		"""
		initialises the whole dependency tree and creates the conversion table for fields from the input
		"""
		self.tree = {} # dictionary of nodes -> id

		self.no2field = {
				"0":"id", #id
				"1":"form", #form
				"2":"lemma", #lemma
				"3":"upostag", #universal part-of-speech tag
				"4":"xpostag", #language specific part-of-speech tag
				"5":"feats", #list o-f morphological features
				"6":"head", #head of the current word (val of ID or 0)
				"7":"deprel", #universal dependency relation to the HEAD (root iff HEAD = 0)
				"8":"deps", #enchanced dependency graph (list of head-deprel pairs)
				"9":"misc" #any other annotation
		}

		self.head = None

	def add_node(self, list):
		"""
		adds a node of type DependencyTreeNode to the class
		:param list: val of fields got from input
		:return: None
		"""
		temp = DependencyTreeNode()

		for no in range(0, 10): # indices of all the fields
				temp.update_field(self.no2field[str(no)], list[no])

		temp.beam = [[temp.fields["id"]]]

		self.tree[temp.fields["id"]] = temp
		self.tree[temp.fields["id"]].extract_features()

		if temp.fields["head"] =="0":
				self.head = temp.fields["id"]

	def print_tree(self):
		"""
		prints the val of fields for every node
		:return: None
		"""
		for id in self.tree:
				print (self.tree[id].fields,"\n")

	def add_children(self):
		"""
		fills out the children field for every node
		:return: None
		"""
		for id in self.tree:
				if self.tree[id].fields["head"] !="0" and self.tree[id].fields["head"] !="_":
					self.tree[self.tree[id].fields["head"]].fields["children"].append(id)

	def calculate_domains(self):
		"""
		fills out the domain fields for every node
		:return: None
		"""

		for id in self.tree:
				self.tree[id].domain = [id]

				for child in self.tree[id].fields["children"]:
					self.tree[id].domain.append(child)

	def set_neigbouring_nodes(self):
		"""
		Calculates the gparents, parents, children and gchildren of every node in a tree
		:return: None
		"""
		for node in self.tree:
				self.tree[node].neighbouring_nodes["0"] = [node]


				if self.tree[node].fields["head"] !="0" and self.tree[node].fields["head"] !="_":
					self.tree[node].neighbouring_nodes["-1"] = [self.tree[node].fields["head"]] # parent

					if self.tree[self.tree[node].fields["head"]].fields["head"] !="0" and self.tree[self.tree[node].fields["head"]].fields["head"] !="_":
						self.tree[node].neighbouring_nodes["-2"] = [self.tree[self.tree[node].fields["head"]].fields["head"]] # grandparent

				self.tree[node].neighbouring_nodes["1"] = self.tree[node].fields["children"] #children

				self.tree[node].neighbouring_nodes["2"] = []

				for child in self.tree[node].fields["children"]:
					self.tree[node].neighbouring_nodes["2"] += self.tree[child].fields["children"] #gchildren


	def ufeat(self, node, position, feature):
		"""
		returns a feature or a vector of features
		:param node:
		:param position:
		:param feature:
		:return: value of a feature for nodes of given relation
		"""
		res = []
		for node_1 in self.tree[node].neighbouring_nodes[position]:
				tmp = self.tree[node_1].features.get(feature, None)
				if tmp != None:
					res.append(tmp)

		return res

	def lemma(self, node, position):
		"""
		returns the lemma of a nparent of the node (for position <0) or a nchildren
		:param node: the relative node
		:param position: the relative position to this node
		:return: lemma
		"""
		res = []

		for node_1 in self.tree[node].neighbouring_nodes[position]:
				res.append(self.tree[node_1].fields["lemma"])

		return res

	def count(self, node, position):
		"""
		count the number of nchildren
		:param node: the relative node
		:param position: the relative position to this node
		:return: the number of nchildren
		"""
		return len(self.tree[node].neighbouring_nodes[position])

	def upos(self, node, position):
		"""
		returns the part of speech
		:param node: the relative node
		:param position: the relative position
		:return: upostag
		"""
		res = []
		for node_1 in self.tree[node].neighbouring_nodes[position]:
				res.append(self.tree[node_1].fields["upostag"])

		return res

	def deprel(self, node, position):
		"""
		returns the relation to the HEAD
		:param node: the relative node
		:param position: the relative position to this node
		:return: the deprel tag
		"""
		res = []

		for node_1 in self.tree[node].neighbouring_nodes[position]:
				res.append(self.tree[node_1].fields["deprel"])

		return res

	def generate_conllu(self):
		"""
		generates the tree in the CONLLU format and puts it to the stdout
		:return:
		"""

		size = len(self.tree)

		for node in range(1, size+1):
				line =""
				for field in range(0, 10):
					line += self.tree[str(node)].fields[self.no2field[str(field)]] +"\t"

				sys.stdout.write(line.strip('\t')+"\n")

		sys.stdout.write('\n')

#}


class GreedyLifting: #{
	"""
	a class performing the greedy lifting algorithm as described here:
	"""

	def __init__(self):
		self.tree = None
		self.lifts = dict()
		self.max_lifts = 1000
		self.max_length = 3

	def execute(self, T):
		"""
		main method, executes the whole algorithm
		:param T: the tree
		:return: the lifted tree
		"""
		self.tree = copy.deepcopy(T)
		tmp = True

		while tmp: # while last time the algorithm lifted something
			tmp = self.DFS1(self.tree.head)

		return self.tree


	def DFS1(self, node):
		"""
		find the first node of a pair that will be to be lifted
		:param node: the current node
		:return: (Boolean) whether the algorithm lifted something or not
		"""

		for child in self.tree.tree[node].fields["children"]:
			if node != self.tree.head:
				tmp = self.DFS2(node, child, 1)

				if tmp:
					return True

			tmp = self.DFS1(child)

			if tmp:
				return True

		return False

	def DFS2(self, ancestor, node, length):
		"""
		looks for the second node of a pair to be lifted (the lower one), first taking the smallest paths
		:param ancestor: the first node of a pair
		:param node: the current node
		:param length: the length of a path from one node to another
		:return: (Boolean) whether the algorithm lifted something or not
		"""

		if not self.is_projective(ancestor, node): #{
			tmp = self.lifts.get(node, 0) # how many times a node has already been lifted

			# max lifts per node # @@@
			if tmp < self.max_lifts and self.tree.tree[node].fields["deprel"] == "punct": #{
			#if tmp < self.max_lifts: #{
				self.lifts[node] = self.lifts.get(node, 0) + length # add the number of lifts done this time 
				self.lift(ancestor, node)
				return True
			#}
		#}

		if length < self.max_length: # the max length of a path

			for child in self.tree.tree[node].fields["children"]: # continue the search for a non-projective edge
				tmp = self.DFS2(ancestor, child, length+1)
				if tmp:
					return True

		return False

	def is_projective(self, ancestor, b):
		"""
		checks whether the edge is projective
		:param ancestor: a node
		:param b: a node
		:return: (Boolean)
		"""
		begin = min(int(ancestor), int(b))
		end = max(int(ancestor), int(b)) - 1

		for node in range(begin, end):
			if not self.is_ancestor(str(node), ancestor): # if confused, look at the def of projectivity
				return False

		return True

	def is_ancestor(self, a, b):
		"""
		checkhs whether a is an ancestor of b
		:param a:
		:param b:
		:return: (Boolean
		"""
		if self.tree.tree[a].fields["head"] == '0':
			return False

		while self.tree.tree[a].fields["head"] != self.tree.head :
			if self.tree.tree[a].fields["head"] == b:
				return True

			a = self.tree.tree[a].fields["head"]

		return False

	def lift(self, a, b):
		"""
		lifts the a->b edge
		:param a: the higher node
		:param b: the lower node
		:return: None
		"""
		self.tree.tree[self.tree.tree[b].fields["head"]].fields["children"].remove(b)
		self.tree.tree[self.tree.tree[a].fields["head"]].fields["children"].append(b)
		self.tree.tree[b].fields["head"] = self.tree.tree[a].fields["head"]
	#}
#}

tree = DependencyTree()
lifting = GreedyLifting()
for line in sys.stdin.readlines(): #{
	if line.strip() == '': #{
		tree.add_children()
		tree.calculate_domains()
		tree.set_neigbouring_nodes()

		tree1 = lifting.execute(tree)
		tree1.generate_conllu();
		tree = DependencyTree()
		continue;
	#}

	if line[0] == '#': #{
		print(line.strip('\n'));
		continue;
	#}
	
	# deal with spans
	
	row = line.strip('\n').split('\t');
	tree.add_node(row)

#}
