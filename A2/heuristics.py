'''
This file will contain different variable ordering heuristics to be used within
bt_search.

1. ord_dh(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the DH heuristic.
2. ord_mrv(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the MRV heuristic.
3. val_lcv(csp, var)
    - Takes in a CSP object (csp), and a Variable object (var)
    - Returns a list of all of var's potential values, ordered from best value 
      choice to worst value choice according to the LCV heuristic.

The heuristics can use the csp argument (CSP object) to get access to the 
variables and constraints of the problem. The assigned variables and values can 
be accessed via methods.
'''

import random
from copy import deepcopy
import propagators

def ord_dh(csp):
    # TODO! IMPLEMENT THIS!
    if len(csp.get_all_unasgn_vars()) == 0:
        return None
    else:
        varList = csp.get_all_unasgn_vars()
        numValue = -1
        maxVar = None
        
        for var in varList:
            conList = csp.get_cons_with_var(var)
            count = 0
            for cons in conList:
                if cons.get_n_unasgn() <= 1:
                    continue
                else:
                    count += 1
            if count > numValue:
                numValue = count
                maxVar =var
        return maxVar
    

def ord_mrv(csp):
    # TODO! IMPLEMENT THIS!
    if len(csp.get_all_unasgn_vars()) == 0:
        return None
    else:
        varList = csp.get_all_unasgn_vars()
        minVar = varList[0]
        numValue = minVar.cur_domain_size()
        
        for var in varList:
            if var.cur_domain_size() < numValue:
                numValue = var.cur_domain_size()
                minVar = var
        csp.get_all_unasgn_vars().remove(minVar)
        return minVar

def val_lcv(csp, var):
    if len(csp.get_all_unasgn_vars()) == 0:
        return None
    else:
        valueList = var.cur_domain()
        variDict = {}
        GACQueue = csp.get_cons_with_var(var)
        
        for value in valueList:
            var.assign(value)
    
            prunedList = []
                
            while len(GACQueue) != 0:
                constraint = GACQueue[0]
                GACQueue = GACQueue[1:]
                
                for vari in constraint.get_scope():
                    if not vari.is_assigned():
                        for d in vari.cur_domain():
                            if constraint.has_support(vari,d):
                                continue
                            else:
                                vari.prune_value(d)
                                prunedList.append((vari,d))
                                for c in csp.get_cons_with_var(vari):
                                    if not c in GACQueue:
                                        GACQueue.append(c)
                    
            variDict[value] = len(prunedList)
            for var2,val in prunedList:
                var2.unprune_value(val)
            var.unassign()
          
        result = sorted(variDict,key=variDict.__getitem__,reverse=True)
        return result

                
        
