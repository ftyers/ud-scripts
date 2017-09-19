#!/usr/bin/env python3

import sys, re;

rword = re.compile('"<(.+)>"');
rbase = re.compile('"(.+)"');
rcateg = re.compile(' ([_\w0-9\/\*]+)');
rnode = re.compile('#([0-9]+)->');
rparent = re.compile('->([0-9]+)');
rfunc = re.compile('@(.+) #');
rmisc = re.compile('(<[^ >]+>)');
rdep = re.compile('#[0-9]+->[0-9]+');

# Input:
#	"<Қала>"
#		"қала" n nom @nmod #1->2
#	"<халқы>"
#		"халық" n px3sp nom @subj #2->3
#	"<58,3%>"
#		"58,3" num percent nom @main #3->0
#			"е" cop aor p3 sg @cop #4->3
#	"<.>"
#		"." sent @punct #5->3
#	

# Output:
#	1	Қала	кала	_	n	nom	2	nmod	_	_
#	2	халқы	халық	_	n	px3sp|nom	3	nsubj	_	_
#	3-4	58,3%	_	_	_	_	_	_	_	_
#	3	58,3	58,3	_	num	percent|nom	0	root	_	_
#	4	_	е	_	cop	aor|p3|sg	3	cop	_	_
#	5	.	.	_	sent	_	3	punct	_	_

def LCS(X, Y): #{
	m = len(X)
	n = len(Y)
	# An (m+1) times (n+1) matrix
	C = [[0] * (n + 1) for _ in range(m + 1)]
	for i in range(1, m+1):
		for j in range(1, n+1):
			if X[i-1] == Y[j-1]: 
				C[i][j] = C[i-1][j-1] + 1
			else:
				C[i][j] = max(C[i][j-1], C[i-1][j])
	return C
#}

def backTrackAll(C, X, Y, i, j): #{
	if i == 0 or j == 0:
		return set([""])
	elif X[i-1] == Y[j-1]:
		return set([Z + X[i-1] for Z in backTrackAll(C, X, Y, i-1, j-1)])
	else:
		R = set()
		if C[i][j-1] >= C[i-1][j]:
			R.update(backTrackAll(C, X, Y, i, j-1))
		if C[i-1][j] >= C[i][j-1]:
			R.update(backTrackAll(C, X, Y, i-1, j))
		return R
#}

def tekst(blokk): #{
	o = '';
	#print('!!!', blokk, file=sys.stderr);
	first = True;
	for line in blokk.split('\n'): #{
		if len(line) == 0: #{
			continue;
		#}
		if line[0] == '"': #{
			tok = line.strip()[2:-2];
			if tok in [',', '.', ':', ';', '!', '?', '...'] or first: #{
				o = o + tok;
			else: #{
				o = o + ' ' + tok;
			#}
		#}
		first = False;
	#}

	# Hacks
	o = o.replace('( ', '(');
	o = o.replace(' )', ')');
	o = o.replace('« ', '«');
	o = o.replace(' »', '»');
	o = o.replace('“ ', '“');
	o = o.replace(' ”', '”');
	o = o.replace(' - ', '-');
	o = o.replace('!-', '! - ');
	o = o.replace(',-', ', - ');
	o = o.replace(':-', ': - ');
	o = o.replace('?-', '? - ');

	# " Осылай тұр! " дегендей екі иығынан басып қалды, бес-алты адымдай жерге барып тұра қалды.
	
	new_o = '';
	qc = 0;
	lastc = '';
	for c in o: #{
		if c == '"': #{
			qc = qc + 1;	
		#}
		if c == ' ' and qc % 2 == 1 and lastc == '"': #{
			continue;
		#}
		new_o += c;
		lastc = c;
	#}
	o = new_o;
	o = o.replace(' " ', '" ');
	o = o.replace(' ",', '",');

	return o ;
#}

def trykk(buffer, tokcount, charcount, t): #{
	newt = t + ' ' * tokcount;
	if buffer.strip() == '': #{
		return (tokcount, charcount);
	#}
	llong = buffer.count('\n') - 2;
	tokcount = tokcount + 1; 
	index = '';
	if llong > 0: #{
		index = str(tokcount) + '-' + str(tokcount+llong);
	else: #{
		index = str(tokcount);
	#}
	buffer = buffer.split('\n');
	ord = rword.findall(buffer[0])[0].strip(); 
	if ord.count(' ') > 0: #{
		charcount = charcount + len(ord) + ord.count(' ');
	else: #{
		charcount = charcount + len(ord) + 1;
	#}
#	print('!!!',tokcount,'!!!', charcount , '!!! "', newt[charcount-1] ,'" |' , t ,'!!!',  buffer,'=====',file=sys.stderr);
	if llong == 0: #{
		lems = rbase.findall(buffer[1]);
		lem = '@LEMMA@'
		if len(lems) > 0: #{
			lem = rbase.findall(buffer[1])[0]; 
		#}
		categs = rcateg.findall(buffer[1][buffer[1].rfind('"'):]);
		mor = rparent.findall(buffer[1])[0];
		etiqueta = rfunc.findall(buffer[1]);
		if not etiqueta: #{
			etiqueta = 'X';	
		else: #{
			etiqueta = etiqueta[0].strip();
		#}
		misc = '';
#		if len(t) > charcount and newt[charcount-1] != ' ': #{
#			misc = misc + 'SpaceAfter=No|';
#		#}
		misc = misc + '|'.join(rmisc.findall(buffer[1])).replace('>', '').replace('<', '');
		misc = misc.strip('|');
		if misc == '': #{
			misc = '_';
		#}
		pos = '_'
		if len(categs) > 0: #{
			pos = categs[0];
		#}
		msd = '_';
		if len(categs) > 1: #{
			msd = '';
			for i in categs[1:]: #{
				msd = msd + i.strip() + '|';
			#}
			msd = msd.strip('|');
		#}
		print('%s\t%s\t%s\t_\t%s\t%s\t%s\t%s\t_\t%s' % (index,ord,lem, pos, msd, mor, etiqueta,misc));	
	else: #{
		print('%s\t%s\t_\t_\t_\t_\t_\t_\t_\t_' % (index,ord));	
		nindex = tokcount;
#		ord_part = ord.split(' ');
		# FIXME: This is for in breton, e.g. P'edon, but will break if you have c'h 
		ord_part = re.split("[ '’]", ord); 
		if ord[0] == "'": #{
			ord_part[0] = "'";
		#}
		ord_len = len(ord_part);
		ord_idx = 0;
		n_toks = len(buffer[1:-1]);
#		print('!!!', ord_part, ord_len, ord_idx, n_toks, file=sys.stderr);
		prev_lem = '';
		for llinia in buffer[1:]: #{
			if llinia == '': continue;
			lem = rbase.findall(llinia)[0];	
			categs = rcateg.findall(llinia);	
			mor = rparent.findall(llinia)[0];
			etiqueta = rfunc.findall(llinia)[0].strip();
			misc = '';
#			if len(t) > charcount and newt[charcount-1] != ' ': #{
#				misc = misc + 'SpaceAfter=No|';
#			#}
			misc = '|'.join(rmisc.findall(llinia)).replace('>', '').replace('<', '');
			if misc == '': #{
				misc = '_';
			#}
			pos = '_'
			if len(categs) > 0: #{
				pos = categs[0];
			#}
			msd = '_';
			if len(categs) > 1: #{
				msd = '';
				for i in categs[1:]: #{
					msd = msd + i.strip() + '|';
				#}
				msd = msd.strip('|');
			#}
			sur = '_'
			if n_toks == ord_len: #{
				sur = ord_part[ord_idx];
				ord_idx += 1;
			elif len(lem) > 1: #{
				lcsall = '';
				if ord[0].isupper() and lem[0].isupper(): #{
					M = LCS(ord, lem);
					lcsall = backTrackAll(M, ord, lem, len(ord), len(lem));
				else: #{
					M = LCS(ord.lower(), lem);
					lcsall = backTrackAll(M, ord.lower(), lem, len(ord), len(lem));
				#}
#				print(M, lcsall,'|',prev_lem, file=sys.stderr)
#				sur = list(lcsall)[0];
			#}
#			print(sur, prev_lem, file=sys.stderr);
			if (sur == '' or sur == '_') and re.match('^'+prev_lem, ord): #{
				sur = re.sub('^'+prev_lem,'', ord, 1);
			#}
			if sur == '': #{
				sur = '_';
			#}
			print('%d\t%s\t%s\t_\t%s\t%s\t%s\t%s\t_\t%s' % (nindex,sur,lem, pos, msd, mor, etiqueta, misc));	
			nindex = nindex + 1;
			prev_lem = lem;
		#}
	#}
	return (tokcount+llong, charcount);
#}

def kasitella(blokk, t): #{
	buffer = ''
	tokcount = 0;
	charcount = 0;
	for line in blokk.split('\n'): #{
		#print('X', line, file=sys.stderr)
	
		if line and line[0] == ';': #{
			continue;
		#}
		if line and line[0] == '#': #{
			print(line.strip('\n'));
			continue;
		#}
	
		if line.strip() == '': #{
			(tc, cc) = trykk(buffer, tokcount, charcount, t);
			buffer = '';
			tokcount = tc;
			charcount = cc;
			#print('');
			continue;
		#}	
	
		if line[0] == '"' and line[1] == '<' and buffer != '': #{
			(tc, cc) = trykk(buffer, tokcount, charcount, t);
			buffer = '';
			tokcount = tc;
			charcount = cc;
			buffer = buffer + line + '\n';
			continue;
		#}
	
		if line.strip()[0] == '"': #{
			buffer = buffer + line + '\n';	
		#}
	#}
	if buffer != '': #{
		(tc, cc) = trykk(buffer, tokcount, charcount, t);
		tokcount = tc;
		charcount = cc;
		
	#}
	return (tokcount, charcount);
#}

blokk = '';
sentcount = 1;
linecount = 0;
complete = 0;
cleantokens = 0;
ord = 1;
prefiks = sys.argv[1].strip();
for line in sys.stdin.readlines(): #{
		
	if line.strip() == '' and blokk != '' and blokk != '\n': #{
#		print('# ord: %d  ||| %d/%d' % (ord, len(rdep.findall(blokk)), blokk.count('\t"')), file=sys.stderr);
		if blokk.count('\t"') == len(rdep.findall(blokk)): #{
			blokk = blokk + line;
			print('# sent_id = %s:%d:%d' % (prefiks,sentcount,(linecount-blokk.count('\n')+1)));
			t = tekst(blokk);
			if blokk.count('# text ') == 0: #{
				print('# text = %s' % (t));
			#}
			complete = complete + 1;
			(newtok, newchar) = kasitella(blokk, t);
			cleantokens = cleantokens + newtok;
			print('');
		#}
		#print(sentcount,file=sys.stderr);
		blokk = '';
		sentcount = sentcount + 1;
		ord = ord + 1;
	#}
	
	blokk = blokk + line;
	linecount = linecount + 1;
#}
if blokk != '' and blokk != '\n': #{
#	print('# ord: %d ||| %d/%d' % (ord, len(rdep.findall(blokk)), blokk.count('\t"')));
	if blokk.count('\t"') == len(rdep.findall(blokk)): #{
		blokk = blokk + line;
		print('# sent_id = %s:%d:%d' % (prefiks,sentcount,(linecount-blokk.count('\n')+1)));
		t = tekst(blokk);
		if blokk.count('# text ') == 0: #{
			print('# text = %s' % (t));
		#}
		(newtok, newchar) = kasitella(blokk, t);
		cleantokens = cleantokens + newtok;
		print('');
	#}
#}
print('')
print(complete,'/',sentcount,file=sys.stderr);
print(cleantokens, file=sys.stderr);
