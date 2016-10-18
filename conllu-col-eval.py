import sys ;

ref = open(sys.argv[1]);
tst = open(sys.argv[2]);
col = int(sys.argv[3]);

total = 0.0;
correct = 0.0;
errors = 0.0;

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

	if ref_r[1] != tst_r[1]: #{
		print('ERROR: Unaligned', file=sys.stderr);
		print(ref_r, file=sys.stderr);
		print(tst_r, file=sys.stderr);
		break;
	#}
	if ref_r[1] == tst_r[1] and ref_r[col] == tst_r[col]: #{
		correct = correct + 1.0;
	elif ref_r[1] == tst_r[1] and ref_r[col] != tst_r[col]: #{
		errors = errors + 1.0;	

	#}
	total = total + 1.0
#}
print('%.2f' % (correct/total*100.0));
