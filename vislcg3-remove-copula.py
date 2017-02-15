import sys;

# IN: 
#	"<Мүмкін>"
#		"мүмкін" adj advl @advmod #1->3
#	"<бұл>"
#		"бұл" prn dem nom @nsubj #2->3
#	"<Азамат шығар>"
#		"Азамат" np ant m nom @root #3->0
#			"е" cop aor p3 sg @cop #4->3
#				"шығар" mod @discourse #5->3
#	"<?>"
#		"?" sent @punct #6->3
#	

# OUT: 
#	"<Мүмкін>"
#		"мүмкін" adj advl @advmod #1->3
#	"<бұл>"
#		"бұл" prn dem nom @nsubj #2->3
#	"<Азамат шығар>"
#		"Азамат" np ant m nom @root #3->0
#			"шығар" mod @discourse #4->3
#	"<?>"
#		"?" sent @punct #5->3
#	

def count_tokens(l): #{
	c = 0;

	for i in l: #{
		for j in l[i]: #{
			c = c + 1;
		#}
	#}
	return c;
#}

def kasitella(blokk): #{
	tokcount = 0;
	groupcount = 0;
	tokens = {};
	groups = {};
	for line in blokk.split('\n'): #{
		if line.strip() == '': #{
			continue;
		#}
		if line[0] == '"': #{
			groupcount += 1;
			groups[groupcount] = line;
			continue;
		#}
		if groupcount not in tokens: #{
			tokens[groupcount] = [];
		#}
		row = line.strip().split('#');
		(t, h) = row[1].split('->');
		a = row[0];
		tokens[groupcount].append((a, int(t), int(h)));
		tokcount += 1;
	#}

	print(groupcount, groups, file=sys.stderr);
	print(tokcount, tokens, file=sys.stderr);
	print('=====================================', file=sys.stderr);
	cur_tok = 1;
	max_tok = tokcount - 1 ;
	offset = 0;
	while cur_tok <= max_tok: #{
		new_tokens = {};
		# for each of the token groups
		for i in tokens.keys(): #{
			# for each of the tokens in group i
			new_group = [];
			null_cop = (-1, -1);
			for j in range(0, len(tokens[i])): #{
				# if the group has a null copula
				if tokens[i][j][0].count('"е" cop aor p3') > 0 and tokens[i][j][0].count('@cop') > 0: #{
					null_cop = (tokens[i][j][1], tokens[i][j][2])
					print('!!!!!!!!!!',null_cop,'|||',tokens[i][j], file=sys.stderr);
					continue;
				#}
				new_group.append(tokens[i][j]);
			#}
			# if we found a null copula [or "deleted" some node]
			if len(tokens[i]) != len(new_group): #{
				print('¶ %', null_cop, cur_tok, max_tok,'|||', i, j, '|||', tokens[i], file=sys.stderr);	
				# for all of the groups 
				for k in tokens.keys(): #{
					new_local = [];
					# for all of the tokens
					for m in range(0, len(tokens[k])): #{
						(local_tok, l_t, l_h) = tokens[k][m];
						if l_t == null_cop[0] and l_h == null_cop[1]: #{
							max_tok = max_tok - 1;
							continue;
						#}
						print('\t\t:::', cur_tok,'|', l_t, l_h,'|', k, m, file=sys.stderr)
						if l_t > null_cop[0]: #{
							l_t = l_t - 1;	
						#}
						if l_h > null_cop[0]: #{
							l_h = l_h - 1;
						#}
						x = (local_tok, l_t, l_h);
						new_local.append(x);
						print('\t\t>>>', cur_tok,'|', l_t, l_h, '|', k, m, x, new_local, file=sys.stderr)
					#}
					new_tokens[k] = new_local
				#}
				#cur_tok = null_cop[0] + null_cop[1];
				print('&&&&', null_cop, file=sys.stderr);
				cur_tok = null_cop[0] ;
				break;
			else: #{
				(local_tok, l_t, l_h) = tokens[i][j];
				print('± %', cur_tok, max_tok,'|||', i, j, '|||', tokens[i], file=sys.stderr);	
				cur_tok = l_t;
				new_tokens[i] = tokens[i];
			#}
		#} 
		print(cur_tok, max_tok, '////////////////////////////////////////////////////////////////////////', file=sys.stderr);
		print(count_tokens(tokens),'\t|', tokens, file=sys.stderr);
		print(count_tokens(new_tokens),'\t|',new_tokens, file=sys.stderr);
		if count_tokens(tokens) == count_tokens(new_tokens): #{
			break;
		#}
		tokens = new_tokens;
	#}

	for g in tokens: #{
		print(groups[g]);
		ind = 1;
		for j in tokens[g]: #{
#			print('\t'*ind, j[0] + '#' + str(j[1]) + '->' + str(j[2]));
			print('%s%s#%d->%d' % ('\t'*ind, j[0], j[1], j[2]));
			ind += 1;
		#}
	#} 

	print('');
#}

buffer = '';
for line in sys.stdin.readlines(): #{

	if line.strip() == '': #{
		kasitella(buffer);
		buffer = '';
	#}	

	buffer += line;
#}
