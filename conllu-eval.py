import sys ;

if len(sys.argv) != 3: #{
	print('conllu-eval.py <ref file> <tst file>');
	sys.exit(-1);
#}

ref = open(sys.argv[1]);
tst = open(sys.argv[2]);

total = 0.0;
uas_correct = 0.0;
las_correct = 0.0;
uas_errors = 0.0;
las_errors = 0.0;

while True: #{

	ref_l = ref.readline();
	tst_l = tst.readline();

	if ref_l == '' and tst_l == '': #{
		break;
	#}

	if ref_l == '\n' and tst_l == '\n': #{
		continue;
	#}

	ref_r = ref_l.split('\t');
	tst_r = tst_l.split('\t');

	if ref_r[0].count('-') > 0 and tst_r[0].count('-') > 0: #{
		ref_l = ref.readline();
		ref_r = ref_l.split('\t');
		tst_l = tst.readline();
		tst_r = tst_l.split('\t');
	elif ref_r[0].count('-') > 0 and tst_r[0].count('-') == 0: #{
		ref_l = ref.readline();
		ref_r = ref_l.split('\t');
	#}

	if ref_r[1] != tst_r[1]: #{
		print('ERROR: Unaligned', file=sys.stderr);
		print('REF:', ref_r, file=sys.stderr);
		print('TST:', tst_r, file=sys.stderr);
		break;
	#}
	if ref_r[1] == tst_r[1] and ref_r[6] == tst_r[6]: #{
		uas_correct = uas_correct + 1.0;
	elif ref_r[1] == tst_r[1] and ref_r[6] != tst_r[6]: #{
		uas_errors = uas_errors + 1.0;	

	#}
	if ref_r[1] == tst_r[1] and ref_r[6] == tst_r[6] and ref_r[7] == tst_r[7]: #{
		las_correct = las_correct + 1.0;
	elif ref_r[1] == tst_r[1] and (ref_r[6] != tst_r[6] or ref_r[7] != tst_r[7]): #{
		las_errors = las_errors + 1.0;	

	#}

	total = total + 1.0
#}
print('UAS: %.2f' % (uas_correct/total*100.0));
print('LAS: %.2f' % (las_correct/total*100.0));
