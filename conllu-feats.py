import sys, collections;

# List of rules in the format: 
# (priority, set([in, tags]), set([out, tags]))
# The priority is used to determine rule application order. Things that are more specific
# should come first, then backoff stuffs
symbs = [];

def convert(lema, xpos, feat, dep, s): #{
	u_lema = lema;
	u_pos = '_';
	u_feat = '';
	u_dep = dep;

	msd = set([xpos] + feat + [dep]);

	print('>', msd, file=sys.stderr);

	for i in s: #{
		remainder = msd - i[1];
		intersect = msd.intersection(i[1]);
		if intersect == i[1]: #{
			print('-', msd, intersect, remainder, i[2], '|||', u_pos, u_feat, u_dep, file=sys.stderr);
			for j in list(i[2]): #{
				if j == j.upper(): #{
					u_pos = j;
				else: #{
					if u_feat == '': #{
						u_feat = j
					else: #{
						u_feat = u_feat + '|' + j
					#}
				#}
			#}
			msd = remainder;
		#}
	#}

	if u_feat == '': #{
		u_feat = '_';
	#}

	return (u_lema, u_pos, u_feat, u_dep);
#}

sf = open(sys.argv[1]);

# Read in the replacement rules
for line in sf.readlines(): #{

	line = line.strip('\n');
	row = line.split('\t')
	inn_lem = row[0];
	inn_pos = row[1];
	inn_feat = row[2];
	inn_dep = row[3];
	out_lem = row[4];
	out_pos = row[5];
	out_feat = row[6];
	out_dep = row[7];

	nivell = -1.0;
	inn = set();
	if inn_pos != '_' and inn_feat != '_' and inn_dep != '_': #{
		inn = set([inn_pos] + inn_feat.split('|') + [inn_dep]);	
		nivell = 1.0;
	elif inn_pos != '_' and inn_dep != '_' and inn_feat == '_': #{
		inn = set([inn_pos] + [inn_dep]);	
		nivell = 2.0;
	elif inn_pos != '_' and inn_feat != '_': #{
		#print('#', 1.0/(inn_feat.count('|')+1.0), row);
		inn = set([inn_pos] + inn_feat.split('|'));	
		nivell = 3.0 + (1.0/(inn_feat.count('|')+1.0));
	elif inn_pos == '_' and inn_feat != '_': #{
		inn = set(inn_feat.split('|'));	
		nivell = 5.0;
	elif inn_pos != '_' and inn_feat == '_': #{
		inn = set([inn_pos]);	
		nivell = 5.0;
	#}

	out = set();
	if out_pos != '_' and out_feat != '_': #{
		out = set([out_pos] + out_feat.split('|'));	
	elif out_pos == '_' and out_feat != '_': #{
		out = set(out_feat.split('|'));	
	elif out_pos != '_' and out_feat == '_': #{
		out = set([out_pos]);	
	#}


	rule = (nivell, inn, out);

	symbs.append(rule)
		
	print(nivell, inn, out, file=sys.stderr);
#}
# Order the rules by priority
symbs.sort(); 

# Process a CoNLL-U file from stdin
for line in sys.stdin.readlines(): #{

	if line.count('\t') == 9: #{
		row = line.strip('\n').split('\t');
		if row[0].count('-') > 0: #{
			sys.stdout.write(line);
			continue;
		#}

		#3	vuosttalda	vuosttaldit	_	V	TV|Ind|Prs|Sg3	0	FMV	_	_
		lema = row[2];
		xpos = row[4];
		feat = row[5].split('|');
		udep = row[7];
		misc = row[9];
		if misc != '_': #{
			misc = row[9].strip() + '|' + lema + '|' + xpos + '|' + '|'.join(feat).replace('_', '');
		#}
		misc = misc.strip('|');

		(u_lema, u_pos, u_feat, u_dep) = convert(lema, xpos, feat, udep, symbs);
		u_feat_s = list(set(u_feat.split('|')));
		u_feat_s.sort(key=str.lower);
		u_feat = '|'.join(u_feat_s);

		print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (row[0], row[1], u_lema, u_pos ,xpos, u_feat,row[6], row[7], row[8], misc))
	else: #{
		sys.stdout.write(line);
	#}
#}
