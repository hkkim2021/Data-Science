import sys
from itertools import combinations

minSup = int(sys.argv[1])
inputFile=open (sys.argv[2],"r") 
outputFile = open(sys.argv[3], 'w')
transactions = []
frequentPattern = []
c1_itemSet=[]
dbSize = 0
minSupFreq = 0

def readInput():
    global transactions, dbSize, minSupFreq,c1_itemSet
    while True:
        line=inputFile.readline()
        if not line:
            break
        transactions.append(line.split())
        for i in line.split():
            c1_itemSet.append(i)
    c1_itemSet=set(c1_itemSet)
    dbSize=len(transactions)
    minSupFreq=minSup*dbSize/100
    transactions=setList(transactions)
    inputFile.close()

def setList(oldList):
    newSet= []
    for i in oldList:
        newSet.append(set(i))
    return newSet

def getFreq(itemSet):
    freq=0
    for i in transactions:
        if itemSet == itemSet.intersection(i):
            freq +=1
    return freq

def getSup(itemSet):
    freq=getFreq(itemSet)
    if freq >= minSupFreq:
        return freq / dbSize
    else:
        return 0

def getConf(itemSet, associative_itemSet):
    t=getFreq(itemSet | associative_itemSet)
    p=getFreq(itemSet)
    if t==0:
        return 0
    else:
        return t/p

def selfJoin(itemSet, k):
    t = set()
    for i in itemSet:
        t=t.union(i)
    p=combinations(t,k)
    p=setList(list(p))
    return p

def pruning(c_itemSet):
    t = []
    for c in c_itemSet:
        getFreq(c)
        if getFreq(c)>= minSupFreq:
            t.append(c)
    return t

def getAssociative(itemSet, outputFile):
    if len(itemSet) == 1:
        return
    itemSet_comb = [set(combination) for i in range(1, len(itemSet)) for combination in combinations(itemSet, i)]
    for prev in itemSet_comb:
        next = itemSet - prev
        if len(prev & next )== 0 and (prev | next) == itemSet:
            union = prev | next
            support = getSup(union)
            if support > 0:
                confidence = getConf(prev, next)
                line = f"{getResult(prev)}\t{getResult(next)}\t{support * 100:.2f}\t{confidence * 100:.2f}\n"
                outputFile.write(line)


def getResult(itemSet):
    sorted_items = sorted(map(int, itemSet))
    return "{" + ",".join(map(str, sorted_items)) + "}"

def apriori():
    global frequentPattern
    k=1
    C=[]
    C = [{i} for i in c1_itemSet]
    
    while True:
        L = pruning(C)
        frequentPattern.extend(L)
        if len(L) == 0:
            break
        k += 1
        C= selfJoin(L, k)


def main():
    readInput()
    apriori()
    for itemSet in frequentPattern:
        getAssociative(itemSet,outputFile)
    outputFile.close()


if __name__ == '__main__':
    main()