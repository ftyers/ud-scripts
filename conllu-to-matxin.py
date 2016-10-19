#!/usr/bin/env python3

#    1	Радианның	радиан	_	n	gen	4	nmod:poss	_	_
#    2-3	басқа да	_	_	_	_	_	_	_	_
#    2	_	басқа	_	adj	_	4	amod	_	_
#    3	_	да	_	postadv	_	2	advmod	_	_
#    4	бірліктермен	бірлік	_	n	pl|ins	5	nmod	_	_
#    5	байланысы	байланыс	_	n	px3sp|nom	0	root	_	_
#    6	.	.	_	sent	_	5	punct	_	_
#    

#    <corpus>
#    <SENTENCE ord='1' alloc='0'>
#    <NODE ord='5' alloc='32' form='байланысы' lem='байланыс' mi='n|px3sp|nom' si='root'>
#      <NODE ord='4' alloc='19' form='бірліктермен' lem='бірлік' mi='n|pl|ins' si='nmod'>
#        <NODE ord='1' alloc='0' form='Радианның' lem='радиан' mi='n|gen' si='nmod:poss'/> 
#        <NODE ord='2' alloc='9' form='' lem='басқа' mi='adj' si='amod'> 
#          <NODE ord='3' alloc='14' form='' lem='да' mi='postadv' si='advmod'/> 
#        </NODE>
#      </NODE>
#      <NODE ord='6' alloc='41' form='.' lem='.' mi='sent' si='punct'/>
#    </NODE>
#    </SENTENCE>

import sys ;

capcalera = """<?xml version='1.0' encoding='UTF-8' ?>
<corpus>
""" ; 

print(capcalera);
scount = 0;
lcount = 0;
ccount = 0;

deps = {}; 
nodes = {};

def escape(s): #{
	o = s;
	o = o.replace('"', '&#34;');
	o = o.replace("'", '&quot;');
	o = o.replace("&", '&amp;');
	return o;
#}

def proc(depth, nodes, deps, node): #{
	depth = depth + 1;
	if node != 0: #{
		form = escape(nodes[node][1]);
		lem = escape(nodes[node][2]);
		mi = nodes[node][4] + '|' + nodes[node][5];
		mi = mi.replace('|_', '').replace('<', '[').replace('>', ']');
		si = nodes[node][7].replace('>', '→').replace('<', '←');
		if node in deps and len(deps[node]) > 0: #{
			print(' ' * (2 * depth), '<NODE ord="%d" alloc="%d" form="%s" lem="%s" mi="%s" si="%s">' % (node, 0, form, lem, mi, si) );
		else: #{
			print(' ' * (2 * depth), '<NODE ord="%d" alloc="%d" form="%s" lem="%s" mi="%s" si="%s"/>' % (node, 0, form, lem, mi, si) );
		#}
	#}
	if node in deps: #{
		for n in deps[node]: #{
			proc(depth, nodes, deps, n);
		#}
	else: #{
		return;
	#}
	if node != 0: #{
		print(' ' * (2 * depth), '</NODE>');
	#}
	depth = depth - 1;
	return ;
#}
open = 0;
ord = 0;
for line in sys.stdin.readlines(): #{
	line = line.strip('\n');
	if line.count('# ord:') > 0: #{
		ord = int(line.split('ord:')[1].strip().split(' ')[0].strip());
	elif line == '\n': #{
		ord = 0;
	#}
	if line.count('\t') > 1: #{
		row = line.split('\t');
		if row[0] == '1': #{
			scount = scount + 1;
			print('<SENTENCE ord="%d" alloc="%d">' % (ord, ccount)) ;
			open = 1;
		#}
		if row[0].count('-') > 0: #{
			continue;
		#}
		cur = int(row[0]);
		cap = int(row[6]);
		if cap not in deps: #{
			deps[cap] = [];
		#}
		deps[cap].append(cur);
		nodes[cur] = row; 
	#}
	if line.strip() == '' and open == 1: #{
		proc(0, nodes, deps, 0); 
		print('</SENTENCE>');
		open = 0;
		deps = {};
		nodes = {};
	#}
#}

print('</corpus>');
