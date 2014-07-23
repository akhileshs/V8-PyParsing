import re
import sys
import os

def dtrace(file):
    inst = 0
    binst = 0
    taken = 0
    nTaken = 0
    opcode = re.compile("(0x\S+)\s+\S+\s+\S+")
    bopcode = re.compile("(0x\S+)\s+\S+\s+(b|cbz|cbnz|bl|blx|bx|tbb|tbh)(\s+|\S+)")
    ldopcode = re.compile("(0x\S+)\s+\S+\s+(ld\S+)\s+pc,\s+\S+")
    fd = open(file, "r")
    while 1:
        line = fd.readline()
        last_pos = fd.tell()
        if not line:
            break
        OPCODE = opcode.findall(line)
        BOPCODE = bopcode.findall(line)
        LDOPCODE = ldopcode.findall(line)
        if OPCODE:
            inst += 1
            if BOPCODE:
                binst += 1
                targetline = fd.readline()
                TARGET = opcode.findall(targetline)
                if TARGET and BOPCODE:
                    if (int(TARGET[0],16) - int(BOPCODE[0][0],16) == 4):
                        nTaken += 1
                    else:
                        taken += 1
               
        fd.seek(last_pos)
    fd.close()
    print "Total Instructions: ",inst, " Branch Instructions:  ", binst, " Taken Branches: ", taken, " Branches Not Taken: " ,nTaken

if __name__ == "__main__":
    dtraceFile = sys.argv[1]
    dtrace(dtraceFile)



