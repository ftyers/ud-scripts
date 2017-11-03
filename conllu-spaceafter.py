# -*- coding: UTF-8 -*-
# Author: Aibek Makazhanov <aibek.makazhanov@nu.edu.kz>

import sys
import os
import codecs
import re

def main():

    tm = '# text = '
    fd = sys.stdout
    lp = 0
    mwt = range(0,0)
    for l in codecs.open(sys.argv[1],'r','utf-8').readlines():
        l = l.strip()
        if not l:
            lp = 0
            mwt = range(0,0)
        if l.startswith(tm):
            txt = l[len(tm):]
            #fd.write('%s\n'%txt.encode('utf-8'))
        fields = l.split('\t')
        if len(fields)==10:
            tid = fields[0]
            if tid.count('-'):
                rng = tid.split('-')
                mwt = range(int(rng[0]),int(rng[1])+1)
                tid = int(rng[0]) - 1
            else: tid = int(tid)
            tok = fields[1]
            #fd.write('%s\n'%tok.encode('utf-8'))
            p = txt.find(tok,lp)
            if p>=0 and not (re.sub('\s','',txt[lp:p]) or tid in mwt):
                lp = p + len(tok)
                #fd.write('%d\t%d\t%s\n'%(p,lp,txt[lp:].encode('utf-8')))
                if lp<len(txt) and not re.match('^\s',txt[lp:]):
                    if fields[9] == '':
                        fields[9] = 'SpaceAfter=No'
                    else: 
                        fields[9] += '|SpaceAfter=No'
        l = '\t'.join(fields)
        fd.write('%s\n'%l.encode('utf-8'))

if __name__=='__main__':
    main()
