# This is fractional chromatic number of W_9^3. 

import numpy as np; import scipy as sp; import networkx as nx;
import matplotlib.pyplot as plt; import csv; import random; 
import gurobipy as gp 
import math
options = {
    "WLSACCESSID": "c213c390-45b2-4161-9e09-8bf82cb89f34",
    "WLSSECRET": "c1981d5a-9626-416b-b16d-9fd0c8d67764",
    "LICENSEID": 2650983,
}
from gurobipy import GRB

def flatten_cartesian_product(G1, G2, G3):
    G = nx.cartesian_product(nx.cartesian_product(G1, G2), G3)
    mapping = {node: (*node[0], node[1]) for node in G.nodes()}
    return nx.relabel_nodes(G, mapping)

k = 10;
w = nx.wheel_graph(k);
g = flatten_cartesian_product(w,w,w);

A1 = [(0,0,0)]; A2 = []; A3 = []; A4 = [];
for i in range(1,k):
    A2.append((i,0,0)); A2.append((0,i,0)); A2.append((0,0,i));

for i in range(1,k):
    for j in range(1,k):
        A3.append((i,j,0));
        A3.append((i,0,j));
        A3.append((0,i,j));

A4 = A1+A2+A3; V = list(g.nodes()); 
A4 = [item for item in V if item not in A4]; V = A1 + A2 + A3 + A4;

h1 = g.subgraph(A1); h2 = g.subgraph(A2); h3 = g.subgraph(A3); h4 = g.subgraph(A4);

n = nx.number_of_nodes(g); e = nx.number_of_edges(g); 
B = nx.incidence_matrix(g, nodelist=V); B = np.abs(B);
je = np.ones([1,e]); jn = np.ones([1,n]); h = np.zeros([1,n]);  # These definition are for total independence set excluding (0,0)

B1 = nx.incidence_matrix(h1, nodelist=A1); 
B2 = nx.incidence_matrix(h2, nodelist=A2); 
B3 = nx.incidence_matrix(h3, nodelist=A3); 
B4 = nx.incidence_matrix(h4, nodelist=A4); 
B1 = np.abs(B1); B2 = np.abs(B2); B3 = np.abs(B3); B4 = np.abs(B4); # these are to control size in smaller ind sets

n1 = nx.number_of_nodes(h1); e1 = nx.number_of_edges(h1);
n2 = nx.number_of_nodes(h2); e2 = nx.number_of_edges(h2);
n3 = nx.number_of_nodes(h3); e3 = nx.number_of_edges(h3);
n4 = nx.number_of_nodes(h4); e4 = nx.number_of_edges(h4);


je1 = np.ones([1,e1]); jn1 = np.ones([1,n1]); h1 = np.zeros([1,n1]);
je2 = np.ones([1,e2]); jn2 = np.ones([1,n2]); h2 = np.zeros([1,n2]);
je3 = np.ones([1,e3]); jn3 = np.ones([1,n3]); h3 = np.zeros([1,n3]);
je4 = np.ones([1,e4]); jn4 = np.ones([1,n4]); h4 = np.zeros([1,n4]);

alpha1 = 1; alpha2 = 12; alpha3 = 108; alpha4 = 324; alpha = 336; # these are individual alphas and total alpha of W_5^3

MPr= []; flag = 0;

for l in range(alpha3+1):
    m = gp.Model("Maximal_profiles")

# adding variables x,y
    x1 = m.addMVar((1,n1), vtype=GRB.BINARY, name="x1")
    x2 = m.addMVar((1,n2), vtype=GRB.BINARY, name="x2")
    x3 = m.addMVar((1,n3), vtype=GRB.BINARY, name="x3")
    x4 = m.addMVar((1,n4), vtype=GRB.BINARY, name="x4")

# Maximize LP for independence number
    m.setObjective(x4.sum(),GRB.MAXIMIZE)
# Constraints for the LP

    m.addConstr(x1 @ B1 <= je1)
    m.addConstr(x1 >=h1)
    m.addConstr(x1.sum() == 1)
    m.addConstr(x2 @ B2 <= je2) 
    m.addConstr(x2 >=h2)
    m.addConstr(x2.sum() == 0)
    m.addConstr(x3 @ B3 <= je3) 
    m.addConstr(x3 >=h3)
    m.addConstr(x3.sum() == l)
    m.addConstr(x4 @ B4 <= je4) 
    m.addConstr(x4 >=h4)
    x = gp.hstack((x1, x2, x3, x4))
    m.addConstr(x @ B <= je);
    
    # Since we have each individual alphas we can also add the following constraint
    m.addConstr(x1.sum() + x2.sum() + x3.sum() + x4.sum() <= alpha)
    m.addConstr(x4.sum() <= alpha4)
            
    m.Params.OutputFlag = 0;
    m.optimize()
    
    if m.status == GRB.OPTIMAL:
        MPr.append((1,0,l,math.floor(m.ObjVal)))
    else:
        print(f"Skipped (i,j,l)=({1},{0},{l}) — model status: {m.status}")
        continue 
    flag = flag +1; print(flag);
    

print(MPr);

for i in range(alpha1): # to find profiles
    for j in range(alpha2+1):
        for l in range(alpha3+1):

            m = gp.Model("Maximal_profiles")

# adding variables x,y
            x1 = m.addMVar((1,n1), vtype=GRB.BINARY, name="x1")
            x2 = m.addMVar((1,n2), vtype=GRB.BINARY, name="x2")
            x3 = m.addMVar((1,n3), vtype=GRB.BINARY, name="x3")
            x4 = m.addMVar((1,n4), vtype=GRB.BINARY, name="x4")

# Maximize LP for independence number
            m.setObjective(x4.sum(),GRB.MAXIMIZE)
# Constraints for the LP

            m.addConstr(x1 @ B1 <= je1)
            m.addConstr(x1 >=h1)
            m.addConstr(x1.sum() == i)
            m.addConstr(x2 @ B2 <= je2) 
            m.addConstr(x2 >=h2)
            m.addConstr(x2.sum() == j)
            m.addConstr(x3 @ B3 <= je3) 
            m.addConstr(x3 >=h3)
            m.addConstr(x3.sum() == l)
            m.addConstr(x4 @ B4 <= je4) 
            m.addConstr(x4 >=h4)
            x = gp.hstack((x1, x2, x3, x4))
            m.addConstr(x @ B <= je);
            
            m.addConstr(x1.sum() + x2.sum() + x3.sum() + x4.sum() <= alpha)
            m.addConstr(x4.sum() <= alpha4)
            
            m.Params.OutputFlag = 0
            m.optimize()

            if m.status == GRB.OPTIMAL:
                MPr.append((i, j, l, math.floor(m.ObjVal)))
            else:
                print(f"Skipped (i,j,l)=({i},{j},{l}) — model status: {m.status}")
                continue 
            flag = flag +1; print(flag);

print(MPr);

m = gp.Model("Maximal_profiles")

# adding variables x,y
z = m.addMVar((1,5), name="z")

# Maximize LP for independence number
m.setObjective(z[0,4],GRB.MINIMIZE)
# Constraints for the LP
for l in range(len(MPr)):
    m.addConstr(z[0,0]*MPr[l][0] + z[0,1]*MPr[l][1] + z[0,2]*MPr[l][2] + z[0,3]*MPr[l][3] <=   z[0,4]) 

m.addConstr(z[0,0] + 3*(k-1)*z[0,1] + 3*(k-1)*(k-1)*z[0,2] + (k-1)*(k-1)*(k-1)*z[0,3] == 1)
m.addConstr(z[0,0] >= 0); m.addConstr(z[0,1] >= 0); m.addConstr(z[0,2] >= 0); m.addConstr(z[0,3] >= 0) ; m.addConstr(z[0,4] >= 0)

m.optimize()
