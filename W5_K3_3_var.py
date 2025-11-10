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
g = nx.cartesian_product(w,w); #g = nx.cartesian_product(g,w);
n = nx.number_of_nodes(g); e = nx.number_of_edges(g);
g = nx.convert_node_labels_to_integers(g, first_label=0, ordering='default', label_attribute=None); 
B = nx.incidence_matrix(g); B = np.abs(B); 
je = np.ones([1,e]); jn = np.ones([1,n]); h = np.zeros([1,n]); 
alpha = 79;

m = gp.Model("W5pow4_Ind")

# adding variable x 
x = m.addMVar((3,n), vtype=GRB.BINARY, name="x")

# Maximize LP for independence number
m.setObjective(x.sum(),GRB.MAXIMIZE)
# Constraints for the LP
for i in range(3):
    m.addConstr(x[i,:] @ B <= je)
    m.addConstr(x[i,:] >=h)
    m.addConstr(x[i,:].sum() <= alpha)

m.addConstr(x[0,:] + x[1,:] <= jn)
m.addConstr(x[1,:] + x[2,:] <= jn)
m.addConstr(x[2,:] + x[0,:] <= jn)
m.addConstr(x[2,:] + x[1,:] + x[0,:] <= jn)

#m.addConstr(x[0,:].sum() == 11)
#m.addConstr(x[1,:].sum() == 9)
#m.addConstr(x[2,:].sum() == 9)


# trying tune the problem
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

x_val = np.abs(x.X); 

