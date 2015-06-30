import sys, re;

rword = re.compile('"<(.+)>"');
rbase = re.compile('"(.+)"');
rcateg = re.compile(' ([_A-Za-z0-9]+)');

toknum = 0;
buffer = '';
for line in sys.stdin.readlines(): #{
	if line.strip() == '': #{
		toknum = toknum + 1;
		if buffer != '': #{
#			toknum = toknum + 1;
			buffer = buffer.split('\n');
			ord = rword.findall(buffer[0])[0];
			lem = rbase.findall(buffer[1])[0];
			categs = rcateg.findall(buffer[1]);
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
			print('%d\t%s\t%s\t_\t%s\t%s' % (toknum, ord, lem, pos, msd));
#			print(toknum, buffer, file=sys.stderr);
		#}
		toknum = 0;
		buffer = '';
		print('');
	elif line[0] == '"': #{
		if buffer != '': #{
			toknum = toknum + 1;
			buffer = buffer.split('\n');
			ord = rword.findall(buffer[0])[0];
			lem = rbase.findall(buffer[1])[0];
			categs = rcateg.findall(buffer[1]);
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
			print('%d\t%s\t%s\t_\t%s\t%s' % (toknum, ord, lem, pos, msd));
#			print(toknum, buffer, file=sys.stderr);
		#}
		buffer = '';
		buffer = buffer + line;
	elif line[0] == '\t': #{
		buffer = buffer + line;
	#}
#}
