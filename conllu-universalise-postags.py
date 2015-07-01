import sys;

bord = {};

for line in open(sys.argv[1]).readlines(): #{

	line = line.strip();
	row = line.split('\t');

	bord[row[0]] = row[1];
#}

for line in sys.stdin.readlines(): #{

	line = line.strip();

	if line == '': #{
		print(line);	
		continue;
	#}

	row = line.split('\t');
	
	if row[4] in bord: #{
		row[3] = bord[row[4]];
	#}	
	
	print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]));
#}
