import random
import itertools
import csv
#######################################################################
def int2node(i):
    return "( node_"+str(i)+" id )"
def intint2q(i,j):
    return "q_"+str(i)+"to"+str(j)
def genNoisyOrBody(parents,i):
    return genNoisyOrBodyString(parents,i,"") 
    
def genNoisyOrBodyString(parents,i,brac):
    if not parents:
        return " 0.000001 "+ brac
    else:
        if len(parents)==1:
            orString =""
            brac+=" )"
        else:
            orString = "( probOr "
        brac+=" )"
        j=parents.pop()
        return orString+" ( probAnd "+ int2node(j)+" "+intint2q(j, i)+" ) " + genNoisyOrBodyString(parents, i, brac) 


########################################################################

def importMyData(name):
    matrix=[]
    for line in open(name):
        arr=[]
        for value in line.rstrip('\n').split(','):
            arr.append(float(value))
        matrix.append(arr)    
    return matrix

######################################################################



def getParents(dag,i):
    col = column(dag, i)
    return [index for index in range(len(col)) if col[index]==1 ]   
######################################################################
def findsubsets(S,m):
    return list(itertools.combinations(S, m))
def findAllsubsets(S):
    outS=[]
    for i in range(len(S)):
        outS.extend(findsubsets(S, i))
    outS.append(tuple(S))
    outS = outS[::-1]
    return outS
######################################################################
def generateNoisyOrData(dag,n,q):
    data = [[0 for i in range(len(dag))]for j in range(n)]
    for i in range(len(dag)):
        parents = getParents(dag, i)
        probs=[0.5,0.5]
        if not parents:
            for j in range(n):
                data[j][i]=sampleDiscrete(probs)
        else:
            for j in range(n):
                q_effect =1

                for parent in parents:
                    if data[j][parent]==1:
                        q_effect*=q[parent]
                #print(q_effect)
                print("########")
                print(q_effect)
                print("########")
                data[j][i]=sampleDiscrete([q_effect,1-q_effect])
    return data
######################################################################      
def generateNoisyOrBooleanDataOld(dag,n,q):
    data = [[0 for i in range(len(dag))]for j in range(n)]
    for i in range(len(dag)):
        parents = getParents(dag, i)
        probs=[0.5,0.5]
        if not parents:
            for j in range(n):
                data[j][i]=int2bool(sampleDiscrete(probs))
        else:
            for j in range(n):
                q_effect =1
                for parent in parents:
                    if data[j][parent]=='true':
                        q_effect*=q[parent]
                #print(q_effect)
                data[j][i]=int2bool(sampleDiscrete([q_effect,1-q_effect]))
    return data

######################################################################      
######################################################################      
def generateNoisyOrBooleanData(dag,n,q):
    data = [[0 for i in range(len(dag))]for j in range(n)]
    for i in range(len(dag)):
        parents = getParents(dag, i)
        probs=[0.5,0.5]
        if not parents:
            for j in range(n):
                data[j][i]=int2bool(sampleDiscrete(probs))
        else:
            for j in range(n):
                q_effect =1
                for parent in parents:
                    if data[j][parent]=='true':
                        q_effect*=q[parent][i]
                #print(q_effect)
                data[j][i]=int2bool(sampleDiscrete([q_effect,1-q_effect]))
    return data

######################################################################      
######################################################################      
def generateNoisyOrData2(dag,n,q):
    data = [[0 for i in range(len(dag))]for j in range(n)]
    for i in range(len(dag)):
        parents = getParents(dag, i)
        probs=[0.5,0.5]
        if not parents:
            for j in range(n):
                data[j][i]=sampleDiscrete(probs)
        else:
            for j in range(n):
                q_effect =1
                for parent in parents:
                    if data[j][parent]==1:
                        q_effect*=q[parent][i]
                #print(q_effect)
                data[j][i]=sampleDiscrete([q_effect,1-q_effect])
    return data

######################################################################      
def sampleDiscrete(probs): # samples discrete values from a distribution
    sortedProbabilites = [i[1] for i in sorted(enumerate(probs), key=lambda x:x[1])]
    indeces = [i[0] for i in sorted(enumerate(probs), key=lambda x:x[1])]
    randUni=random.uniform(0,1)
    #print randUni
    for i in range(len(probs)):
        if i>0:
            sortedProbabilites[i]=sortedProbabilites[i]+sortedProbabilites[i-1]
        if randUni<sortedProbabilites[i]:
            break
    return indeces[i]
###################################################################### 
def column(matrix,i): #returns a column of a matrix
    return [row[i] for row in matrix]
######################################################################
def int2bool(int):
    if int==1:
        return 'true'
    else: return 'false'
def writeMyCSV(name,matrix):
    with open(name, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(matrix)
'''    
    
N = 10

dag=[[0,1,1],[0,0,1],[0,0,0]]
#data =generateNoisyOrBooleanDataOld(dag,N,q)
#q=[0.1,0.3,0.8]
q=[[0,0.5,0.1],[0,0,0.3],[0,0,0],[0,0,0]]
data =generateNoisyOrBooleanData(dag,N,q)
for line in data:
    print line
'''        