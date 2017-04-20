import libhfst;
import re
import sys;

###############################################################################

def plain_tekst(blokk): #{
	tekst = '';
	for line in blokk.split('\n'): #{
		row = line.split('\t');
		tekst = tekst + row[1] + ' ' ;	
	#}

	tekst = tekst.replace(' .', '.');
	tekst = tekst.replace(' ,', ',');

	return tekst.strip() ;
#}

def read_rules(sf): #{
	symbs = [];
	# Read in the replacement rules
	for line in sf.readlines(): #{
	
		line = line.strip('\n');
		row = line.split('\t')
		inn_lem = row[0].strip();
		inn_pos = row[1].strip();
		inn_feat = row[2].strip();
		out_lem = row[4].strip();
		out_pos = row[5].strip();
		out_feat = row[6].strip();
	
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
	
	
	#}
	# Order the rules by priority
	symbs.sort(); 
	
	return symbs;
#}

# List of rules in the format: 
# (priority, set([in, tags]), set([out, tags]))
# The priority is used to determine rule application order. Things that are more specific
# should come first, then backoff stuffs

def generic_convert(lema, xpos, feat, s): #{
	u_lema = lema;
	u_pos = '_';
	u_feat = '';

	msd = set([xpos] + feat);

#	print('>', lema, '|', xpos, '|', feat,'|||', msd, file=sys.stderr);

	for i in s: #{
		remainder = msd - i[1];
		intersect = msd.intersection(i[1]);
		if intersect == i[1]: #{
			#print('-', msd, intersect, remainder, i[2], '|||', u_pos, u_feat, file=sys.stderr);
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

	u_feat_s = list(set(u_feat.split('|')));
	u_feat_s.sort(key=str.lower);
	u_feat = '|'.join(u_feat_s);


	if u_feat == '': #{
		u_feat = '_';
	#}

	return (u_lema, u_pos, u_feat);
#}

def apertium_convert(analyses, s): #{
	retval = [];
	for analysis in analyses: #{

		loca = analysis[0].replace('><','|').replace('<','|').replace('>','').replace('@_EPSILON_SYMBOL_@', '');
		if '+' in loca: #{
			# Do something better here
			loca = loca.split('+')[0]; 
		#}
		lema = loca.split('|')[0];
		pos = loca.split('|')[1];
		feats = loca.split('|')[2:]
		#print(lema, file=sys.stderr);
		#print(pos, file=sys.stderr);
		#print(feats, file=sys.stderr);
		(u_lema, u_pos, u_feat) = generic_convert(lema, pos, feats, s);
		retval.append((u_lema, u_pos, u_feat));
	#}

	return retval;
#}

def best_analysis(lema, pos, sparse, analyses): #{
	maxoverlap = 0;
	best_analysis = ();
	for analysis in analyses: #{
		set_s = set([lema, pos] + sparse.split('|'));
		set_a = set([analysis[0], analysis[1]] + analysis[2].split('|'));
		
		intersect = set_a.intersection(set_s);
		if len(intersect) >= maxoverlap: #{
			maxoverlap = len(intersect);
			best_analysis = analysis;
		#}
		
	#}
	#print(maxoverlap, best_analysis, file=sys.stderr);
	if maxoverlap > 0: #{
		return best_analysis;
	else: #{
		return ();
	#}
#}


###############################################################################

if len(sys.argv) < 3: #{
	print('conllu-morph.py <fst> <tsv>');
	sys.exit(-1);
#}


istr = libhfst.HfstInputStream(sys.argv[1]);
morf = istr.read();
#morf.remove_epsilons();

af = open(sys.argv[2]);
apertium_symbs = read_rules(af);

#print(apertium_symbs);

unknown = 0;
known = 0;

for blokk in sys.stdin.read().split('\n\n'): #{
	if blokk.strip() == '': #{
		continue;
	#}
	tekst = plain_tekst(blokk);
#	print('# text = %s' % (tekst));
	for line in blokk.split('\n'): #{
		row = line.split('\t');
		morfres = [];

		morfres = morfres + list(morf.lookup(row[1].lower()));
		morfres = morfres + list(morf.lookup(row[1].title()));
		morfres = morfres + list(morf.lookup(row[1]));

		retres = apertium_convert(morfres, apertium_symbs);
		best = best_analysis(row[2], row[3], row[5], retres);
		if best != (): #{
			row[2] = best[0];
			row[3] = best[1];
			row[5] = best[2];
			known += 1;
		else: #{
			if row[9] == '_': #{
				row[9] = 'Morf=Unknown';
			else: #{
				row[9] = row[9] + '|Morf=Unknown';
			#}
			unknown += 1;
		#}
		print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]));	
		#print(line, best,morfres, retres, file=sys.stderr);
	#}
	print('');
#}

print(unknown / (known+unknown) *100, file=sys.stderr)
