#%%
import pandas as pd
import numpy as np
import pulp
#%%
#defining problem
problem = pulp.LpProblem('part1', pulp.LpMinimize)


#defining basic parameters
generator_type_count= 3
type_counts= [12, 10, 5]
hours= 24
#%%
#defining variebles
y1= pulp.LpVariable.dicts('y1', (range(type_counts[0]), range(hours)), 0, 1, 'Integer')
y2= pulp.LpVariable.dicts('y2', (range(type_counts[1]), range(hours)), 0, 1, 'Integer')
y3= pulp.LpVariable.dicts('y3', (range(type_counts[2]), range(hours)), 0, 1, 'Integer')

l1= pulp.LpVariable.dicts('l1', (range(type_counts[0]), range(hours)), 0, 1, 'Integer')
l2= pulp.LpVariable.dicts('l2', (range(type_counts[1]), range(hours)), 0, 1, 'Integer')
l3= pulp.LpVariable.dicts('l3', (range(type_counts[2]), range(hours)), 0, 1, 'Integer')

s1= pulp.LpVariable.dicts('s1', (range(type_counts[0]), range(hours)), 0, 1, 'Integer')
s2= pulp.LpVariable.dicts('s2', (range(type_counts[1]), range(hours)), 0, 1, 'Integer')
s3= pulp.LpVariable.dicts('s3', (range(type_counts[2]), range(hours)), 0, 1, 'Integer')

x1= pulp.LpVariable.dicts('x1', (range(type_counts[0]), range(hours)), lowBound = 0, cat='Continuous')
x2= pulp.LpVariable.dicts('x2', (range(type_counts[1]), range(hours)), lowBound = 0, cat='Continuous')
x3= pulp.LpVariable.dicts('x3', (range(type_counts[2]), range(hours)), lowBound = 0, cat='Continuous')


# l(ijk)- s(ijk)= y(ijk)- y(ijk-1)
j= 0
k= 0
for j in range(len(y1)):
    for k in range(hours):
        if k>0:
            problem+= y1[j][k]- y1[j][k-1]== l1[j][k]- s1[j][k]
        
        elif k==0:
            problem+= y1[j][0]- y1[j][23]== l1[j][k]- s1[j][k]
            
for j in range(len(y2)):
    for k in range(hours):
        if k>0:
            problem+= y2[j][k]- y2[j][k-1]== l2[j][k]- s2[j][k]
        
        elif k==0:
            problem+= y2[j][0]- y2[j][23]== l2[j][k]- s2[j][k]

for j in range(len(y3)):
    for k in range(hours):
        if k>0:
            problem+= y3[j][k]- y3[j][k-1]== l3[j][k]- s3[j][k]
        
        elif k==0:
            problem+= y3[j][0]- y3[j][23]== l3[j][k]- s3[j][k]


#%%
#Defining goal function
#Production Costs
C11= pulp.lpSum([1000* y1[j][k]+ 2*  (x1[j][k]- 850*  y1[j][k]) for j in range(type_counts[0]) for k in range(hours)])
C12= pulp.lpSum([2600* y2[j][k]+ 1.3*(x2[j][k]- 1250* y2[j][k]) for j in range(type_counts[1]) for k in range(hours)])
C13= pulp.lpSum([3000* y3[j][k]+ 3*  (x3[j][k]- 1500* y3[j][k]) for j in range(type_counts[2]) for k in range(hours)])
C1= C11+ C12+ C13
del C11, C12, C13

#lunching cost
C21= pulp.lpSum([2000* l1[j][k] for j in range(type_counts[0]) for k in range(hours)])
C22= pulp.lpSum([1000* l2[j][k] for j in range(type_counts[1]) for k in range(hours)])
C23= pulp.lpSum([500 * l3[j][k] for j in range(type_counts[2]) for k in range(hours)])
C2= C21+ C22+ C23
del C21, C22, C23

#total cost
TC= C1+ C2
problem+= TC


#%%
#subject to:
#s.t.
#adding constraints
#up and down limit for production
for j in range(len(y1)):
    for k in range(hours):
        problem+= x1[j][k]>= 850* y1[j][k]
        problem+= x1[j][k]<= 2000
        
for j in range(len(y2)):
    for k in range(hours):
        problem+= x2[j][k]>= 1250* y2[j][k]
        problem+= x2[j][k]<= 1750

for j in range(len(y3)):
    for k in range(hours):
        problem+= x3[j][k]>= 1500* y3[j][k]
        problem+= x3[j][k]<= 4000


#demand satisfaction cinstraints
#demand data:
demand= {
     0: 15000,
     1: 15000,
     2: 15000,
     3: 15000,
     4: 15000,
     5: 15000,
     6: 30000,
     7: 30000,
     8: 30000,
     9: 25000,
    10: 25000,
    11: 25000,
    12: 25000,
    13: 25000,
    14: 25000,
    15: 40000,
    16: 40000,
    17: 40000,
    18: 27000,
    19: 27000,
    20: 27000,
    21: 27000,
    22: 27000,
    23: 27000,
    }
for k in demand.keys():
    production= None
    for j in range(type_counts[0]):
        production+=x1[j][k]
    
    for j in range(type_counts[1]):
        production+=x2[j][k]
    
    for j in range(type_counts[2]):
        production+=x3[j][k]
        
    
    problem+= production>=demand[k]


#over-load constraints
for k in demand.keys():
    max_production= None
    for j in range(type_counts[0]):
        max_production+=2000* y1[j][k]
    
    for j in range(type_counts[1]):
        max_production+=1750* y2[j][k]
    
    for j in range(type_counts[2]):
        max_production+=4000* y3[j][k]
        
    
    problem+= max_production>=round(demand[k]*1.15)

#%%
M= 100000

for j in range(len(y1)):
    for k in range(hours):
        problem+= x1[j][k]<= M* y1[j][k]
        
for j in range(len(y2)):
    for k in range(hours):
        problem+= x2[j][k]<= M* y2[j][k]
        
for j in range(len(y3)):
    for k in range(hours):
        problem+= x3[j][k]<= M* y3[j][k]
        

#%%
solver = pulp.getSolver(solver= 'PULP_CBC_CMD', msg=1, timeLimit=30, gapRel=0, gapAbs=0, options= ['--ranges sensit2_mohsen.sen --tmlim 60 --nomip'],keepFiles= True)
problem.solve(solver)
#%%
print("The problem status is:", pulp.LpStatus[problem.status] )
print("The Objective value is", pulp.value(problem.objective))

#
solver = pulp.GLPK_CMD(path = r'C:\Users\LENOVO\Downloads\Compressed\glpk-4.65\w64\glpsol.exe', msg=1, timeLimit=30, options= ['--ranges sensitivity_analysis_part_A.txt --tmlim 60 --nomip'] ,keepFiles= True)
problem.solve(solver)
#%%
