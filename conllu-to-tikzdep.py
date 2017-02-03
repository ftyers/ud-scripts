#!/usr/bin/python3

###############################################################################
#        Convert a file in CoNLL-U format to TikZdependency + XeLaTeX         #
###############################################################################
#
# $ cat output.conllu  | python3 ~/scripts/conllu-to-tikzdep.py <direction>
#
# Where direction is:
#  * head (default) = head → dependent arrows 
#  * dependent = dependent → head arrows 
#
###############################################################################

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

def trykk(s, f, o): #{

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
	rootPos = 1;
	for ord in s: #{
		if s[ord][3][0] == "0" and not seenRoot: #{
			print("\deproot{%s}{\qgmk{root}}" % s[ord][3][rootPos], file=f);
			rootNode = s[ord][3][rootPos];
			seenRoot = True;
			continue;
		#}

		if s[ord][3][1] == "0" and seenRoot: #{
			print("\depedge[edge unit distance=1.5ex,edge below]{%s}{%s}{\qgmk{%s}}" % (s[ord][3][0], rootNode, "x"), file=f);
		else: #{
			if o == 'head': #{
				print("\depedge{%s}{%s}{\qgmk{%s}}" % (s[ord][3][0], s[ord][3][1], s[ord][3][2].lower()), file=f);
			else: #{
				print("\depedge{%s}{%s}{\qgmk{%s}}" % (s[ord][3][1], s[ord][3][0], s[ord][3][2].lower()), file=f);
			#}
		#}

	#}
		
#}

###############################################################################

origin = 'head'
prefiks = '/tmp/sentence.';
sno = 0;
pos = 0;

if len(sys.argv) > 1 and sys.argv[1] == 'dependent': #{
	origin = 'dependent';
#}

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
		trykk(words, fil, origin);
		print(footer, file=fil);
		words = {};
		pos = 0;
		fil.close();
		continue;
	#}
	if line.count('\t') > 4: #{
		row = line.split('\t');
		if '-' in row[0]: #{
			multiword = row[1]
		else: #{
			if row[1]=="_": #{
				if multiword: #{
					row[1] = multiword
					multiword = False
				else: #{
					row[1] = "\\_"
				#}
			#}
			print(row,file=sys.stderr);
			words[pos] = (row[1], row[2], '-', (row[6], row[0], row[7].strip()));
			if row[4] != '_': #{
				words[pos] = (row[1], row[2], row[4], (row[6], row[0], row[7].strip()));
			#}
			if row[3] != '_': #{
				words[pos] = (row[1], row[2], row[3], (row[6], row[0], row[7].strip()));
			#}
			pos = pos + 1;
		#}
	#}
#}
