import sys
sys.setrecursionlimit(10000)

class Point:
    def __init__(self, id: int, x: float, y: float):
        self.id=id
        self.x=x
        self.y=y
        self.defined=False 
        self.neighbor=[]

def expand(p, seedSet):
    for q in p.neighbor:
        if q.defined:
            continue
        q.defined =True
        seedSet.append(q)

        if len(q.neighbor) >= Minpts:
            expand(q,seedSet)
        
def findNeighbors(p):
    neighbors=[]
    for q in DB:
        if p.id==q.id:
            continue
        if dist(p,q):
            neighbors.append(q)
    p.neighbor=neighbors

def dist(p,q):
    r=(p.x-q.x)*(p.x-q.x)+(p.y-q.y)*(p.y-q.y)
    if r <=Eps*Eps:
        return True

    return False


def main():
    global Eps, Minpts, DB
    fileName= sys.argv[1]
    n = int (sys.argv[2])
    Eps = float(sys.argv[3])
    Minpts = int(sys.argv[4])
    DB=[]
    Cluster=[]

    #file 읽기
    f=open(fileName,'r')
    while True:
        line = f.readline()
        if not line:
            break
        id,x,y=line.split()
        DB.append(Point(int(id),float(x),float(y)))
    
    f.close()
    
    #find neighbors
    for p in DB:
        findNeighbors(p)

    #DBscan
    for p in DB:
        if p.defined:
            continue
        N=len(p.neighbor)
        if N<Minpts:
            continue
        p.defined=True
        seedSet=[p]
        expand(p, seedSet)
        
        Cluster.append(seedSet)

    #output 
    if len(Cluster)>n:
        Cluster=sorted(Cluster, key=len, reverse=True)

    for i in range(n):
        outputFile = "input" + fileName[5]+"_cluster_"+str(i)+".txt"
        f=open(outputFile, 'w')
        for j in Cluster[i]:
            k=str(j.id)
            f.write(k+'\n')

        f.close()
        
if __name__=="__main__":
    main()