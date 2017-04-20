import sys;

def proc_tekst(blokk): #{
	o = '' ;

	first = True;
	for tok in blokk.split(' '): #{
		if tok in [',', '.', ':', ';', '!', '?', '...'] or first: #{
			o = o + tok;
		else: #{
			o = o + ' ' + tok;
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

idx = 0;
prefiks = "undefined";
if len(sys.argv) >= 1: #{
	prefiks = sys.argv[1]
#}

for blokk in sys.stdin.read().split('\n\n'): #{

	sent_id = '';
	b = '';
	for line in blokk.split('\n'): #{
		if line.strip() == '': #{
			break;
		#}
		if line[0] == '#': #{
			if line.count('sent_id') > 0: #{
				sent_id = line.strip();
			#}
			continue;			
		#}
		row = line.split('\t');
		if '.' in row[0] or '-' in row[0]: #{
			continue;
		#}	
		if b == '': #{
			b = row[1];
		else: #{
			b = b + ' ' + row[1];
		#}
	#}
	
	tekst = proc_tekst(b);
	
	
	if blokk.strip() != '': #{
		if sent_id == '': #{
			print('# sent_id = %s::%d' % (prefiks, idx));
		else: #{
			print(sent_id);
		#}
		print('# text = %s' % (tekst));
	#}
	for line in blokk.split('\n'): #{
		if line.strip() == '': #{
			break;
		#}
		print(line);
	#}
	if blokk.strip() != '':	 #{
		print('');	
	#}
	idx += 1
#}
