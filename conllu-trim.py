import sys;

nl = 0

for line in sys.stdin.readlines(): #{

	if line[0] == '\n': #{
		nl = nl + 1;
	else: #{
		nl = 0;
	#}

	if nl > 1: #{
		continue;
	#}	

	sys.stdout.write(line);
#}
