import re
import sys
import os

btb = {}
correct = 0
incorrect = 0
total = 0
size = 4096
mask = 0x03FF
actualBranchTarget = ""
def btbAddress(file):
    global actualBranchTarget
    branch = re.compile("(0x\S+)\s+\S+\s+(b|beq|bne|cbz|cbnz|bl|blx|bx|tbb|tbh)\s+\S+\s+\S+\s+(0x\S+)")
    address = re.compile("(0x\S+)\s+\S+\s+\S+")
    fd = open(file, "r")
    while 1:
        line = fd.readline()
        if not line:
            break
        last_pos = fd.tell()
        nextLine = fd.readline()
        if not nextLine:
            break
        ADDRESS = address.findall(nextLine)
        if ADDRESS:
          actualBranchTarget = ADDRESS[0]
        
        BRANCH = branch.findall(line)
        if BRANCH:
            if ((BRANCH[0][0] not in btb.keys()) and (len(btb) != size)):
              index = mask & int(BRANCH[0][0], 16)
              btb[index] = [0, 1, BRANCH[0][2], 0, 1]  #prediction, state, target address, simple initilization
            else:
              insert(BRANCH[0][0], BRANCH[0][2], btb[index][0])
            
            btb[index][3] += 1
            predict(BRANCH[0][0], BRANCH[0][2], btb[index][0])                               #add all branch instructions to the dictionary
        
        fd.seek(last_pos)

    fd.close()

def lookupTarget(ptr):                           #lookup address and return target address
    index = mask & int(ptr, 16)
    if (index in btb.keys()):
        return btb[index][2]
    return 0

def lookupBTB(ptr):
    index = mask & int(ptr, 16)
    return index in btb.keys()

def prediction(ptr):                      #return prediction for a branch  
    index = mask & int(ptr, 16)
    if (btb[index][1] == 1 or btb[index][1] == 0):
        btb[index][0] = 0
    if (btb[index][1] == 2 or btb[index][1] == 3):
        btb[index][0] = 1

    return btb[index][0]

def updateCounter(ptr, target, correct): #update 2-bit saturating counter
    index = mask & int(ptr, 16)

    if ((correct == True) and btb[index][1] == 3):
        btb[index][1] = 3
    if ((correct == True) and btb[index][1] == 2):
        btb[index][1] = 3
    if ((correct == False) and btb[index][1] == 3):
        btb[index][1] = 2
    if ((correct == False) and btb[index][1] == 2):
        btb[index][1] = 0

    if ((correct == True) and btb[index][1] == 0):
        btb[index][1] = 1
    if ((correct == True) and btb[index][1] == 1):
        btb[index][1] = 3
    if ((correct == False) and btb[index][1] == 0):
        btb[index][1] = 0
    if ((correct == False) and btb[index][1] == 1):
        btb[index][1] = 0

    if (btb[index][1] == 3 or btb[index][1] == 2):
        btb[index][2] = target
        btb[index][0] = 1
    else:
        btb[index][0] = 0


def insert(ptr, target):
    index = mask & int(ptr, 16)
    btb[index][4] = 1
    btb[index][0] = 1
    btb[index][2] = target
    btb[index][1] = 2

def predict(ptr, target, taken):            #primary prediction mechanism
    global correct, incorrect, total, actualBranchTarget
    total += 1
    if lookupBTB(ptr):
        if ((prediction(ptr) == taken) and (lookupTarget(ptr) == actualBranchTarget)): #check line
            correct += 1
            updateCounter(ptr, target, 1)
        else:
            updateCounter(ptr, target, 0)
    else:
        if (taken != 0):
            correct += 1
        else:
            insert(ptr, target)


                        
if __name__ == "__main__" :
    btbfile = sys.argv[1]
    btbAddress(btbfile)
    print "correct ", correct, "total: ", total
    print "BTB HIT%: ", correct/float(total)*100

