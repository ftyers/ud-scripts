# IN:
#	"<Сөздерін>"
#	        "сөз" n pl px3sp acc @obj #1->4
#	"<екеуі де>"
#	        "екеу" num coll subst px3sp nom @nsubj #2->4
#	                "да" postadv @advmod #3->2
#	"<қабыл алды>"
#	        "қабыл ал" v tv ifi p3 sg @root #4->0
#	"<.>"
#	        "." sent @punct #5->4
# OUT:
#	"<Сөздерін>"
#	        "сөз" n pl px3sp acc @obj #1->5
#	"<екеуі де>"
#	        "екеу" num coll subst px3sp nom @nsubj #2->5
#	                "да" postadv @advmod #3->2
#	"<қабыл>"
#	        "қабыл" x @compound #4->5
#	"<алды>"
#	        "ал" v tv ifi p3 sg @root #5->0
#	"<.>"
#	        "." sent @punct #6->5


import sys;

# If the token has space in lemma, and surface form and the number of analysis lines is 1
# split the lemma and the surface form into two tokens.

# increment head indexes >= cur_idx by 1
# increment token indexes >= cur_idx by 1

def break_token(t, idx, idmax): #{
	
#('"<Сөздерін>"\n', '\t"сөз" n pl px3sp acc @obj ')
	surf = t[0].strip()[2:-2].split(' ');
	lem = t[1].split('"')[1].split(' ');
	tags = '';
	if idx == idmax: #{
		tags = ' '.join(t[1].split('"')[2:]);
	else: #{
		tags = ' x @dep ';
	#}

	return ('"<' + surf[idx] + '>"\n', '\t"'+lem[idx]+'"' + tags);
#}

def kasitella(heads, tokens, cur_sur, max_tok): #{
	
	cur_tok = 0;
	while cur_tok <= max_tok: #{
		new_tokens = {};
		new_heads = {};
		for i in tokens.keys(): #{
			lem = '"'.join(tokens[i][1].split('"')[0:2]).strip();
			if tokens[i][0].strip().count(' ') == lem.count(' ') and lem.count(' ') > 0: #{
				print('¶ [',cur_tok,max_tok,'] ¶', i, '|||', tokens[i], heads[i], file=sys.stderr)
				for j in tokens.keys(): #{
					if j == i: #{ 
						local_max = lem.count(' ');
						for k in range(0, local_max+1): #{
							new_tokens[j+k] = break_token(tokens[j], k, local_max);
						#}
						for k in range(0, local_max): #{
							new_heads[j+k] = j+local_max;	
						#}
						if heads[j] >= i: #{
							new_heads[j+local_max] = heads[j]+local_max;
						else: #{
							new_heads[j+local_max] = heads[j];
						#}
						print('@', j, i, heads[j], lem, file=sys.stderr);
					elif j > i: #{
						new_tokens[j+1] = tokens[j];
						if heads[j] >= i: #{
							new_heads[j+1] = heads[j]+1;
						else: #{
							new_heads[j+1] = heads[j];
						#}
						print('!', j, i, heads[j], new_heads[j+1], lem, file=sys.stderr);
					else: #{
						new_tokens[j] = tokens[j];
						if heads[j] >= i: #{
							new_heads[j] = heads[j]+1;
						else: #{
							new_heads[j] = heads[j];
						#}
						print('%', j, i, heads[j], lem, file=sys.stderr);
					#}
				#}
				print('===', new_tokens, file=sys.stderr);
				print('===', new_heads, file=sys.stderr);
				cur_tok = i;
				break;
			else: #{
				print('[',cur_tok,max_tok,'] >', tokens, file=sys.stderr);
				print('§ [',cur_tok,max_tok,'] § >', i, '|||', tokens[i], '|||', file=sys.stderr);
				new_tokens[i] = tokens[i];
				new_heads[i] = heads[i]
				cur_tok = i+1;
				#break;
			#}
		#}
		print(cur_tok, '////////////////////////////////////////////////////////////////////////', file=sys.stderr);
		tokens = new_tokens;
		heads = new_heads;
	#}	

	for i in tokens.keys(): #{
	#	print(i, tokens[i], heads[i])
		print(tokens[i][0] + tokens[i][1] + '#' + str(i) + '->' + str(heads[i]));
	#}
#}

heads = {};
tokens = {};
cur_sur = '';
max_tok = 0;
for line in sys.stdin.readlines(): #{

	if line.strip() == '': #{
		print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$', file=sys.stderr);
		kasitella(heads, tokens, cur_sur, max_tok)
		heads = {};
		tokens = {};
		cur_sur = '';
		print('');
		continue;
	#}

	if line[0] == '"': #{
		cur_sur = line;	
	elif line[0] == '\t': #{
		row = line.split('#');
		anal = row[0];
		(d, h) = row[1].replace('->', '\t').split('\t');
		head = int(h);
		toki = int(d);
		heads[toki] = head;
		tokens[toki] = (cur_sur, anal);
		cur_sur = '';
		max_tok = toki;
	else: #{
		print('Invalid:', file=sys.stderr);
	#}
#}
