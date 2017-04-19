import sys;

nlc = 0;
first = True;
for line in sys.stdin.readlines(): #{

	if line.strip() == '': #{
		nlc = nlc + 1;
	#}

	if line.strip() != '': #{
		nlc = 0;
	#}

	if line.strip() == '' and nlc > 1: #{
		first = False;
		continue;
	elif line.strip() == '' and first: #{
		first = False;
		continue;
	else: #{
		sys.stdout.write(line);
	#}
	first = False;
#}
