import sys 

MIN_ANALYSIS_FREQ = 5 

dico = {}

def train(inn, out): 
	for line in inn.readlines():
		line = line.strip()
		if line == '':
			continue
		if line[0] == '#': 
			continue
		row = line.split('\t')
		if row[0].count('.') > 0 or row[0].count('-') > 0: 
			continue
		form = row[1]
		analysis = row[2] + '\t' + row[3] + '\t' + row[5];
		
		if form not in dico:
			dico[form] = {}
		if analysis not in dico[form]:
			dico[form][analysis] = 0
		dico[form][analysis] += 1
	
	for form in dico:
		for analysis in dico[form]:
			if dico[form][analysis] >= MIN_ANALYSIS_FREQ:
				print('%s\t%s' % (form, analysis), file=out)

def analyse(inn, out, model):
	dico = {}
	for line in model.readlines():
		line = line.strip()
		if line == '':
			continue
		row = line.split('\t')
		form = row[0]
		row[3] = row[3].replace('_','').replace('|', ' ')
		rest = row[1:]
		if form not in dico:
			dico[form] = []
		dico[form].append(rest)

	line = inn.readline()	
	while line != '':
		line = line.strip('\n')
		for punct in '!,.?:;':
			line = line.replace(punct, ' '+punct)
		for token in line.split(' '):
			print('"<%s>"' % (token), file=out)
			if token in dico:
				for analysis in dico[token]:
					print('\t"%s" %s' % (analysis[0], ' '.join(analysis[1:])), file=out)
			else:
				print('\t"*%s"' % (token), file=out)
		line = inn.readline()
		

if len(sys.argv) == 3 and sys.argv[1] == '-t':
	out = open(sys.argv[2], 'w')
	train(sys.stdin, out)	
elif len(sys.argv) == 2:
	model = open(sys.argv[1])	
	analyse(sys.stdin, sys.stdout, model)
else:
	print('conllu-analyser.py [-t] model.dat');
	sys.exit(-1)

