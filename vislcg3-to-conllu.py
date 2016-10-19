#!/usr/bin/env python3

import sys, re;

rword = re.compile('"<(.+)>"');
rbase = re.compile('"(.+)"');
rcateg = re.compile(' ([_\w0-9\/\*]+)');
rnode = re.compile('#([0-9]+)->');
rparent = re.compile('->([0-9]+)');
rfunc = re.compile('@(.+) #');
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

def trykk(buffer, tokcount): #{
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
	ord = rword.findall(buffer[0])[0];
	if llong == 0: #{
		lem = rbase.findall(buffer[1])[0];
		categs = rcateg.findall(buffer[1][buffer[1].rfind('"'):]);
		mor = rparent.findall(buffer[1])[0];
		etiqueta = rfunc.findall(buffer[1])[0];
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
		print('%s\t%s\t%s\t_\t%s\t%s\t%s\t%s\t_\t_' % (index,ord,lem, pos, msd, mor, etiqueta));	
	else: #{
		print('%s\t%s\t_\t_\t_\t_\t_\t_\t_\t_' % (index,ord));	
		nindex = tokcount;
		for llinia in buffer[1:]: #{
			if llinia == '': continue;
			lem = rbase.findall(llinia)[0];	
			categs = rcateg.findall(llinia);	
			mor = rparent.findall(llinia)[0];
			etiqueta = rfunc.findall(llinia)[0];
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
			
			print('%d\t_\t%s\t_\t%s\t%s\t%s\t%s\t_\t_' % (nindex,lem, pos, msd, mor, etiqueta));	
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
sentcount = 0;
complete = 0;
cleantokens = 0;
ord = 1;
for line in sys.stdin.readlines(): #{
		
	if line.strip() == '' and blokk != '': #{
		print('# ord: %d  ||| %d/%d' % (ord, len(rdep.findall(blokk)), blokk.count('\t"')));
		if blokk.count('\t"') == len(rdep.findall(blokk)): #{
			complete = complete + 1;
			blokk = blokk + line;
			cleantokens = cleantokens + kasitella(blokk);	
			print('');
		#}
		#print(sentcount,file=sys.stderr);
		blokk = '';
		sentcount = sentcount + 1;
		ord = ord + 1;
	#}
	
	blokk = blokk + line;
#}
if blokk != '': #{
	print('# ord: %d ||| %d/%d' % (ord, len(rdep.findall(blokk)), blokk.count('\t"')));
	if blokk.count('\t"') == len(rdep.findall(blokk)): #{
		blokk = blokk + line;
		cleantokens = cleantokens + kasitella(blokk);	
		print('');
	#}
#}
print('')
print(complete,'/',sentcount,file=sys.stderr);
print(cleantokens, file=sys.stderr);
