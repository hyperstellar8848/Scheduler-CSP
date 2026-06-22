import json
import time
import random

# loading data
def load_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

class BacktrackingSolver:
    def __init__(self, data):
        self.data = data
        self.variables = [c['id'] for c in data['classes']]
        self.nodes_visited = 0
        #  Initialize domains for each variable
        self.domains = {v: self._get_initial_domain(v) for v in self.variables}

    def _get_initial_domain(self, v):
        c_type = next(c['type'] for c in self.data['classes'] if c['id'] == v)
        rooms = ["B201", "B202"] if c_type == "practical" else self.data['rooms']
        return [{'day': d, 'time': t, 'room': r} for d in self.data['days'] 
                for t in self.data['time_slots'] for r in rooms]

    def _is_consistent(self, var, val, assignment):
        # Mandatory Constraint (Professor/Room collision)
        for other, assigned_val in assignment.items():
            if assigned_val['day'] == val['day'] and assigned_val['time'] == val['time']:
                if assigned_val['room'] == val['room']: return False
                p1 = next(c['professor'] for c in self.data['classes'] if c['id'] == var)
                p2 = next(c['professor'] for c in self.data['classes'] if c['id'] == other)
                if p1 == p2: return False
        return True

    def solve(self, assignment=None, domains=None):
        if assignment is None: assignment = {}
        if domains is None: domains = self.domains
        
        self.nodes_visited += 1
        if len(assignment) == len(self.variables): return assignment
        
        # MRV (Minimum Remaining Values) - Select variable with smallest domain
        var = min([v for v in self.variables if v not in assignment], key=lambda v: len(domains[v]))
        
        #  LCV (Least Constraining Value) - Sort values by impact on others
        ordered_values = sorted(domains[var], key=lambda val: sum(1 for o in self.variables if o not in assignment and o != var))
        
        for val in ordered_values:
            if self._is_consistent(var, val, assignment):
                assignment[var] = val
                
                #  Forward Checking - Prune domains of future variables
                new_domains = {v: [d for d in domains[v] if self._is_consistent(var, val, {v: d})] for v in domains}
                
                if all(len(new_domains[v]) > 0 for v in self.variables if v not in assignment):
                    result = self.solve(assignment, new_domains)
                    if result: return result
                
                del assignment[var]
        return None

class MinConflictsSolver:
    def __init__(self, data):
        self.data = data
        self.variables = [c['id'] for c in data['classes']]

    def get_conflicts(self, var, val, assignment):
        count = 0
        for other in self.variables:
            if var != other:
                assigned_val = assignment[other]
                if assigned_val['day'] == val['day'] and assigned_val['time'] == val['time']:
                    if assigned_val['room'] == val['room']: count += 1
        return count

    def solve(self, max_steps=1000):
        #  Min-Conflicts - Start with random assignment
        assignment = {v: random.choice([{'day': d, 'time': t, 'room': r} 
                      for d in self.data['days'] for t in self.data['time_slots'] 
                      for r in self.data['rooms']]) for v in self.variables}
        
        for step in range(max_steps):
            #  Pick variable with highest conflicts
            conflicted = [v for v in self.variables if self.get_conflicts(v, assignment[v], assignment) > 0]
            if not conflicted: return assignment, step
            var = random.choice(conflicted)
            
            # Minimize conflicts by changing value
            assignment[var] = min([{'day': d, 'time': t, 'room': r} 
                                  for d in self.data['days'] for t in self.data['time_slots'] 
                                  for r in self.data['rooms']], 
                                  key=lambda val: self.get_conflicts(var, val, assignment))
        return None, max_steps

if __name__ == "__main__":
    data = load_data('data.json')
    
    print("--- Running Backtracking (with MRV, LCV, FC) ---")
    bt = BacktrackingSolver(data)
    bt_res = bt.solve()
    print(f"Nodes Visited: {bt.nodes_visited}")
    
    print("\n--- Running Min-Conflicts ---")
    mc = MinConflictsSolver(data)
    mc_res, steps = mc.solve()
    print(f"Steps Taken: {steps}")