import re
import sys
import os
import operator
import collections
from sets import Set

k = {}
dummyk = {}
countMap = {}
sameCount = {}
ic = []
l = []
i = 0
counter = 0
flag = 0
def icCount(file):
    global l, i
    kind = re.compile("kind = (\S+)")
    instinfo = re.compile("(0x\S+)\s+\d+\s+\S+\s+\S+")
    dinstinfo = re.compile("\s+(0x\S+)\s+\S+\s+\S+")

    fd = open(file, "r")
    lastSeenIC = ""
    while 1:
        
        line = fd.readline()
        last_pos = fd.tell()
        if not line:
            break
        KIND = kind.findall(line)
        DINST = dinstinfo.findall(line)
        DINSTLINE = []
        if KIND:
            while 1:
                instline = fd.readline()
                if not instline:
                    break
                DUMMYKIND = kind.findall(instline)
                DINSTLINE = dinstinfo.findall(instline)
                INSTLINE = instinfo.findall(instline)
                if DINSTLINE:
                    break                
                if DUMMYKIND:
                    break
                if INSTLINE:
                    l.append(INSTLINE[0])
            if KIND[0] in dummyk.keys():
                sameCount[KIND[0]] += 1
            else:
                sameCount[KIND[0]] = 0
            dummyk[KIND[0]] = l
            ic.append(l)
            k[KIND[0] + "#" + str(sameCount[KIND[0]])] = l
            countMap[KIND[0] + "#" + str(sameCount[KIND[0]])] = 0
        l = []
        VALIDDINST = DINST or DINSTLINE
        if VALIDDINST:
            for i in reversed(ic):
                changed = 0
                if VALIDDINST[0] in i:
                    for key in k.keys():
                        if((k[key] == i) and (lastSeenIC != key)):
                          lastSeenIC = key
                          countMap[key] += 1
                          changed = 1
                if changed == 1:
                    break 
    fd.close()
    
if __name__ == "__main__":
    staticTrace = sys.argv[1]
    icCount(staticTrace)

    od = collections.OrderedDict(sorted(k.items()))
    print "IC_Name  ", "Reused Count  ", "Size of the IC (No. of Instructions)"
    for key, value in od.items():
        print key, "\t", countMap[key], "\t", len(od[key])

    
    
    

