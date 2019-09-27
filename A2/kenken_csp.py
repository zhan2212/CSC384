'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''
from cspbase import *
import itertools
import functools
import operator

def binary_ne_grid(kenken_grid):
    # TODO! IMPLEMENT THIS!
    size = kenken_grid[0][0]
    Vars = []
    var_array = []
    domain = [x for x in range(1,size+1)]
    
    for i in range(size):
        var_array.append([])
        for j in range(size):
            var = Variable(str(i)+str(j),domain)
            Vars.append(var)
            var_array[i].append(var)
                       
    csp = CSP('binary',Vars)
    
    for var1 in Vars:
        for var2 in Vars:
            if (var1.name[0] == var2.name[0] and var1.name[1] < var2.name[1])\
            or (var1.name[1] == var2.name[1] and var1.name[0] < var2.name[0]):

                constraint = Constraint(str(var1.name)+str(var2.name), [var1,var2])
                sat = []
                for tp in itertools.permutations(domain, 2):
                    sat.append(tp)
                constraint.add_satisfying_tuples(sat)
                csp.add_constraint(constraint)
                
    return csp, var_array

    

def nary_ad_grid(kenken_grid):
    # TODO! IMPLEMENT THIS!
    size = kenken_grid[0][0]
    Vars = []
    var_array = []
    domain = [x for x in range(1,size+1)]
    
    for i in range(size):
        var_array.append([])
        for j in range(size):
            var = Variable(str(i)+str(j),domain)
            Vars.append(var)
            var_array[i].append(var)
                       
    csp = CSP('nary',Vars)
    
    for i in range(size):
        sat = []
        constraint = Constraint("Row"+str(i+1), var_array[i])
        for t in itertools.permutations(list(range(1,size+1))):
            sat.append(t)
        constraint.add_satisfying_tuples(sat)
        csp.add_constraint(constraint)

        sat = []
        conList = [var_array[x][i] for x in range(size)]
        constraint = Constraint("Col"+str(i+1), conList)
        for t in itertools.permutations(list(range(1,size+1))):
            sat.append(t)
        constraint.add_satisfying_tuples(sat)
        csp.add_constraint(constraint)
            
    return csp, var_array

def kenken_csp_model(kenken_grid):
    # TODO! IMPLEMENT THIS!
    size = kenken_grid[0][0]
    Vars = []
    var_array = []
    domain = [x for x in range(1,size+1)]
    
    for i in range(size):
        var_array.append([])
        for j in range(size):
            var = Variable(str(i)+str(j),domain)
            Vars.append(var)
            var_array[i].append(var)
                       
    csp = CSP('binary',Vars)
    
    for i in range(1,len(kenken_grid)):
        if len(kenken_grid[i]) <= 2:
            continue  
        
        varCagList = []
        for varcag in kenken_grid[i][:-2]:
            varCagList.append(var_array[int(str(varcag)[0])-1][int(str(varcag)[1])-1])
        
        if kenken_grid[i][-1] == 0:
            name = 'plus'+str(i)
            constraint = Constraint(name, varCagList)
            sat = []
            for tp in itertools.product(domain,repeat=len(varCagList)):
                if sum(tp) == kenken_grid[i][-2]:
                    sat.append(tp)
            constraint.add_satisfying_tuples(sat)   
            csp.add_constraint(constraint)
            
        if kenken_grid[i][-1] == 1:
            name = 'minus'+str(i)
            constraint = Constraint(name, varCagList)
            sat = []
            for tp in itertools.product(domain,repeat=len(varCagList)):
                for permu in itertools.permutations(tp):
                    if permu[0]-sum(permu[1:]) == kenken_grid[i][-2]:
                        sat.append(tp)
            constraint.add_satisfying_tuples(sat)   
            csp.add_constraint(constraint)
            
        if kenken_grid[i][-1] == 2:
            name = 'divide'+str(i)
            constraint = Constraint(name, varCagList)
            sat = []
            for tp in itertools.product(domain,repeat=len(varCagList)):
                for permu in itertools.permutations(tp):
                    result = functools.reduce(lambda x,y: x*y, permu[1:])
                    if permu[0]/result == kenken_grid[i][-2]:
                        sat.append(tp)
            constraint.add_satisfying_tuples(sat)   
            csp.add_constraint(constraint)
                
        if kenken_grid[i][-1] == 3:
            name = 'multiply'+str(i)
            constraint = Constraint(name, varCagList)
            sat = []
            for tp in itertools.product(domain,repeat=len(varCagList)):
                result = functools.reduce(lambda x,y: x*y, tp)
                if result == kenken_grid[i][-2]:
                    sat.append(tp)
            constraint.add_satisfying_tuples(sat)   
            csp.add_constraint(constraint)

    for i in range(size):
        sat = []
        constraint = Constraint("Row"+str(i+1), var_array[i])
        for t in itertools.permutations(list(range(1,size+1))):
            sat.append(t)
        constraint.add_satisfying_tuples(sat)
        csp.add_constraint(constraint)

        sat = []
        conList = [var_array[x][i] for x in range(size)]
        constraint = Constraint("Col"+str(i+1), conList)
        for t in itertools.permutations(list(range(1,size+1))):
            sat.append(t)
        constraint.add_satisfying_tuples(sat)
        csp.add_constraint(constraint)
           
    return csp, var_array



    
    
    
    
    
    
    
    