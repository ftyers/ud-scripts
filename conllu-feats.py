import sys, collections;

symbs = [];

def convert(lema, xpos, feat, s): #{
	u_lema = lema;
	u_pos = '_';
	u_feat = '';

	msd = set([xpos] + feat);

	print('>', msd, file=sys.stderr);

	for i in s: #{
		remainder = msd - i[1];
		intersect = msd.intersection(i[1]);
		if intersect == i[1]: #{
			print('-', msd, intersect, remainder, i[2], '|||', u_pos, u_feat, file=sys.stderr);
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

	return (u_lema, u_pos, u_feat);
#}

sf = open(sys.argv[1]);

for line in sf.readlines(): #{

	line = line.strip('\n');
	row = line.split('\t')
	inn_lem = row[0];
	inn_pos = row[1];
	inn_feat = row[2];
	out_lem = row[3];
	out_pos = row[4];
	out_feat = row[5];

	nivell = -1;
	inn = set();
	if inn_pos != '_' and inn_feat != '_': #{
		inn = set([inn_pos] + inn_feat.split('|'));	
		nivell = 1;
	elif inn_pos == '_' and inn_feat != '_': #{
		inn = set(inn_feat.split('|'));	
		nivell = 2;
	elif inn_pos != '_' and inn_feat == '_': #{
		inn = set([inn_pos]);	
		nivell = 2;
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
symbs.sort();

for line in sys.stdin.readlines(): #{

	if line.count('\t') == 9: #{
		row = line.strip('\n').split('\t');
		#3	vuosttalda	vuosttaldit	_	V	TV|Ind|Prs|Sg3	0	FMV	_	_
		lema = row[2];
		xpos = row[4];
		feat = row[5].split('|');
		misc = lema + '|' + xpos + '|' + '|'.join(feat).replace('_', '');

		(u_lema, u_pos, u_feat) = convert(lema, xpos, feat, symbs);

		print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (row[0], row[1], u_lema, u_pos ,xpos, u_feat,row[6], row[7], row[8], misc))
	else: #{
		sys.stdout.write(line);
	#}
#}
