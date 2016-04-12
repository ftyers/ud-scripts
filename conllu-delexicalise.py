import sys;

for line in sys.stdin.readlines(): #{
	if line.count('\t') == 0: #{
		sys.stdout.write(line);
		continue;
	#}
	r = line.strip('\n').split('\t');

	if len(r) == 10: #{
		print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (r[0], '_', '_', r[3], r[4], r[5], r[6], r[7], r[8], r[9]));
	elif len(r) == 6: #{
		print('%s\t%s\t%s\t%s\t%s\t%s' % (r[0], '_', '_', r[3], r[4], r[5]));
	#}
#}

