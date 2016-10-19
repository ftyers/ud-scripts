#!/usr/bin/env python3

import sys; 
import xml.etree.ElementTree as ET

typ = "ud";
if len(sys.argv) > 1: #{
	typ = "gt"
#}

buf = ''
for line in sys.stdin.readlines(): #{
	buf = buf + line;
#}

root = ET.fromstring(buf);

class Globals: #{
	NODES = {};
#}

def proc_node(depth, node, lastnode): #{
	depth = depth + 1;
#	print(Globals.NODES, file=sys.stderr)
#	curnode = str(int(node.attrib['ord']) + 1);
	if 'ord' not in node.attrib: #{
		print(Globals.NODES, file=sys.stderr);
		print('ERROR: lastnode=', lastnode, file=sys.stderr);
	#}
	curnode = int(node.attrib['ord']) + 1;
#	print('! %d || cur: %s || last: %s' % (depth, curnode, lastnode), node.tag, file=sys.stderr);
	if node.tag == 'NODE': #{
		form = '-';
		lem = '-';
		mi = '-';
		si = '-';
		ord = '-';
		if 'form' in node.attrib: #{
			form = node.attrib['form'];
		#}
		if 'ord' in node.attrib: #{
			ord = int(node.attrib['ord']);
		#}
		if 'lem' in node.attrib: #{
			lem = node.attrib['lem'];
		#}
		if 'mi' in node.attrib: #{
			mi = node.attrib['mi'];
		#}
		if 'si' in node.attrib: #{
			si = node.attrib['si'];
		#}
		pos = mi;
		if '|' in mi: #{
			pos = mi.split('|')[0]
		#}
		#      1    2  3   4   5   6   7   8   9   10  #  1    2     3     4   5    6  7         8 
		Globals.NODES[ord] = (ord, form, lem, '_',pos, '_',lastnode, si, '_', mi);
	#}

	nodes = node.findall('NODE');
	
	for d in nodes: #{
		proc_node(depth, d, ord);
	#}
#}

insent = 0;
validsent = 0;
for sent in root.findall(".//SENTENCE"): #{
	insent = insent + 1;	
	heads = sent.findall("./NODE");
	if len(heads) == 0: #{
		print('SENTENCE', sent.attrib['ord'], 'has no head.', file=sys.stderr)
		continue;
	elif len(heads) > 1: #{
		print('SENTENCE', sent.attrib['ord'], 'has multiple heads.', file=sys.stderr)
		continue;
	#}	
	head = heads[0]
#	print(head, head.attrib['lem'], file=sys.stderr);
	proc_node(0, head, '0');
	kk = list(Globals.NODES.keys());
	kk.sort();
	last = kk[-1];
	if len(kk) != last: #{
		print('SENTENCE', sent.attrib['ord'], 'is missing nodes.', kk, file=sys.stderr)
		continue
	#}
	print('# ord: %s' % (sent.attrib['ord']));
	for node in kk: #{
		#1    2     3    4     5    6   7     8    9        10
		(id, form, lem, upos, xpos, mi, head, dep, deprels, misc) = Globals.NODES[node];
		if typ == "ud":
			print('%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (id, form, lem, '_',xpos, '_',head, dep, '_', misc))
		else:
			misc = misc.replace(xpos+'|', '', 1);
			if misc == xpos: #{
				misc = '_';
			#}
			print('%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (id, form, lem, '_',xpos, misc,head, dep, '_', '_'))
		#}
		
	#}
	Globals.NODES = {};
	validsent = validsent + 1;
	print('');
#}

print(validsent,'/',insent, file=sys.stderr);
