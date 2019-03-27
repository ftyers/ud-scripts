"""
Todo:
	- Subreadings
	- Per rule statistics
"""
import sys, re

r_wordform = re.compile('^"<[^>]+>"$')
r_baseform = re.compile(';?\t"[^$]+" ')
r_rule = re.compile('(REMOVE|SELECT):[^$]+$')

if len(sys.argv) < 3: 
	print('vislcg3-evaluate.py <src> <ref> <tst>')
	sys.exit(-1)

f_src = open(sys.argv[1])
f_ref = open(sys.argv[2])
f_tst = open(sys.argv[3])

tokens = {}
idx = 0
n_analyses_src = 0
n_analyses_ref = 0
n_analyses_tst = 0

for line in f_src.readlines():
	if r_wordform.match(line):
		idx += 1
		wordform = line[2:-3]
		tokens[idx] = (wordform, {})
	if r_baseform.match(line):
		n_analyses_src += 1			
		tokens[idx][1][line.strip()] = False

idx = 0
for line in f_ref.readlines():
	if r_wordform.match(line):
		idx += 1
		wordform = line[2:-3]
		if tokens[idx][0] != wordform:
			print('Alignment broken,\n', idx, line)
			sys.exit(-1)
	if r_baseform.match(line):
		n_analyses_ref += 1			
		tokens[idx][1][line.strip()] = True

idx = 0
n_removed = 0
n_fn = 0 # Bad rule non-application
n_fp = 0 # Bad rule application
n_tn = 0 # Good rule non-application
n_tp = 0 # Good rule application
errors = []
for line in f_tst.readlines():
	if r_wordform.match(line):
		idx += 1
		wordform = line[2:-3]
		if tokens[idx][0] != wordform:
			print('Alignment broken,\n', idx, line)
			sys.exit(-1)
	if r_baseform.match(line):
		analysis = line.strip()
		if line[0] == ';':	
			n_removed += 1
			rule_match = r_rule.search(analysis)
			analysis = analysis[1:rule_match.start()].strip()
			rules = rule_match.group().strip()
			if analysis in tokens[idx][1]:
				# If the rule has deleted a reading that is found in the reference
				if tokens[idx][1][analysis] == True:
					n_fp += 1
					errors.append((idx, analysis, tokens[idx][1], rules))
				# If the rule has deleted a reading that is not found in the reference
				elif tokens[idx][1][analysis] == False:
					n_tp += 1
		else:
			n_analyses_tst += 1			
			if analysis in tokens[idx][1]:
				# If a reading is left in that is not found in the reference
				if tokens[idx][1][analysis] == False:
					n_fn += 1	
					errors.append((idx, analysis, tokens[idx][1], ''))
				# If a reading is left that is the one found in the reference
				elif tokens[idx][1][analysis] == True:
					n_tn += 1

print('Tokens:')
print()
for token in tokens:
	print(token,'|', tokens[token], file=sys.stderr)
print()
print('Errors:')
print()
for error in errors:
	print(error[0], '|', error[1], '|', error[2])
print()
print('--------------------------------------------------------------------------------')
print('Input analyses:', n_analyses_src)
print('Reference analyses:', n_analyses_ref)
print('Output analyses:', n_analyses_tst)
print()
print('Input ambiguity:', n_analyses_src / len(tokens))
print('Reference ambiguity:', n_analyses_ref / len(tokens))
print('Output ambiguity:', n_analyses_tst / len(tokens))
print()
print('False positives:', n_fp)
print('False negatives:', n_fn)
print('True positives:', n_tp)
print('True negatives:', n_tn)
print()
precision =  n_tp / (n_tp + n_fp)
recall = n_tp / (n_tp + n_fn)
print('Precision:', precision)
print('Recall:', recall)
print('F1: %.4f' % (2 * ((precision * recall) / (precision + recall))))
print()
