Venture-based algorithm for a Noisy-or Bayesian Network parameter estimation. 

Implemented using runFromConditional. Assumptions are generated via python-processing of a DAG-linkmatrix. For more complex DAGs it is necessary to increase the number of sweeps/mcmc steps. An MRIPL-if branching based implementation seemed much slower than the current one. AND/OR have been re-implemented to strange behavoiur of the build in functions while propagating bernoulli distributions (i.e. it converted from double to boolean in one case but not in the other; [ASSUME becomesDouble  (or 0 0) >>>  0],[ASSUME becomesBoolean  (or 1 0) >>> True]). Further experiments regarding performance are planned. 

To test, simply run Python NoisyOrBnet.py.

For testing other DAGs and more/less data/observations simply change line 9-11 in NoisyOrBnet.py, which is currently set to:
N =200
dag=[[0,0,1],[0,0,1],[0,0,0]]
q=[[0,0,0.1],[0,0,0.3],[0,0,0]]



