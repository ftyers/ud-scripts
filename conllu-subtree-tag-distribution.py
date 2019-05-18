import sys 

LABEL = sys.argv[1]

# for each sentence
#    for each node
#       check if the label is LABEL
#          if it is, recurse down, storing the frequency counts of pos tags

trees = []
current_tree = {}
for line in sys.stdin.readlines():
	if line.strip() == '':
		trees.append(current_tree)
#		print(current_tree)
		current_tree = {}
		continue
	elif line[0] == '#':
		continue

	row = line.split('\t')
	idx = int(row[0])
	pos = row[3]
	head = int(row[6])
	deprel = row[7]
	if head not in current_tree: 
		current_tree[head] = []
	current_tree[head].append((idx, deprel, pos))

def dfs(freq, node, tree):
	if node not in tree:
		return freq
	for child in tree[node]:
		if child[2] not in freq:
			freq[child[2]] = 0
		freq[child[2]] += 1
		print('S:', node, child, tree[node], '|',freq[child[2]])
		if child[0] in tree:
			freq = dfs(freq, child[0], tree)

	return freq

freq = {}

for tree in trees:
	print()
	k = list(tree.keys())
	k.sort()
	for head in k:
		for child in tree[head]:
			if child[1] == LABEL:
				print('T:',head, child)
				dfs(freq, child[0], tree)


for tag in freq:
	print(tag, freq[tag])

