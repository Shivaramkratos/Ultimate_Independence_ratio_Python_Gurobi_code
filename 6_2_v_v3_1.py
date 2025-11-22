import numpy as np; import scipy as sp; import networkx as nx;
import gurobipy as gp
options = {
    "WLSACCESSID": "-", # Enter Gurobi license details here, this assumes you have WLS license
    "WLSSECRET": "-",
    "LICENSEID": -,
}
from gurobipy import GRB

k = 6; # Number of vertices in the Wheel
w = nx.wheel_graph(k); 
g = nx.cartesian_product(w,w); # This constructs Wheel^2
n = nx.number_of_nodes(g); e = nx.number_of_edges(g); 
B = nx.incidence_matrix(g); B = np.abs(B); 
je = np.ones([1,e]); jn = np.ones([1,n]); h = np.zeros([1,n]); # This are required vectors to setup the Integer Program
alpha = 11; # This is independene number of W_5^2, use the formula [((k-1)*(k-2)/2) + 1] if working with W_k^2

with gp.Env(params=options) as env:
    m = gp.Model("W5pow4_Ind", env=env)

# adding variable x 
    x = m.addMVar((k,n), vtype=GRB.BINARY, name="x") # Adding indicator vector on each vertex of the W_k, so this constructs W_k^3

# Maximize LP for independence number
    m.setObjective(x.sum(),GRB.MAXIMIZE)
# Constraints for the LP
    for i in range(k):
        m.addConstr(x[i,:] @ B <= je) # These constraints makes each indicator vector an independent set on W_k^2
        m.addConstr(x[i,:] >=h)
        m.addConstr(x[i,:].sum() <= alpha) # Auxillary constraint, but reduces search space

    
    for i in range(1,k-1):
        m.addConstr(x[0,:] + x[i,:] <= jn) # These add disjointness of ind sets along the edges of wheel
        m.addConstr(x[i,:] + x[i+1,:] <= jn)

    m.addConstr(x[1,:] + x[k-1,:] <= jn)
    m.addConstr(x[0,:] + x[k-1,:] <= jn)

    # These next constraints allow finer control of ind sets, here is we include values which are specific to W_5^2
    m.addConstr(x[0,:].sum() == 8)
    m.addConstr(x[1,:].sum() == 11)
    m.addConstr(x[2,:].sum() == 9)
    m.addConstr(x[3,:].sum() == 9)
    m.addConstr(x[4,:].sum() == 11)
    m.addConstr(x[5,:].sum() == 10)



# trying tune the problem
    m.params.Threads = 8
    m.params.Method = 2
    m.params.Cuts = -1
    m.params.Heuristics = 1
    m.params.RINS = 1
    m.params.ImproveStartNodes = 1
    m.params.ImproveStartTime = 1
    m.params.MIPFocus = 3
# Solve the problem
    m.optimize()

#print(f"{m.ObjVal:.0f}")
