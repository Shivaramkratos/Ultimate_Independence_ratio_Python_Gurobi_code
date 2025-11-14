import numpy as np; import scipy as sp; import networkx as nx;
import matplotlib.pyplot as plt; import csv; import random; 
import gurobipy as gp 
import math
options = {
    "WLSACCESSID": "c213c390-45b2-4161-9e09-8bf82cb89f34", # Need to hide at the end
    "WLSSECRET": "c1981d5a-9626-416b-b16d-9fd0c8d67764",
    "LICENSEID": 2650983,
}
from gurobipy import GRB

k = 10; w = nx.wheel_graph(k); g = nx.cartesian_product(w,w); # This defines the Wheel^2

A1 = [];
for i in range(1,k):
    A1.append((i,0)); A1.append((0,i)); # A1 is set [(i,0), (0,i)]
A2 = A1.copy(); A2.append((0,0)); A2 = list(A2); 
V = list(g.nodes()); 
A2 = [item for item in V if item not in A2]; # A2 = [(i,j)] 
V = A1 + A2; # We order total vertices according to A1, A2

h1 = g.subgraph(A1); h2 = g.subgraph(A2); # induced subgraphs of A1, A2
g.remove_node((0,0)); # Since the only maximal profile which contains (0,0) is (1, 0 , alpha-1), we don't need this for rest of profiles
n = nx.number_of_nodes(g); e = nx.number_of_edges(g); 
B = nx.incidence_matrix(g, nodelist=V); B = np.abs(B); # This defines incidence matrix according to ordering of [A1,A2]
je = np.ones([1,e]); jn = np.ones([1,n]); h = np.zeros([1,n]);  # These definition are for total independence set excluding (0,0)


B1 = nx.incidence_matrix(h1, nodelist=A1); B2 = nx.incidence_matrix(h2, nodelist=A2); 
B1 = np.abs(B1); B2 = np.abs(B2); # these are to control size in smaller ind sets

n1 = nx.number_of_nodes(h1); e1 = nx.number_of_edges(h1); # These are required to set up the first LP to find the profiles
n2 = nx.number_of_nodes(h2); e2 = nx.number_of_edges(h2);

je1 = np.ones([1,e1]); jn1 = np.ones([1,n1]); h1 = np.zeros([1,n1]);
je2 = np.ones([1,e2]); jn2 = np.ones([1,n2]); h2 = np.zeros([1,n2]);

MPr= [(1, 0, math.floor(((k-1)*(k-2)/2)))]; # This is maximum independent set profile (1,0,alpha-1) and this list stores all the maximal profiles

for l in range(2,k-1): # to find profiles, this sets of value of ind set on A1, then tries largest ind set on A2 

    m = gp.Model("Maximal_profiles")

# adding variables x,y
    x = m.addMVar((1,n1), vtype=GRB.BINARY, name="x") # independent set on A1 = (i,0), (0,i)
    y = m.addMVar((1,n2), vtype=GRB.BINARY, name="y") # ind set on A2 = (i,j)

# Maximize LP given the value of x.sum()
    m.setObjective(y.sum(),GRB.MAXIMIZE)
# Constraints for the LP

    m.addConstr(x @ B1 <= je1) # This collects independent vertices from (i,0) and (0,i)
    m.addConstr(x >=h1)
    m.addConstr(x.sum() == l)
    m.addConstr(y @ B2 <= je2) # This collects independent vertices from (i,j)
    m.addConstr(y >=h2)
    xy = gp.hstack((x, y)) # this defines ind set on full Wheel^2
    m.addConstr(xy @ B <= je); # this makes (x,y) together independent on whole graph excluding (0,0)
    m.Params.OutputFlag = 0 # suppresses the outlog of Gurobi 
    m.optimize()
    
    MPr.append((0,l,math.floor(m.ObjVal))) # appending profile to the list

# With Maximal profiles, we compute X_f

m = gp.Model("chi_f of Wheel^2")

# adding variables a,b,c,t
a = m.addVar(name="a");b = m.addVar(name="b");c = m.addVar(name="c");t = m.addVar(name="t")


# Hahn-Hell-Poljak Maximal profile LP
m.setObjective(t,GRB.MINIMIZE)
# Constraints for the LP
for l in range(len(MPr)):
    m.addConstr(a*MPr[l][0] + b*MPr[l][1] + c*MPr[l][2] <=  t) # These are profile constraints 

m.addConstr(a + 2*(k-1)*b + (k-1)*(k-1)*c == 1) # This corresponds to normalization constraint
m.addConstr(a>= 0); m.addConstr(b >= 0); m.addConstr(c>= 0); m.addConstr(t >= 0) # non-negative constraint

m.optimize()
