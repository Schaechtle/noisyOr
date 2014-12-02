import matplotlib
matplotlib.use('Agg')
from DAGutil import dag2graph_unsorted,topolgical_sort
from venture import shortcuts
from venture.unit import VentureUnit
from util import generateNoisyOrData2,int2node,intint2q
from sets import Set
global dag,q,N 
N =200
dag=[[0,0,1],[0,0,1],[0,0,0]]
q=[[0,0,0.1],[0,0,0.3],[0,0,0]]
class NoisyOr(VentureUnit):
 

    def generateQs(self,sortGraph):
        baseline=Set([])
        block  = 0
        for item in sortGraph:
            for node in item[1]:
                #print(" v.assume(q_"+str(item[0])+"to"+str(node),"(uniform_continuous 0 1)")
                self.assume("q_"+str(item[0])+"to"+str(node),"(scope_include (quote hypers) "+str(block)+" (uniform_continuous 0 1))")
                block+=1
                baseline.add(node)
        for item in baseline:
            self.assume("q_baseline_"+str(item),"(scope_include (quote hypers) "+str(block)+" (uniform_continuous 0 1))")
            block+=1
       
    def genNoisyOrBodyString(self,parents,i,brac):
        if not parents:
            return " q_baseline_"+str(i)+ " ) "+ brac
        else:
            if len(parents)==1:
                j=parents.pop()        
                if not brac:
                    addBrac="))"
                else:
                    addBrac=""                
                return " ( probAnd "+ int2node(j)+" "+intint2q(j, i)+" )" +brac+ self.genNoisyOrBodyString(parents, i, brac+addBrac) 
            else:
                brac+=" )"
                j=parents.pop()
                return "( probOr  ( probAnd "+ int2node(j)+" "+intint2q(j, i)+" ) " + self.genNoisyOrBodyString(parents, i, brac) +" ) "

    
    def genNoisyOrBody(self,parents,i):
        return self.genNoisyOrBodyString(parents,i,"") 
    
    def generateNodes(self,sortGraph):
        parentLookup={}
        for item in sortGraph:
            if parentLookup.has_key(item[0]):
                # CAVEAT: printing assumption ruins recursion!!!
                #print "(mem (lambda (id) ( bernoulli (probOr  "+self.genNoisyOrBody(parentLookup[item[0]],item[0])+ ")"
                self.assume("node_"+str(item[0]),"(mem (lambda (id) ( bernoulli (probOr  "+self.genNoisyOrBody(parentLookup[item[0]],item[0])+ ")")
            else:
                #print("node_"+str(item[0]),"(mem (lambda (id)   ( bernoulli 0.5) ))")        
                self.assume("node_"+str(item[0]),"(mem (lambda (id)   ( bernoulli 0.5) ))")        
            for j in item[1]:
                    if j in parentLookup:
                        parentLookup[j].append(item[0])
                    else:                    
                        parentLookup[j]=[item[0]]
    def makeAssumes(self):
        unsGraph=dag2graph_unsorted(dag)
        sortGraphRev=topolgical_sort(unsGraph)
        sortGraph=sortGraphRev[::-1]
        self.clear()
        self.generateQs(sortGraph)
        self.assume("probOr","(lambda (a b) ( - ( + a b ) ( * a b) ))")
        self.assume("probAnd","(lambda (a b) ( * a b ))")
        self.generateNodes(sortGraph)
        
    def makeObserves(self):
        data =generateNoisyOrData2(dag,N,q)
        for n in range(N):
            self.observe("(node_0 %d)" % n, data[n][0])
            self.observe("(node_1 %d)" % n, data[n][1])
            self.observe("(node_2 %d )" % n, data[n][2])

if __name__ == '__main__':
    model = NoisyOr(shortcuts.make_church_prime_ripl())
    model.makeAssumes()
    model.makeObserves()
    def statisticsInfer(ripl, _):
    # ripl.infer("(cycle ((mh hypers one 5) (mh parameters one 20) (mh clustering one 80)) 10)")
        ripl.infer("(mh hypers one 5)")    
    def gibbsInfer(ripl, _):
    # ripl.infer("(cycle ((mh hypers one 5) (mh parameters one 20) (pgibbs clustering ordered 2 1)) 10)")
        ripl.infer("(gibbs hypers one  2)")

    # ripl.infer("(cycle ((mh hypers one 5) (mh parameters one 20) (mh clustering one 80)) 10)")
    def statisticsInferAll(ripl, _):
        ripl.infer("(mh hypers all 2)")  





def run(arg):
    name = arg[0]
    inference = arg[1]


    history = model.runFromConditional(100, runs=5, verbose=True, name=name, infer=inference)
    print "average value q_0to2: ",1-history[0].averageValue("q_0to2")
    print "average value q_1to2: ",1-history[0].averageValue("q_1to2")
#    print "average value q_0to1: ",1-history[0].averageValue("q_0to1")
    print "average value q_baseline_2: ", history[0].averageValue("q_baseline_2")
 #   print "average value q_baseline_1: ", history[0].averageValue("q_baseline_1")

    history[0].plot(fmt='png')
 

from multiprocessing import Pool
pool = Pool(30)
pool.map(run, [("statisticsInfer", statisticsInfer)])
#print postQa

