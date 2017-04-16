import sys;

def e(s): #{
	return s.replace(' ', '·');
#}

def calc_spaceafter(a, b): #{
	
	if a.replace(' ', '') != b.replace(' ', ''): #{
		return {};
	#}
	
	idx = 0;
	ord = '';
	i = 0;
	j = 0;
	m = {};
	while True: #{
		if i >= len(a): break;
	
		if a[i] == ' ' and b[j] == ' ': #{
	#		print('%', idx, ord, i, j,'|||',e(a[i]),'|', e(b[i]));
	#		print('%d\t%s\t%s' % (idx, ord, '_'));
			m[idx] = '';
			ord = '';
			idx += 1;	
		if a[i] == b[j]: #{
	#		print('\t',idx, ord, i, j,'|||',e(a[i]),'|', e(b[i]));
			ord = ord + a[i];
			
		else: #{
			if b[j] == ' ': #{
				#print('%d\t%s\t%s' % (idx, ord, 'SpaceAfter=No'));
				m[idx] = 'SpaceAfter=No';
				ord = '';
				idx += 1;	
				j += 1;
				continue;
			else: 
				break;
			#}
		#}
	
		i += 1;
		j += 1;
	#}

	return m;
#}	

for blokk in sys.stdin.read().split('\n\n'): #{

	a = '';
	b = '';
	for line in blokk.split('\n'): #{
		if line.strip() == '': #{
			break;
		#}
		if line.count('# text = ') > 0: #{
			a = line.split('# text = ')[1].strip();
			continue;
		#}
		if line[0] == '#': #{
			continue;			
		#}
		row = line.split('\t');
		if b == '': #{
			b = row[1];
		else: #{
			b = b + ' ' + row[1];
		#}
	#}
	spaces = calc_spaceafter(a, b);
	
	for line in blokk.split('\n'): #{
		if line.strip() == '': #{
			break;
		#}
		if line[0] == '#': #{
			print(line);
			continue;
		#}
		row = line.split('\t');
		if '.' in row[0] or '-' in row[0]: #{
			print(line);
			continue;
		#}	
		idx = int(row[0]) - 1;

		if idx in spaces and spaces[idx] != '': #{
			if row[9] == '_': #{
				row[9] = 'SpaceAfter=No';
			else: #{
				row[9] += '|SpaceAfter=No';
			#}
			print('\t'.join(row));
		else: #{
			print(line);
		#}		
	#}
	if blokk.strip() != '':	 #{
		print('');	
	#}
#}

