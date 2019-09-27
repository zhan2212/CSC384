'''
This file will contain different constraint propagators to be used within 
bt_search.

---
A propagator is a function with the following header
    propagator(csp, newly_instantiated_variable=None)

csp is a CSP object---the propagator can use this to get access to the variables 
and constraints of the problem. The assigned variables can be accessed via 
methods, the values assigned can also be accessed.

newly_instantiated_variable is an optional argument. SEE ``PROCESSING REQUIRED''
if newly_instantiated_variable is not None:
    then newly_instantiated_variable is the most
    recently assigned variable of the search.
else:
    propagator is called before any assignments are made
    in which case it must decide what processing to do
    prior to any variables being assigned. 

The propagator returns True/False and a list of (Variable, Value) pairs, like so
    (True/False, [(Variable, Value), (Variable, Value) ...]

Propagators will return False if they detect a dead-end. In this case, bt_search 
will backtrack. Propagators will return true if we can continue.

The list of variable value pairs are all of the values that the propagator 
pruned (using the variable's prune_value method). bt_search NEEDS to know this 
in order to correctly restore these values when it undoes a variable assignment.

Propagators SHOULD NOT prune a value that has already been pruned! Nor should 
they prune a value twice.

---

PROCESSING REQUIRED:
When a propagator is called with newly_instantiated_variable = None:

1. For plain backtracking (where we only check fully instantiated constraints)
we do nothing...return true, []

2. For FC (where we only check constraints with one remaining 
variable) we look for unary constraints of the csp (constraints whose scope 
contains only one variable) and we forward_check these constraints.

3. For GAC we initialize the GAC queue with all constaints of the csp.

When a propagator is called with newly_instantiated_variable = a variable V

1. For plain backtracking we check all constraints with V (see csp method
get_cons_with_var) that are fully assigned.

2. For forward checking we forward check all constraints with V that have one 
unassigned variable left

3. For GAC we initialize the GAC queue with all constraints containing V.

'''

def prop_BT(csp, newVar=None):
    '''
    Do plain backtracking propagation. That is, do no propagation at all. Just 
    check fully instantiated constraints.
    '''
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            Vars = c.get_scope()
            for var in Vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    # TODO! IMPLEMENT THIS!
    if not newVar:
        consList = csp.get_all_cons()
    else:
        consList = csp.get_cons_with_var(newVar)
    
    prunedList = []
    for constraint in consList:
        
        if constraint.get_n_unasgn() != 1:
            continue
        vari = constraint.get_unasgn_vars()[0]
        
        for d in vari.cur_domain():          
            if constraint.has_support(vari,d):
                continue
            else:
                vari.prune_value(d)
                prunedList.append((vari,d))
            
            if len(vari.cur_domain()) == 0:
                return ( False , list(set(prunedList)) )
            
    return ( True , list(set(prunedList)) )
         
            

def prop_GAC(csp, newVar=None):
    '''
    Do GAC propagation. If newVar is None we do initial GAC enforce processing 
    all constraints. Otherwise we do GAC enforce with constraints containing 
    newVar on GAC Queue.
    '''

    
    # TODO! IMPLEMENT THIS!
    if not newVar:
        consList = csp.get_all_cons()
    else:
        consList = csp.get_cons_with_var(newVar)
        
    prunedList = []
    GACQueue = []
    
    for constraint in consList:
        GACQueue.append(constraint)
        
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
                        if len(vari.cur_domain()) == 0:
                            GACQueue = []
                            return ( False , prunedList )
                        else:
                            for constraint2 in csp.get_cons_with_var(vari):
                                if constraint2 not in GACQueue:
                                    GACQueue.append(constraint2)
    return ( True , prunedList )



    
    
