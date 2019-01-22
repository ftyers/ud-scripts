import sys;

skipUnknown = True;
testFunc = False;

# src: ^власти/власть<n><f><nn><sg><gen>/власть<n><f><nn><sg><dat>/власть<n><f><nn><sg><prp>/власть<n><f><nn><pl><acc>/власть<n><f><nn><pl><nom>$
# ref: ^власти/власть<n><f><nn><sg><dat><@P←>$	
# tst: ^власти/власть<n><f><nn><sg><dat>$

def readings(w, testFunc): #{
	readings = [];
	removed_readings = [];
	reading = '';
	seen = False;
	escaped = False;
	for c in w: #{
#		print('@@', c, w, escaped, seen, readings, file=sys.stderr);
		if c == '\\': #{
			escaped = True; 
		#}
		if c != '\\' and escaped: #{
			reading = reading + c;
			escaped = False;
			continue;
		#}
		if c == '/' and seen == False and not escaped: #{
			seen = True;
			continue;
		elif (c == '/' or c == '$') and seen and not escaped: #{
			if len(reading) < 1: #{
				print('Feil: ', w ,file=sys.stderr); 
			#}
			if reading[0] == '¬': #{
				removed_readings.append(reading);
			else: #{
				if testFunc:
					readings.append(reading_lemma(reading) + reading_msd(reading) + reading_func(reading));
				else:
					readings.append(reading_lemma(reading) + reading_msd(reading));
				
			#}
			reading = '';
			continue;
		#}
		if seen: #{
			reading = reading + c;
		#}
	#}
	return (readings, removed_readings);
#}

def clean(s): #{

	o = s.replace('¹', '').replace('²', '').replace('³', '').replace('⁻', '');
	return o;
#}

def reading_lemma(r): #{
	r = clean(r);
	return r.split('<')[0];
#}

def reading_pos(r): #{
	if r.count('<') < 1: #{
		return '<unk>';
	#}
	return '<' + r.split('<')[1].split('>')[0] + '>';
#}

def reading_msd(r): #{
	msd = '';
	seen = False;
	tag = '';
	for c in r: #{
		if c == '<': #{
			seen = True;
		#}
		if c == '>': #{
			tag = tag + c;
			if tag.count(':') > 0 or len(tag) < 2: #{
				continue;
			elif tag[1] == '@': #{
				continue;
			else: #{
				msd = msd + tag;
			#}
			tag = '';
			continue;
		#}
		if seen: #{
			tag = tag + c;
		#}
	#}
	return msd;
#}

def reading_func(r): #{
	func = '';
	seen = False;
	for c in r: #{

		if c == '@': #{
			seen = True;
		#}
		if c == '>': #{
			seen = False;
		#}
		if seen: #{
			func = func + c;
		#}
	#}
	func = '<' + func + '>';
	return func.replace('<>', '');
#}

def readings_rules(readings): #{
	rules = set();
	readings_rules = {};

	for r in readings: #{
		reading = '';
		seen = False;
		tag = '';
		first = True;
		for c in r: #{
			if c == '<' and first == False: #{
				seen = True;
			elif c == '<' and first == True: #{
				seen = True;
				first = False;		
			#}
			if c == '+': #{
				first = True;
			#}
			if c == '¬': #{
				continue;
			#}
			if c == '>': #{
				tag = tag + c;
				if tag.count(':'): #{
					rules.add(tag);
				else: #{
					reading = reading + tag;
				#}
				tag = '';
				seen = False;
			#}
			if seen and not first: #{
				tag = tag + c;
			elif first: #{
				reading = reading + c;
			#}
		#}
		if reading not in readings_rules: #{
			readings_rules[reading] = [];
		#}
		readings_rules[reading] = list(rules);
	#}
	return (rules, readings_rules);
#}

src_f = open(sys.argv[1]);
ref_f = open(sys.argv[2]);
tst_f = open(sys.argv[3]);

# Sanity check

src_l = len(src_f.readlines()); 
ref_l = len(src_f.readlines()); 
tst_l = len(src_f.readlines()); 

lines = -1; 

if src_l != ref_l != tst_l: #{
	print(src_l, ref_l, tst_l, file=sys.stderr);
else: #{
	lines = src_l;
#}

src_f.close();
ref_f.close();
tst_f.close();

src_f = open(sys.argv[1]);
ref_f = open(sys.argv[2]);
tst_f = open(sys.argv[3]);

n_tokens = 0;
n_unknown = 0;
n_line = 0;
            #                       tp tn fp fn
rules = {}; # rules['SELECT:462'] = (0, 0, 0, 0) 

applic = {}; # applic['SELECT:462'] = 0;

feiler = {}; # feiler['SELECT:462'] = [13, 45, 100]; 

n_truepositive = 0;
n_truenegative = 0;
n_falsepositive = 0;
n_falsenegative = 0;

n_ref_readings = 0;
n_src_readings = 0;
n_tst_readings = 0;

n_tst_lema_correct = 0;
n_tst_pos_correct = 0;
n_tst_lemapos_correct = 0;
n_tst_msd_correct = 0;
n_tst_lemamsd_correct = 0;
n_tst_func_correct = 0;

n_bas_lema_correct = 0;
n_bas_pos_correct = 0;
n_bas_lemapos_correct = 0;
n_bas_msd_correct = 0;
n_bas_lemamsd_correct = 0;
n_bas_func_correct = 0;

for line in range(0, lines): #{
	n_line = n_line + 1;
	src_w = src_f.readline();
	ref_w = ref_f.readline();
	tst_w = tst_f.readline();

#	print(src_w);
#	print(ref_w);
#	print(tst_w);

	if src_w.count('¶') > 0: #{
		continue;
	#}

	n_tokens = n_tokens + 1;

	tst_readings = [];
	tst_lema = '';
	tst_pos = '';
	tst_func = '';
	tst_msd = '';
	src_readings = [];
	src_lema = '';
	src_pos = '';
	src_func = '';
	src_msd = '';
	ref_readings = [];
	ref_lema = '';
	ref_pos = '';
	ref_func = '';
	ref_msd = '';



	if tst_w.count('/*') < 1 and tst_w[0] == '^': #{
		tst_readings, tst_removed = readings(tst_w, testFunc);
		tst_lema = reading_lemma(tst_readings[0]);
		tst_pos = reading_pos(tst_readings[0]);
		tst_func = reading_func(tst_readings[0]);
		tst_msd = reading_msd(tst_readings[0]);

		src_readings, src_removed = readings(src_w, testFunc);
		src_lema = reading_lemma(src_readings[0]);
		src_pos = reading_pos(src_readings[0]);
		src_func = reading_func(src_readings[0]);
		src_msd = reading_msd(src_readings[0]);

		n_src_readings = n_src_readings + len(src_readings);
		n_tst_readings = n_tst_readings + len(tst_readings);
	#}

	if ref_w.count('/*') < 1 and ref_w[0] == '^': #{
		ref_readings, ref_removed = readings(ref_w, testFunc);
		ref_lema = reading_lemma(ref_readings[0]);
		ref_pos = reading_pos(ref_readings[0]);
		ref_func = reading_func(ref_readings[0]);
		ref_msd = reading_msd(ref_readings[0]);
		n_ref_readings = n_ref_readings + 1;
	#}

	if tst_w.count('/*') > 0 and skipUnknown == True: #{
		print('*\t', ref_lema, ref_msd);
		n_unknown = n_unknown + 1;
		continue;	
	#}

	#n_ref_readings = n_ref_readings + 1;

	#######################################################################

	tst_rules, tst_readings_rules = readings_rules(tst_readings + tst_removed);
	#print('READINGS:', tst_readings);
	#print('RULES_READINGS:', tst_readings_rules);
	for rule in list(tst_rules): #{
		if rule not in rules: #{
			rules[rule] = (0, 0, 0, 0);
		#}
		#print('RULES:', rule, rules[rule]);
	#}


	for tst_reading in tst_readings: #{
		if tst_reading not in ref_readings: #{
			n_falsepositive = n_falsepositive + 1;
			for rule in tst_readings_rules[tst_reading]: #{
				(tp, tn, fp, fn) = rules[rule];	
				fp = fp + 1;
				rules[rule] = (tp, tn, fp, fn);
			#}
		else: #{
			n_truepositive = n_truepositive + 1;
			for rule in tst_readings_rules[tst_reading]: #{
				(tp, tn, fp, fn) = rules[rule];	
				tp = tp + 1;
				rules[rule] = (tp, tn, fp, fn);
			#}
		#}
	#}

	for ref_reading in ref_readings: #{
		if ref_reading not in tst_readings: #{
			print('['+ str(n_line) +'] FALSENEG:', ref_reading, tst_readings);
			n_falsenegative = n_falsenegative + 1;
			if ref_reading not in tst_readings_rules: #{
				continue;
			#}
			for rule in tst_readings_rules[ref_reading]: #{
				(tp, tn, fp, fn) = rules[rule];	
				fn = fn + 1;
				rules[rule] = (tp, tn, fp, fn);
				if rule not in feiler: #{
					feiler[rule] = [];
				#}
				feiler[rule].append(n_line);
			#}
		#}
	#}

	for src_reading in src_readings: #{
		if src_reading not in ref_readings and src_reading not in tst_readings: #{
			n_truenegative = n_truenegative + 1;
			if src_reading not in tst_readings_rules: #{
				continue;
			#}
			for rule in tst_readings_rules[src_reading]: #{
				(tp, tn, fp, fn) = rules[rule];	
				tn = tn + 1;
				rules[rule] = (tp, tn, fp, fn);
			#}
		#}
	#}

	#######################################################################

	if tst_lema == ref_lema and tst_msd == ref_msd: #{
		print('=\t', tst_lema, tst_msd);
	else: #{
		#print('ref:', ref_readings, file=sys.stderr);
		print('-\t', ref_lema, ref_msd, src_readings);
		#print('tst:', tst_readings, file=sys.stderr);
		print('+\t', tst_lema, tst_msd, tst_readings);
	#}

	if ref_lema+ref_msd not in tst_readings and ref_lema+ref_msd in src_readings: #{
		print('!\t', ref_lema+ref_msd, tst_readings);
	#}
	
	if src_lema == ref_lema: n_bas_lema_correct = n_bas_lema_correct + 1;
	if src_lema == ref_lema and src_pos == ref_pos: n_bas_lemapos_correct = n_bas_lemapos_correct + 1;
	if src_lema == ref_lema and src_msd == ref_msd: n_bas_lemamsd_correct = n_bas_lemamsd_correct + 1;
	if src_pos == ref_pos: n_bas_pos_correct = n_bas_pos_correct + 1;
	if src_msd == ref_msd: n_bas_msd_correct = n_bas_msd_correct + 1;
	
	if tst_lema == ref_lema: n_tst_lema_correct = n_tst_lema_correct + 1;
	if tst_lema == ref_lema and tst_pos == ref_pos: n_tst_lemapos_correct = n_tst_lemapos_correct + 1;
	if tst_lema == ref_lema and tst_msd == ref_msd: n_tst_lemamsd_correct = n_tst_lemamsd_correct + 1;
	if tst_pos == ref_pos: n_tst_pos_correct = n_tst_pos_correct + 1;
	if tst_msd == ref_msd: n_tst_msd_correct = n_tst_msd_correct + 1;
	if tst_func == ref_func and ref_func != '': n_tst_func_correct = n_tst_func_correct + 1;

#	print("");
#}

# Accuracy = number of correct analyses / number of analyses in ref;
# False positives

# Lemma accuracy
# POS accuracy
# MSD accuracy
# Func accuracy

print('');

print("n_ref: %d" % ( n_ref_readings ));
print("n_src: %d" % ( n_src_readings ));
print("n_tst: %d" % ( n_tst_readings ));

print('');

print('unknown  :\t', n_unknown,'(', (float(n_unknown)/float(n_ref_readings))*100.0,')');

print('');

print('truepos  :\t', n_truepositive);
print('trueneg  :\t', n_truenegative);
print('falsepos :\t', n_falsepositive);
print('falseneg :\t', n_falsenegative);

precision = float(n_truepositive) / (float(n_truepositive + n_falsepositive));
recall = float(n_truepositive) / (float(n_truepositive + n_falsenegative));
accuracy = float(n_truepositive + n_truenegative) / (float(n_truepositive + n_falsenegative + n_truenegative + n_falsepositive));
fscore = 2.0 * ((precision*recall) / (precision+recall));

print('');

print('precision:\t', precision, '\t( true pos / all pos )');
print('recall   :\t', recall, '\t( true pos / (true pos + false neg) )');
print('fscore   :\t', fscore);

print('accuracy :\t', accuracy, '\t( (true pos + true neg) / (everything) )');

print('');

src_ambig_rate = float(n_src_readings)/float(n_ref_readings);
tst_ambig_rate = float(n_tst_readings)/float(n_ref_readings);
print('tokens   :\t', n_tokens);
print('src_ambig:\t', src_ambig_rate);
print('tst_ambig:\t', tst_ambig_rate);
###print('resolved :\t %.2f%%' % (100.0-(tst_ambig_rate/src_ambig_rate*100.0))); ## CHECK THIS
xx = (n_src_readings-n_ref_readings);
yy = (n_tst_readings-n_ref_readings);
zz = yy/xx;
print('resolved :\t %.2f' % ((1.0-zz)*100))

print('');

p_bas_lema_correct = float(n_bas_lema_correct)/float(n_ref_readings)*100.0;
p_bas_pos_correct = float(n_bas_pos_correct)/float(n_ref_readings)*100.0;
p_bas_lemapos_correct = float(n_bas_lemapos_correct)/float(n_ref_readings)*100.0;
p_bas_msd_correct = float(n_bas_msd_correct)/float(n_ref_readings)*100.0;
p_bas_lemamsd_correct = float(n_bas_lemamsd_correct)/float(n_ref_readings)*100.0;
p_bas_func_correct = float(n_bas_func_correct)/float(n_ref_readings)*100.0;

print('lem      :\t',p_bas_lema_correct);
#print('pos      :\t',p_bas_pos_correct);
print('lem+pos  :\t',p_bas_lemapos_correct);
#print('msd      :\t',p_bas_msd_correct);
print('lem+msd  :\t',p_bas_lemamsd_correct);
print('func     :\t',p_bas_func_correct);

print('');

p_tst_lema_correct = float(n_tst_lema_correct)/float(n_ref_readings)*100.0;
p_tst_pos_correct = float(n_tst_pos_correct)/float(n_ref_readings)*100.0;
p_tst_lemapos_correct = float(n_tst_lemapos_correct)/float(n_ref_readings)*100.0;
p_tst_msd_correct = float(n_tst_msd_correct)/float(n_ref_readings)*100.0;
p_tst_lemamsd_correct = float(n_tst_lemamsd_correct)/float(n_ref_readings)*100.0;
p_tst_func_correct = float(n_tst_func_correct)/float(n_ref_readings)*100.0;

print('lem      :\t',p_tst_lema_correct, '(', p_tst_lema_correct-p_bas_lema_correct, ')');
#print('pos      :\t',p_tst_pos_correct, '(', p_tst_pos_correct-p_bas_pos_correct, ')');
print('lem+pos  :\t',p_tst_lemapos_correct, '(', p_tst_lemapos_correct-p_bas_lemapos_correct, ')');
#print('msd      :\t',p_tst_msd_correct, '(', p_tst_msd_correct-p_bas_msd_correct, ')');
print('lem+msd  :\t',p_tst_lemamsd_correct, '(', p_tst_lemamsd_correct-p_bas_lemamsd_correct, ')');
print('func     :\t',p_tst_func_correct, '(', p_tst_func_correct-p_bas_func_correct, ')');

rkeys = list(rules.keys());
rkeys.sort();
print('');
print('Rule No.\tTP\tTN\tFP\tFN');
for rule in rkeys: #{
	print('%s\t%d\t%d\t%d\t%d' % (rule, rules[rule][0], rules[rule][1], rules[rule][2], rules[rule][3]));
#	print(rule, rules[rule]);
#}
print('');
for rule in rkeys: #{
	if rule in feiler: #{
		print(rule, '\t', feiler[rule]);
	#}
#}
