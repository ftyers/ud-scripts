# ud-scripts
Scripts for compatibilitising between VISL-CG3, Apertium, CoNLL-X and Universal Dependency

*vislcg3-flatten.sh:*

Flatten VISL-CG3 output, replaces subreadings with null surface tokens (well, actually '*').

*vislcg3-to-conllx-input.py:*

Convert VISL-CG3 output to ConLL-X format. 

*vislcg3-split-space.py:*

Split multiword tokens where the number of spaces in the surface form and lemma are the same into two tokens.

*conllu-to-tikzdep.py:*

Convert CoNLL-U to TiKZdependency graphs. One file per input sentence.

*conllu-to-matxin.py:*

Convert CoNLL-U to Matxin XML format

*matxin-to-conllu.py:*

Convert Matxin XML format to CoNLL-U

*conllu-feats.py:*

Replace lem-pos-feats in some other format to UD using a 6-column rule file.

*conllu-trim.py:*

Remove double blank lines between sentences
