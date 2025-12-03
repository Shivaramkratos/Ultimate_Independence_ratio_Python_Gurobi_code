Project: Independence Sets and Fractional Chromatic Numbers in Strong Products of Wheel Graphs
Author: Shivaramakrishna Pragada
Python Version: 3.10+
Dependencies: NumPy, SciPy, NetworkX, Matplotlib, Gurobi (with WLS license)

Overview

This repository contains three Python codes used in our computational study of independence numbers and fractional chromatic numbers for graph products involving wheel graphs. In particular, the codes implement:

(1) Mixed-integer optimization models for constructing large independent sets in graphs of the form W5 × K3 and W5^3.
(2) A linear program (based on the Hahn–Hell–Poljak maximal profile method) for computing the fractional chromatic number of W_k^2.

The three code files provided are:

W5_K3_170_58-56-56-1.py
6_2_i.py
Wheel_squared_profiles_chi_f.py

Requirements

You need Python 3.10 or higher and the following packages installed:

numpy
scipy
networkx
matplotlib
gurobipy

Install using:

pip install numpy scipy networkx matplotlib gurobipy

Each script contains:

options = {
"WLSACCESSID": "-",
"WLSSECRET": "-",
"LICENSEID": -,
}

Replace these with your valid Gurobi WLS license credentials.

We organize the repository into branches contain the specific code used for validating our computational claims. The main branch has the code for computation of profiles for fractional chromatic number. The branches Lemma 6.2, Lemma 6.3, and Lemma 6.4 contain specific codes used for validation of claims in the respective lemmas.

File Descriptions and How to Run

(A) Files from Lemma 6.2/6.3 branch

Purpose:
Computes independent sets in W5^3 = W5 × W5 × W5. The code uses 6 binary indicator layers, each corresponding to an independent set in W5^2. Incidence-matrix constraints enforce independence, and additional constraints enforce disjointness across layers. Optional profile fixing can be used to target specific constructions.

Example to run:
python3 6_2_i.py

Expected output:
A Gurobi optimization log followed by an objective value representing the total number of vertices selected across all layers.

(B) Files from Lemma 6.4 branch

Purpose:
Computes a maximum independent set in W5^3 × K3 using an 18-layer MILP formulation. Each layer represents an independent set on W5^2. Additional constraints enforce disjointness between layers and fix the sizes of each layer according to the desired profile. This reproduces the known 170-vertex construction.

Example to run:
python3 W5_K3_170_58-56-56-1.py

Expected output:
A Gurobi optimization log followed by an optimal objective value, typically 170 for the provided constraints.

(C) File: Wheel_squared_profiles_chi_f.py in the main branch

Purpose:
Computes the fractional chromatic number chi_f(W_k^2). The script:

Constructs W_k^2 as the Cartesian product of a wheel with itself.

Splits vertices into A1 = {(i,0),(0,i)} and A2 = all remaining vertices.

For each possible size of A1-intersection, computes the maximum possible independent set size in A2. This produces the list of maximal profiles.

Solves the Hahn–Hell–Poljak LP to compute chi_f(W_k^2).

To run:
python3 Wheel_squared_profiles_chi_f.py

Expected output:
A Gurobi optimization log ending with the value of t, where chi_f = 1/t.

Reproducing All Results

For independence numbers of W5 × K3:
Run W5_K3_170_58-56-56-1.py and similar for the rest

For independence numbers of W5^3:
Run 6_2_i.py and similar for the rest

For fractional chromatic number of W_k^2:
Run Wheel_squared_profiles_chi_f.py 

All scripts require a valid Gurobi WLS license and the Python dependencies listed earlier.

Troubleshooting

If Gurobi fails to start:
• Check WLSACCESSID, WLSSECRET, and LICENSEID
• Ensure Gurobi is properly installed
• Confirm that your internet connection allows license validation

If solver performance is slow:
• Reduce logging with m.Params.OutputFlag = 0
• Experiment with solver parameters such as Threads, Method, or MIPFocus
• Run on a machine with more CPU cores or RAM

Notes

These scripts are intended for readers and reviewers of the accompanying research paper. Each script is self-contained and does not depend on external data files.

Contact

For questions, please contact:
Shivaramakrishna Pragada
Department of Mathematics, Simon Fraser University
Email: shivaramkratos@gmail.com, shivaramakrishna_pragada@sfu.ca
