import sys;

def projective(nodes, heads, sid): #{
	k = list(heads.keys());
	k.sort();

	for i in k: #{
		for j in k: #{
			if j > i and j < heads[i]: #{
				if heads[j] > heads[i] or heads[j] < i: #{
					#print('%d [0] i: %d | j: %d | h[i]: %d | h[j]: %d' % (sid, i, j, heads[i], heads[j]), file=sys.stderr);
					return False;
				#}
			#}
			if j > heads[i] and j < i: #{
				if heads[j] > i or heads[j] < heads[i]: #{
					#print('%d [1] i: %d | j: %d | h[i]: %d | h[j]: %d' % (sid, i, j, heads[i], heads[j]), file=sys.stderr);
					return False;
				#}
			#}
			if heads[j] > i and heads[j] < heads[i]: #{
				if j < i or j > heads[i]: #{
					#print('%d [2] i: %d | j: %d | h[i]: %d | h[j]: %d' % (sid, i, j, heads[i], heads[j]), file=sys.stderr);
					return False;
				#}
			#}
			if heads[j] > heads[i] and heads[j] < i: #{
				if j > i or j < heads[i]: #{
					#print('%d [3] i: %d | j: %d | h[i]: %d | h[j]: %d' % (sid, i, j, heads[i], heads[j]), file=sys.stderr);
					return False;
				#}
			#}
		#}
	#}
	
	return True;
#}

puu = {};
heads = {};
blokk = '';
n_np = 0; # non-projective
sent = 0;
tok = 0;
n_dist = 0.0;
lem_label = {};
for line in sys.stdin.readlines(): #{

	if line.count('\t') == 9: #{
		row = line.split('\t')		
		blokk = blokk + line;
		if row[0].count('-') > 0 or row[0].count('.') > 0: #{
			continue;
		#}
		try: #{
			head = int(row[6]);
		except: #{
			print('ERROR:', line, file=sys.stderr);
		#}
		dep = int(row[0]);
		if head not in puu: #{
			puu[head] = [];
		#}
		puu[head].append(dep);
		heads[dep] = head;
		tok = tok + 1;

		if row[2] not in lem_label: #{
			lem_label[row[2]] = set();
		#}
		lem_label[row[2]].add(row[7]);

	elif line[0] == '#': #{
		blokk = blokk + line;
	elif line[0] == '\n': #{
		blokk = blokk + line;
		if blokk == '\n': #{
			continue;
		#}
		proj = projective(puu, heads, sent);
		if not proj: #{
			n_np = n_np + 1;
			sys.stdout.write(blokk);
		#}
		#print(sent, proj, puu, heads, file=sys.stderr);
		puu = {};
		heads = {};
		blokk = '';
		sent = sent + 1;
	#}	
#}

print('total: %d; non-projective: %d' % (sent, n_np), file=sys.stderr)
print('%d\t%d\t%.2f' % (sent, n_np, n_np/sent*100.0), file=sys.stderr)
