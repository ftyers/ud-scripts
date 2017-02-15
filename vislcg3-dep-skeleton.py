import sys;
count = 0;
buffer = '';

def kasitella(buf, count): #{
	n_anal = 0;
	n_tab = 0;
	tag = 'x';
	if buf.count('\t\t') > 0: #{
		print(buf);
		return;
	else: #{
		for line in buf.split('\n'): #{
			if len(line) == 0: #{
				continue;
			#}
			if line[0] == '"': #{
				print(line);
				tag = 'x';
				count = count + 1;
			#}
			if line[0] == '\t': #{
				if line.count(' det'): #{ 
					tag = 'det';
				#}
				if line.count(' cnjcoo'): #{ 
					tag = 'cc';
				#}
				if line.count(' cop '): #{ 
					tag = 'cop';
				#}
				if line.count(' vaux '): #{ 
					tag = 'aux';
				#}
				if line.count(' adv'): #{ 
					tag = 'advmod';
				#}
				if line.count(' post'): #{ 
					tag = 'case';
				#}
				if line.count(' loc attr'): #{ 
					tag = 'amod';
				#}
				if line.count(' n ') and line.count(' acc'): #{ 
					tag = 'obj';
				#}
				if line.count(' sent') or line.count(' guio') or line.count(' cm') or line.count(' lquot') or line.count(' rquot'): #{ 
					tag = 'punct';
				#}
				print('%s @%s #%d->' % (line, tag, count));
				tag = 'x';
			#}
		#}
	#}
#}

for line in sys.stdin.readlines(): #{
	if line.strip() == '': #{
		kasitella(buffer, count);
		print('');
		count = 0;
		buffer = '';
		continue;
	#}

	buffer = buffer + line;
#}
