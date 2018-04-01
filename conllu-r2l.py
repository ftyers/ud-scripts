# -*- coding: UTF-8 -*-
# Author: Aibek Makazhanov

import sys
import os
import codecs
import re


def node_from_text(txt,dlm='\t'):
    fields = txt.split(dlm)
    if not len(fields)==10:
	return
    elif not fields[0].isdigit():
	return node(fields,empty=1)
    return node(fields)


class node():
    
    def __init__(self,fields,empty=0):
	self.fieldnames = ['nid','form','lemma','upos','xpos',\
	                   'feats','head','deprel','deps','misc']
	for i,f in enumerate(fields):
	    self.__dict__[self.fieldnames[i]] = f
	self.empty = empty
	self.nodeid = empty and int(self.nid.split('-')[0])-0.5 or float(self.nid)
	self.head = empty and self.head or int(self.head)
	self.children = {}
    
    def __repr__(self):
	ret = []
	for f in self.fieldnames:
	    if type(self.__dict__[f]) in [unicode,str]:
		ret.append(self.__dict__[f])
	    else:
		ret.append(str(int(self.__dict__[f])))
	ret = u'\t'.join(ret)
	return unicode(ret)
    
    def __str__(self):
	return self.__repr__()


class tree():
    
    def __init__(self,txt,sidmark='# sent_id = ',txtmark='# text = '):
	self.src = txt
	self.nodes = {}
	self.parchild = {}
        self.translations = []
	for l in txt.split('\n'):
	    l = l.strip()
	    if not l: continue
	    if l.startswith(sidmark):
		self.sid = l
	    elif l.startswith(txtmark):
		self.text = l
	    elif l.startswith('# labels ='):
		self.labels = l
	    elif l.startswith('# text['):
		self.translations.append(l)
	    else:
		n = node_from_text(l)
		if n:
		    self.nodes[n.nodeid] = n
		    if not n.empty:
			self.parchild[n.head] = self.parchild.get(n.head,{})
			self.parchild[n.head][n.nodeid] = 1
    
    def walk(self,root=0):
	ret = []
	if not (root in self.parchild and self.parchild[root]): return ret
	if root in self.nodes:
	    #heads.append(self.nodes[root])
	    ret.append(self.nodes[root])
	    #print root
	for n in sorted(self.parchild[root]):
	    #print n
	    ret += self.walk(n)
	return ret
    
    def rebuild(self):
	self.parchild = {}
	for n in self.nodes.values():
	    if not n.empty:
		self.parchild[n.head] = self.parchild.get(n.head,{})
		self.parchild[n.head][n.nodeid] = 1
    
    def __repr__(self):
	ret = [self.sid,self.text]
        for i in self.translations: ret.append(i)
        ret.append(self.labels)
	for nid,node in sorted(self.nodes.iteritems()):
            ret.append(unicode(node))
	ret = u'\n'.join(ret)
	return ret.encode('utf-8')


def flip_rels(t,rel):
    cnt = 0
    for n in t.walk():
	tar = []
	for c in sorted(t.parchild[n.nodeid]):
	    if t.nodes[c].deprel==rel:
		if c>n.nodeid and tar:
		    sys.stderr.write('\n!!!STRANGE!!!\n%s'%t.sid.encode('utf-8'))
		    sys.stderr.write('%d %d %s\n' %(c,n.nodeid,rel))
		elif c<n.nodeid:
		    tar.append(c)
	if tar:
	    #print '\n%s'%t.sid.encode('utf-8')
	    #print tar,n.nodeid,rel
	    cnt += len(tar)
	    t.nodes[tar[0]].deprel = n.deprel
	    t.nodes[tar[0]].head = n.head
	    n.deprel = rel
	    n.head = tar[0]
	    for e in tar[1:]:
		t.nodes[e].head = n.head
    t.rebuild()
    return cnt


def main():

    tm = '# text = '
    fd = len(sys.argv)>2 and codecs.open(sys.argv[2],'w') or sys.stdout
    rels = len(sys.argv)>3 and\
        [l.strip() for l in codecs.open(sys.argv[3],'r','utf-8') if l.strip()]\
        or ['appos','conj','goeswith','flat','flat:name', 'fixed', 'fixed:mwe']
    #['conj','goeswith','appos']
    flips = dict.fromkeys(rels,0)
    ct = []
    for l in codecs.open(sys.argv[1],'r','utf-8').readlines():
	l = l.strip()
	if not l:
	    src = '\n'.join(ct)
	    t = tree(src)
	    for rel in rels:
		fc = flip_rels(t,rel)
		flips[rel] += fc
	    #flip_rels(t,'flat:name')
	    #flip_rels(t,'parataxis')
	    fd.write('%s\n\n'%t)
	    #fd.write('\n%s\n'%t.sid.encode('utf-8'))
	    #fd.write('%s\n'%' '.join([str(n.nodeid) for n in t.walk()]))
	    ct = []
	    #break
	else:
	    ct.append(l)
    sys.stderr.write('\nflipped from right to left:\n')
    for r in rels:
	sys.stderr.write('%s\t%d\n'%(r,flips[r]))

if __name__=='__main__':
    main()
