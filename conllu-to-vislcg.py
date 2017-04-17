import sys ;

for line in sys.stdin.readlines(): #{
	if line.strip() == '': #{
		sys.stdout.write(line);
		continue;
	#}
	if line[0] == '#': #{
		sys.stdout.write(line);
		continue;
	#}
	row = line.split('\t');
	if len(row) != 10: #{
		print('ERR', row);
		break;
	#}
	id = row[0]
	sur = row[1]	
	lem = row[2]	
	upos = row[3]	
	xpos = row[4]	
	feats = row[5]	
	head = row[6]	
	deprel = row[7]	
	deps = row[8]	
	misc = row[9]	

	print('"<%s>"' % (sur));
	print('\t"%s" %s %s @%s #%s->%s' % (lem, upos, ' '.join(feats.split('|')), deprel, id, head));
#}
