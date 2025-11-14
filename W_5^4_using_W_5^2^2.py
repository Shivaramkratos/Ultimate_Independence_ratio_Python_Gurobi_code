# This is to code for computing maximum independent set in W_5 box K_3 using 18 variables, ie we specify each Wheel within the larger triangle structure

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
w = nx.wheel_graph(k); g = nx.cartesian_product(w,w);
n = nx.number_of_nodes(g); e = nx.number_of_edges(g);
g = nx.convert_node_labels_to_integers(g, first_label=0, ordering='default', label_attribute=None); 
B = nx.incidence_matrix(g); B = np.abs(B); 
je = np.ones([1,e]); jn = np.ones([1,n]); h = np.zeros([1,n]); 

with gp.Env(params=options) as env:
    m = gp.Model("W5pow4_Ind", env=env)

# adding variable x 
    x = m.addMVar((36,n), vtype=GRB.BINARY, name="x")

# Maximize LP for independence number
    m.setObjective(x.sum(),GRB.MAXIMIZE)
# Constraints for the LP
    for i in range(36):
        m.addConstr(x[i,:] @ B <= je)
        m.addConstr(x[i,:] >=h)

# This constructs W5power4 using W5squares box W5squares
    for i in range(1,6):
        m.addConstr(x[0,:] + x[i,:] <= jn)
        m.addConstr(x[6,:] + x[i+6,:] <= jn)
        m.addConstr(x[12,:] + x[i+12,:] <= jn)
        m.addConstr(x[18,:] + x[i+18,:] <= jn)
        m.addConstr(x[24,:] + x[i+24,:] <= jn)
        m.addConstr(x[30,:] + x[i+30,:] <= jn)
        m.addConstr(x[6+i,:] + x[i + 30,:] <= jn)


    for i in range(1,5):
        m.addConstr(x[i,:] + x[i+1,:] <=jn )
        m.addConstr(x[i+6,:] + x[i+7,:] <= jn)
        m.addConstr(x[i+12,:] + x[i+13,:] <= jn)
        m.addConstr(x[i+18,:] + x[i+19,:] <= jn)
        m.addConstr(x[i+24,:] + x[i+25,:] <= jn)
        m.addConstr(x[i+30,:] + x[i+31,:] <= jn)

    m.addConstr(x[1,:] + x[5,:] <= jn)
    m.addConstr(x[11,:] + x[7,:] <= jn)
    m.addConstr(x[17,:] + x[13,:] <= jn)
    m.addConstr(x[19,:] + x[23,:] <= jn)
    m.addConstr(x[25,:] + x[29,:] <= jn)
    m.addConstr(x[31,:] + x[35,:] <= jn)
    m.addConstr(x[6,:] + x[30,:] <= jn)

    for i in  range(6,30):
        m.addConstr(x[i,:] + x[i+6,:] <= jn)

    for i in range(0,6):
        for j in range(1,6):
            m.addConstr(x[i,:] + x[i + 6*j, :] <=jn) 

# This is for Specific independent set
    m.addConstr(x[0,:].sum() >= 8)
    #m.addConstr(x[1,:].sum() == 11)
    #m.addConstr(x[2,:].sum() == 9)
    #m.addConstr(x[3,:].sum() == 9)
    #m.addConstr(x[4,:].sum() == 11)
    #m.addConstr(x[5,:].sum() == 9)
    m.addConstr(x[0,:].sum() + x[1,:].sum() + x[2,:].sum() +
                x[3,:].sum() + x[4,:].sum() + x[5,:].sum()== 53)

    m.addConstr(x[6,:].sum() == 9)
    m.addConstr(x[7,:].sum() == 11)
    m.addConstr(x[8,:].sum() == 9)
    m.addConstr(x[9,:].sum() == 11)
    m.addConstr(x[10,:].sum() == 9)
    m.addConstr(x[11,:].sum() == 9)
    #m.addConstr(x[6,:].sum() + x[7,:].sum() + x[8,:].sum() +
                #x[9,:].sum() + x[10,:].sum() + x[11,:].sum()== 58)

    m.addConstr(x[12,:].sum() <= 9)
    #m.addConstr(x[13,:].sum() == 11)
    #m.addConstr(x[14,:].sum() == 9)
    #m.addConstr(x[15,:].sum() == 11)
    #m.addConstr(x[16,:].sum() == 9)
    #m.addConstr(x[17,:].sum() == 9)
    m.addConstr(x[12,:].sum() + x[13,:].sum() + x[14,:].sum() +
                x[15,:].sum() + x[16,:].sum() + x[17,:].sum()== 58)

    m.addConstr(x[18,:].sum() <= 9)
    #m.addConstr(x[19,:].sum() == 11)
    #m.addConstr(x[20,:].sum() == 9)
    #m.addConstr(x[21,:].sum() == 11)
    #m.addConstr(x[22,:].sum() == 9)
    #m.addConstr(x[23,:].sum() == 9)
    m.addConstr(x[18,:].sum() + x[19,:].sum() + x[20,:].sum() +
                x[21,:].sum() + x[22,:].sum() + x[23,:].sum()== 58)

    m.addConstr(x[24,:].sum() <= 9)
    #m.addConstr(x[25,:].sum() == 11)
    #m.addConstr(x[26,:].sum() == 9)
    #m.addConstr(x[27,:].sum() == 11)
    #m.addConstr(x[28,:].sum() == 9)
    #m.addConstr(x[29,:].sum() == 9)
    m.addConstr(x[24,:].sum() + x[25,:].sum() + x[26,:].sum() +
                x[27,:].sum() + x[28,:].sum() + x[29,:].sum()== 58)

    m.addConstr(x[30,:].sum() <= 9)
    #m.addConstr(x[31,:].sum() == 11)
    #m.addConstr(x[32,:].sum() == 9)
    #m.addConstr(x[33,:].sum() == 11)
    #m.addConstr(x[34,:].sum() == 9)
    #m.addConstr(x[35,:].sum() == 9)
    m.addConstr(x[30,:].sum() + x[31,:].sum() + x[32,:].sum() +
                x[33,:].sum() + x[34,:].sum() + x[35,:].sum()== 58)



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
