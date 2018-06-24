import sys 

ud_f = open(sys.argv[1])
ap_f = open(sys.argv[2])

def form(line):
	if line.count('^') == line.count('$') and line.count('^') > 0:
		if line[0] == '^': return line.split('^')[1].split('/')[0]		
		else: return line.split('/')[0].replace('^', '')
	elif line.count('\t') > 0:
		row = line.split('\t')
		if row[1] == '*': return row[1]
		else: return line.split('\t')[1]
	else: 
		return line.strip(' \t\n')

def parse_apertium(line):
	o = []
	analyses = line[1:-2].split('/')[1:]
	for analysis in analyses:
		n = analysis.replace('<', ' <').replace('+', ' + @').split(' ')
		n[0] = ' '.join([i for i in n[0]])
		o.append(' '.join(n))
	return o

def parse_ud(line):
	row = line.split('\t')
	o = ' '.join([i for i in row[2]])
	o += ' ' + row[3]	
	o += ' ' + row[5].replace('|', ' ')

	return o

ud_line = ud_f.readline()
ap_line = ap_f.readline()
count = 0
while ud_line != '' and ap_line != '':
	if ud_line == '' or ap_line == '' or ud_line[0] == '#' or ap_line[0] == '¶':
		count += 1
		ud_line = ud_f.readline()
		ap_line = ap_f.readline()
		continue

	if ap_line.count('^') > 1:
		print('WARNING: Too many ^ on line %d' % (count), file=sys.stderr)
		count += 1
		ud_line = ud_f.readline()
		ap_line = ap_f.readline()
		continue

	ap_form = form(ap_line) 
	ud_form = form(ud_line) 

	if ap_form != ud_form:
		print('ERROR: Misalignment on line %d' % (count), file=sys.stderr)
		print(ap_form,'|', ud_form, file=sys.stderr)
		print('U:', ud_line, file=sys.stderr)
		print('A:', ap_line, file=sys.stderr)
		sys.exit(-1)

	if ap_form.strip() == '' and ud_form.strip() == '':
		count += 1
		ud_line = ud_f.readline()
		ap_line = ap_f.readline()
		continue

#	print(count, ap_form, ud_form)

	ap_analyses = parse_apertium(ap_line)
	ud_analysis = parse_ud(ud_line)

	for ap_analysis in ap_analyses:
		print('%s ||| %s' % (ap_analysis, ud_analysis))
	
	count += 1
	ud_line = ud_f.readline()
	ap_line = ap_f.readline()
