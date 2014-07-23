import re
import sys
import os

def bpredictparse(file):
    pava = re.compile("pa:\s+(\S+),\s+va:\s+(\S+)")
    opcode = re.compile("\S+\s+:\s+(b|cbz|cbnz|bl|blx|bx|tbb|tbh)\S+")
    fd = open(file, "r")
    while 1:
        line1 = fd.readline()
        if not line1:
            break
        PAVA = pava.findall(line1)

        if PAVA:
            line2 = fd.readline()
            OPCODE = opcode.findall(line2)
            if OPCODE:
                targetline = fd.readline()
                TARGET = pava.findall(targetline)
                if TARGET:
                    if (int(TARGET[0][0],16) - int(PAVA[0][0],16) == 4):
                        print PAVA[0][0] + ", " + PAVA[0][1] + ", " + "0"
                    else:
                        print PAVA[0][0] + ", " + PAVA[0][1] + ", " + "1"
                             
        
    fd.close();

if __name__ == "__main__":
    tracefile = sys.argv[1]
    bpredictparse(tracefile)



        
