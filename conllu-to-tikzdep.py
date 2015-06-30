#!/usr/bin/python3

import sys, re;

header = """
\documentclass[landscape,a5paper,12pt]{minimal}
\\usepackage{tikz-dependency} 

\\usepackage{fontspec}
\\usepackage{xunicode}
\\usepackage{xltxtra}
\\usepackage[margin=1.5in,landscape]{geometry}

\setromanfont{Times New Roman}

\\newfontfamily\qgmk[Scale=MatchLowercase,Letters=SmallCaps]{Linux Libertine O}

\\begin{document}

\\resizebox{\\textwidth}{!}{%
\centering
\\begin{dependency}[edge horizontal padding=5pt]
   \\begin{deptext}[column sep=0.3cm]


""";

footer = """
\end{dependency}
}

\end{document}
""";

###############################################################################

def trykk(s, f): #{

	for j in range(0,3): #{
		last = False;
		for ord in s: #{
			if ord == len(s)-1: #{
				last = True;
			#}
			if j == 2: #{
				print("\\texttt{"+str(s[ord][j].strip())+"}", end='', file=f);
			else: #{
				print(str(s[ord][j]).replace('%', '\%'), end='', file=f);
			#}
			if not last: #{
				print(' \& ', end='', file=f);
			else: #{
				print(" \\\\", file=f);
			#}
		#}
	#}

	print("   \end{deptext}", file=f);

	seenRoot = False;
	rootNode = '';
	for ord in s: #{
		if s[ord][3][1] == "0" and not seenRoot: #{
			print("\deproot{%s}{\qgmk{root}}" % s[ord][3][0], file=f);
			rootNode = s[ord][3][0];
			seenRoot = True;
			continue;
		if s[ord][3][1] == "0" and seenRoot: #{
			print("\depedge[edge unit distance=1.5ex,edge below]{%s}{%s}{\qgmk{%s}}" % (s[ord][3][0], rootNode, "x"), file=f);
		else: #{
			print("\depedge{%s}{%s}{\qgmk{%s}}" % (s[ord][3][0], s[ord][3][1], s[ord][3][2].lower()), file=f);
		#}
	
	#}
		
#}

###############################################################################

prefiks = '/tmp/sentence.';
sno = 0;
pos = 0;

# words[0] = ('Город', 'город', 'n', (1,2,'subj'))
words = {}

for line in sys.stdin.readlines(): #{
	if line[0] == '#': #{
		continue;
	#}
	if line.strip() == '': #{
		print(sno, file=sys.stderr);
		sno = sno + 1;
		fitxer = prefiks + str(sno).zfill(4) + '.tex';
		fil = open(fitxer, 'w+');
		print(header, file=fil);
		trykk(words, fil);
		print(footer, file=fil);
		words = {};
		pos = 0;
		fil.close();
		continue;
	#}
	if line.count('\t') > 4: #{
		row = line.split('\t');
		if '-' in row[0]:
			multiword = row[1]
		else:
			if row[1]=="_":
				if multiword:
					row[1] = multiword
					multiword = False
				else:
					row[1] = "\\_"
			words[pos] = (row[1], row[2], row[4], (row[0], row[6], row[7].strip()));
			pos = pos + 1;
	#}
#}
