# This computes the maximum independent set of W5 box K3 using three variables for each independent set in the traingle structure.

import numpy as np; import scipy as sp; import networkx as nx;
import matplotlib.pyplot as plt; import csv; import random; 
import gurobipy as gp
options = {
    "WLSACCESSID": "c213c390-45b2-4161-9e09-8bf82cb89f34",
    "WLSSECRET": "c1981d5a-9626-416b-b16d-9fd0c8d67764",
    "LICENSEID": 2650983,
}
from gurobipy import GRB

k = 6;
w = nx.wheel_graph(k); 
g = nx.cartesian_product(w,w); #g = nx.cartesian_product(g,w); # Definition of the graph g 
n = nx.number_of_nodes(g); e = nx.number_of_edges(g);
g = nx.convert_node_labels_to_integers(g, first_label=0, ordering='default', label_attribute=None); # making the labels of g from vector coords to [0,1,2,...,n]
B = nx.incidence_matrix(g); B = np.abs(B);  # This is the incidence matrix
je = np.ones([1,e]); jn = np.ones([1,n]); h = np.zeros([1,n]); # Ones and zeroes vector
alpha = 11; # If alpha of the underlying graph $g$ is already known, then use that value as another constraint

m = gp.Model("W5pow4_Ind")

# adding variable x 
x = m.addMVar((3,n), vtype=GRB.BINARY, name="x") # Three rows, each of them being a seperate ind set in g

# Maximize LP for independence number
m.setObjective(x.sum(),GRB.MAXIMIZE)
# Constraints for the LP
for i in range(3):  # These are conditions that specify that each row is ind set in g 
    m.addConstr(x[i,:] @ B <= je)
    m.addConstr(x[i,:] >=h)
    m.addConstr(x[i,:].sum() <= alpha)

m.addConstr(x[0,:] + x[1,:] <= jn)  # Each of these constraints specify that rows are disjoint (since in the cartesian product every edge in traingle results in disjoint ind sets in Whole graph)
m.addConstr(x[1,:] + x[2,:] <= jn)
m.addConstr(x[2,:] + x[0,:] <= jn)
m.addConstr(x[2,:] + x[1,:] + x[0,:] <= jn) # All three of them are disjoint together, this is not necessarily required, but speeds up the Gurobi solver


# trying tune the problem, these are some tuning parameters, can be removed or extra can be added to speed up the search.
m.params.Threads = 8
m.params.Method = 2
m.params.Cuts = 3
m.params.Heuristics = 1
m.params.RINS = 1
m.params.ImproveStartNodes = 1
m.params.ImproveStartTime = 1
m.params.MIPFocus = 3

# Solve the problem
m.optimize()

#print(f"{m.ObjVal:.0f}")

x_val = np.abs(x.X); # This is the solution which Gurobi obtained written into python.  

