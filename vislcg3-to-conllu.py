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
			if tok in [',', '.', ':', ';', '!', '?'] or first: #{
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

	return o ;
#}

def trykk(buffer, tokcount): #{
	noSpace = [',', ':', '.', ';', '!', '?'];
	if buffer.strip() == '': #{
		return tokcount;
	#}
	llong = buffer.count('\n') - 2;
	tokcount = tokcount + 1; 
	#print('!!!',tokcount,'!!!', buffer,'=====',file=sys.stderr);
	index = '';
	if llong > 0: #{
		index = str(tokcount) + '-' + str(tokcount+llong);
	else: #{
		index = str(tokcount);
	#}
	buffer = buffer.split('\n');
	ord = rword.findall(buffer[0])[0].strip(); #.replace(' ', '·');
	if llong == 0: #{
		lem = rbase.findall(buffer[1])[0]; #.replace(' ', '·');
		categs = rcateg.findall(buffer[1][buffer[1].rfind('"'):]);
		mor = rparent.findall(buffer[1])[0];
		etiqueta = rfunc.findall(buffer[1]);
		if not etiqueta: #{
			etiqueta = 'X';	
		else: #{
			etiqueta = etiqueta[0].strip();
		#}
		misc = '';
#		if ord in noSpace: #{
#			misc = 'SpaceAfter=No';
#		#}
		misc = misc + '|'.join(rmisc.findall(buffer[1])).replace('>', '').replace('<', '');
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
		ord_part = ord.split(' ');
		ord_len = len(ord_part);
		ord_idx = 0;
		n_toks = len(buffer[1:-1]);
#		print('!!!', ord_part, ord_len, ord_idx, n_toks, file=sys.stderr);
		for llinia in buffer[1:]: #{
			if llinia == '': continue;
			lem = rbase.findall(llinia)[0];	
			categs = rcateg.findall(llinia);	
			mor = rparent.findall(llinia)[0];
			etiqueta = rfunc.findall(llinia)[0].strip();
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
			else: #{
				M = LCS(ord.lower(), lem);
				lcsall = backTrackAll(M, ord.lower(), lem, len(ord), len(lem));
#				print(M, lcsall, file=sys.stderr)
				sur = list(lcsall)[0];
			#}
			if sur == '': #{
				sur = '_';
			#}
			print('%d\t%s\t%s\t_\t%s\t%s\t%s\t%s\t_\t%s' % (nindex,sur,lem, pos, msd, mor, etiqueta, misc));	
			nindex = nindex + 1;
		#}
	#}
	return tokcount+llong;
#}

def kasitella(blokk): #{
	buffer = ''
	tokcount = 0;
	for line in blokk.split('\n'): #{
		#print('X', line, file=sys.stderr)
	
		if line and line[0] == ';': #{
			continue;
		#}
	
		if line.strip() == '': #{
			#tokcount = tokcount + 1; 
			tokcount = trykk(buffer, tokcount);
			buffer = '';
			#tokcount = 0;
			#print('');
			continue;
		#}	
	
		if line[0] == '"' and line[1] == '<' and buffer != '': #{
			tokcount = trykk(buffer, tokcount);
			buffer = '';
			buffer = buffer + line + '\n';
			continue;
		#}
	
		if line.strip()[0] == '"': #{
			buffer = buffer + line + '\n';	
		#}
	#}
	if buffer != '': #{
		tokcount = trykk(buffer, tokcount);
	#}
	return tokcount;
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
			print('# text = %s' % tekst(blokk));
			complete = complete + 1;
			cleantokens = cleantokens + kasitella(blokk);
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
		print('# text = %s' % tekst(blokk));
		cleantokens = cleantokens + kasitella(blokk);	
		print('');
	#}
#}
print('')
print(complete,'/',sentcount,file=sys.stderr);
print(cleantokens, file=sys.stderr);
