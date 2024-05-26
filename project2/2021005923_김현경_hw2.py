import sys
import numpy as np

class Node:
    def __init__(self, myDb,myAttrList):
        self.myDb=myDb #내 database
        self.myClassLabel=None# 예측 레이블
        self.selectAttr=None#분기 조건으로 선택된 attribute
        self.myAttrList=myAttrList#여태까지 분기에 사용된 attribute
        self.children=[]#자식 노드 
        self.isLeaf=False #리프 노드인지 확인
    
    def info(self,db):
        #p_i=현재 노드에서 클래스 i의 값/전체 갯수
        entropy=0
        for label in classLabel:
            count=0
            for subset in db:
                if label==subset[-1]:
                    count+=1
            p_i=count/len(db)
            if p_i>0:
                entropy-=p_i*np.log2(p_i)

        return entropy

    def info_a(self,db, attrIndex):
        #시그마(j=1~feature valuesr개수) feature_j의 데이터 갯수/node전체의 갯수 *info(Dj)
        attrValues=set(subset[attrIndex] for subset in db)
        D=len(db)
        entropy=0

        for attrValue in attrValues:
            nextSubset=[]
            for subset in db:
                if subset[attrIndex]==attrValue:
                    nextSubset.append(subset)
            D_i=len(nextSubset)
            entropy+=(D_i/D)*self.info(nextSubset)

        return entropy

    def gain_a(self,db,attrIndex):
        #info-info_a
        return self.info(db)-self.info_a(db, attrIndex)

    def splitInfo(self,db,attrIndex):
        #-시그마(j=1~feature valuesr개수) feature_j의 데이터 갯수/node전체의 갯수*log2((j=1~feature valuesr개수) feature_j의 데이터 갯수/node전체의 갯수)
        attrValues=set(subset[attrIndex] for subset in db)
        D=len(db)
        result=0

        for attrValue in attrValues:
            nextSubset=[]
            for subset in db:
                if subset[attrIndex]==attrValue:
                    nextSubset.append(subset)
            D_i=len(nextSubset)
            result-=(D_i/D)*np.log2(D_i/D)

        return result

    def gainRatio_a(self,db,attrIndex):
        #gain_a()/splitInfo()
        if self.splitInfo(db,attrIndex)==0:
            return 0
        return self.gain_a(db,attrIndex)/self.splitInfo(db,attrIndex)
    
    def select_label(self,db):
        #class label선택
        selectedLabel=None
        max=0
        for label in classLabel:
            count=0
            for subset in db:
                if(label==subset[-1]):
                    count+=1
            if count>max:
                max=count
                selectedLabel=label
        
        return selectedLabel

    def select_attr(self,db):
        #분기할 조건 고르기
        max=0
        selectedIndex=None

        for attrIndex in range(len(attrList)-1):
            if attrList[attrIndex] in self.myAttrList:
                continue
            if self.gainRatio_a(db,attrIndex)>max:
                max=self.gainRatio_a(db,attrIndex)
                selectedIndex=attrIndex
        
        return selectedIndex

    def build_decision_tree(self):
        #decision_tree구축
        #1.myclassLabel 구하기
        self.myClassLabel=self.select_label(self.myDb)
        #2.entropy 구해서 만약 0이면 리프노드로 바꾸고 return 
        entropy=self.info(self.myDb)
        if entropy==0:
            self.isLeaf=True
            return
        #3.만약 더 이상 사용할 attribute가 없다면 리프노드로 바꾸고 return
        if len(self.myAttrList)==len(attrList)-1:
            self.isLeaf=True
            return
        #4.분기할 attribute 구하기
        selectedIndex=self.select_attr(self.myDb)
        self.selectAttr=attrList[selectedIndex]

        nextAttrList=self.myAttrList.copy()
        nextAttrList.append(attrList[selectedIndex])

        #4.그 attribute의 feature들에 따라서 db를 분리
        #5.자식노드를 생성해 추가한다
        #6.각 자식들도 tree를 구축한다.
        attrValues=set(subset[selectedIndex] for subset in self.myDb)
        for attrValue in attrValues:
            child_db=[]
            for subset in self.myDb:
                if subset[selectedIndex]==attrValue:
                    child_db.append(subset)
            child_node=Node(child_db,nextAttrList)
            self.children.append(child_node)
            child_node.build_decision_tree()
           

    def classify(self,line):
        #class_label 판단
        #leaf node일 경우
        if self.isLeaf :
            return self.myClassLabel
        #현재 노드의 분기조건 attribute 의 value값 확인
        value=line[attrList.index(self.selectAttr)]
        #그 value값을 갖고 있는 자식 노드가 있는지 확인
        for child in self.children:
            if child.myDb[0][attrList.index(self.selectAttr)]==value:
                return child.classify(line) 
        return self.myClassLabel

        

def main():
    trainFile=open(sys.argv[1],'r')
    testFile=open(sys.argv[2],'r')
    resultFile=open(sys.argv[3],'w')

    global db,attrList,classLabel,classIndex
    db=[]
    attrList=[]
    classLabel=set()

    attrList=trainFile.readline().split()
    classIndex=len(attrList)-1    #class결정한는 요소가 몇 번째인지 계산

    while True:
        line=trainFile.readline().split()
        if not line:
            break
        db.append(line)
        classLabel.add(line[-1])

    classLabel=list(classLabel)

    decision_tree=Node(db,[])
    decision_tree.build_decision_tree()

    trainFile.close()

    #test파일 ->result작성
    testFile.readline().split()
    result_attribute="\t".join(attrList)+"\n"  #젤 위에 attribute 
    resultFile.write(result_attribute)

    while True:
        line=testFile.readline().split()
        if not line:
            break
        result=decision_tree.classify(line)
        line.append(result)
        result_line="\t".join(line)+"\n"
        resultFile.write(result_line)

    testFile.close()
    resultFile.close()

if __name__ == '__main__':
    main()