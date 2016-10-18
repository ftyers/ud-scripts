
import sys;

# Input:
# "<Радианның>"
#	"радиан" n gen
# "<басқа да>"
# 	"басқа" adj subst nom
# 		"е" cop aor p3 sg
# 			"да" postadv
# 	"бас" n dat
# 		"да" cnjcoo
# "<бірліктермен>"
# 	"бірлік" n pl ins
# "<байланысы>"
# 	"байланыс" n px3sp nom
# 	"байланыс" n px3sp nom
# 		"е" cop aor p3 pl
# 	"байланыс" n px3sp nom
# 		"е" cop aor p3 sg
# "<.>"
# 	"." sent

# Output:
# 1	Радианның	радиан	_	n	gen
# 2-4	басқа да	_	_	_	_
# 2	басқа да	басқа	_	adj	subst|nom
# 3	басқа да	е	_	cop	aor|p3|sg
# 4	басқа да	да	_	postadv	_
# 2	басқа да	бас	_	n	dat
# 3	басқа да	да	_	cnjcoo	_
# 5	бірліктермен	бірлік	_	n	pl|ins
# 6-7	байланысы	_	_	_	_
# 6	байланысы	байланыс	_	n	px3sp|nom
# 6	байланысы	байланыс	_	n	px3sp|nom
# 7	байланысы	е	_	cop	aor|p3|pl
# 6	байланысы	байланыс	_	n	px3sp|nom
# 7	байланысы	е	_	cop	aor|p3|sg
# 8	.	.	_	sent	_

sentid = 1;
tokid = 1;

def surf(s): #{
	return s.split('<')[1].split('>')[0];
#}

def lemma(s): #{
	quot = s.count('"'); 
	lem = '';
	if quot == 2: #{
		lem = s.strip().split('"')[1];
	elif quot == 3: #{
		return '"';
	else: #{
		print('!!! WTF', s, file=sys.stderr);
	#}
	return lem;
#}

def pos(s): #{
	quot = s.count('"'); 
	categ = '';
	if quot == 2: #{
		categ = s.strip().split('"')[2].strip().split(' ')[0];
	elif quot == 3: #{
		categ = s.strip().split('"')[3].strip().split(' ')[0];
	else: #{
		print('!!! WTF', s, file=sys.stderr);
	#}
	return categ;
#}

def feats(s): #{
	quot = s.count('"'); 
	morf = '';
	if quot == 2: #{
		morf = '|'.join(s.strip().split('"')[2].strip().split(' ')[1:]).strip('|');
	elif quot == 3: #{
		morf = '_';
	else: #{
		print('!!! WTF', s, file=sys.stderr);
	#}
	return morf ; 
#}

superf = '';
lema = '';
categ = '';
morf = '';

buf = '';

for line in sys.stdin.readlines(): #{
	# End of sentence
	if line.strip() == '': #{

		if buf != '': #{
			span = 0 ;
			# calculate the maximum indentation
			for linia in buf.split('\n'): #{
				span = max(span, linia.count('\t'));
			#}
			superf = surf(buf.split('\n')[0]);
			i = tokid  ;
			j = tokid + span ;
			if span == 1: #{
				linia = buf.split('\n')[1];
				lema = lemma(linia);
				if linia[2] == '*': #{
					categ = 'unk' ;
					morf = '_';
				else: #{
					categ = pos(linia);
					morf = feats(linia);	
				#}
				if morf == '': #{
					morf = '_';
				#}
				print('%d\t%s\t%s\t_\t%s\t%s' % (i, superf, lema, categ, morf));
			else: #{
				print('%d-%d\t%s\t_\t_\t_\t_' % (i, j-1, superf));
				k = i; 
				for linia in buf.split('\n')[1:]: #{
					if linia == '': #{
						continue;
					#}
					k = i + linia.count('\t') - 1;
					print('!!!', tokid, span, i, j, k, linia, file=sys.stderr);
					lema = lemma(linia);
					if linia[2] == '*': #{
						categ = 'unk' ;
						morf = '_';
					else: #{
						categ = pos(linia);
						morf = feats(linia);	
					#}
					if morf == '': #{
						morf = '_';
					#}

					print('%d\t%s\t%s\t_\t%s\t%s' % (k, superf, lema, categ, morf));	
				#}
			#}
				
			buf = '';
			tokid = j ;
		#}

		sentid = sentid + 1;
		print('');
		print('#', sentid);
		tokid = 1;
		continue;
	#}

	# We hit a new input token
	if line[0] == '"' and line[1] == '<': #{
		if buf != '': #{
			span = 0 ;
			# calculate the maximum indentation
			for linia in buf.split('\n'): #{
				span = max(span, linia.count('\t'));
			#}
			superf = surf(buf.split('\n')[0]);
			i = tokid  ;
			j = tokid + span ;
#			print('$$$ i=%d, j=%d, span=%d' % (i, j, span), buf, file=sys.stderr);
			if span == 1: #{
				#linia = buf.split('\n')[1];
				for linia in buf.split('\n')[1:-1]: #{	
#					print('###', linia, file=sys.stderr);
					lema = lemma(linia);
					if linia[2] == '*': #{
						categ = 'unk' ;
						morf = '_';
					else: #{
						categ = pos(linia);
						morf = feats(linia);	
					#}
	
					if morf == '': #{
						morf = '_';
					#}
					print('%d\t%s\t%s\t_\t%s\t%s' % (i, superf, lema, categ, morf));
				#}
			else: #{
				print('%d-%d\t%s\t_\t_\t_\t_' % (i, j-1, superf));
				k = i; 
				for linia in buf.split('\n')[1:]: #{
					if linia == '': #{
						continue;
					#}
					k = i + linia.count('\t') - 1;
#					print('!!!', tokid, span, i, j, k, linia, file=sys.stderr);
					lema = lemma(linia);
					if linia[2] == '*': #{
						categ = 'unk' ;
						morf = '_';
					else: #{
						categ = pos(linia);
						morf = feats(linia);	
					#}
					if morf == '': #{
						morf = '_';
					#}

					print('%d\t%s\t%s\t_\t%s\t%s' % (k, superf, lema, categ, morf));	
				#}
			#}
				
			buf = '';
			tokid = j ;
		#}
		buf = buf + line;
	else: #{
		buf = buf + line;
	#}
#}
if buf != '': #{
	span = 0 ;
	# calculate the maximum indentation
	for linia in buf.split('\n'): #{
		span = max(span, linia.count('\t'));
	#}
	superf = surf(buf.split('\n')[0]);
	i = tokid  ;
	j = tokid + span ;
	if span == 1: #{
		linia = buf.split('\n')[1];
		lema = lemma(linia);
		if linia[2] == '*': #{
			categ = 'unk' ;
			morf = '_';
		else: #{
			categ = pos(linia);
			morf = feats(linia);	
		#}

		if morf == '': #{
			morf = '_';
		#}
		print('%d\t%s\t%s\t_\t%s\t%s' % (i, superf, lema, categ, morf));
	else: #{
		print('%d-%d\t%s\t_\t_\t_\t_' % (i, j-1, superf));
		k = i; 
		for linia in buf.split('\n')[1:]: #{
			if linia == '': #{
				continue;
			#}
			k = i + linia.count('\t') - 1;
#					print('!!!', tokid, span, i, j, k, linia, file=sys.stderr);
			lema = lemma(linia);
			if linia[2] == '*': #{
				categ = 'unk' ;
				morf = '_';
			else: #{
				categ = pos(linia);
				morf = feats(linia);	
			#}
			if morf == '': #{
				morf = '_';
			#}

			print('%d\t%s\t%s\t_\t%s\t%s' % (k, superf, lema, categ, morf));	
		#}
	#}
		
	buf = '';
	tokid = j ;
#}

