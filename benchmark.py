import re
import sys
import os

def benchmark(file):
    inst = 0
    binst = 0
    kind = re.compile("kind = \S+IC")
    bopcode = re.compile("\S+\s+\S+\s+\S+\s+(b|beq|bne|cbz|cbnz|bl|blx|bx|tbb|tbh)\s+\S+")
    ldopcode = re.compile("\S+\s+\S+\s+\S+\s+(l\S+)\s+pc,\s+\S+")

    opcode = re.compile("0x\S+\s+\S+\s+\S+\s+\S+")
    constpool = re.compile("\S+\s+\S+\s+\S+\s+constant")
    fd = open(file, "r")
    while 1:
        line = fd.readline()
        last_pos = fd.tell()
        if not line:
            break
        KIND = kind.findall(line)
        if KIND:
            while 1:
                line1 = fd.readline()
                if not line1:
                    break
                BOPCODE = bopcode.findall(line1)
                LDOPCODE = ldopcode.findall(line1)
                OPCODE = opcode.findall(line1)
                CONSTPOOL = constpool.findall(line1)
                if CONSTPOOL:
                    break
                if OPCODE:
                    inst += 1
                    if BOPCODE or LDOPCODE:
                        binst += 1
        fd.seek(last_pos)
                
                          
    fd.close()
    print binst, inst    

if __name__ == "__main__":
    benchmarkfile = sys.argv[1]
    benchmark(benchmarkfile)

