

def hungarian(M_or: list[list[int]]) -> tuple[int, list[list[bool]]]:
    """
    Hungarian algorithm
    takes a matrix of n agents and m tasks with associated costs
    and matches them.
    returns cost, assignment matrix
    """
    M = [[value for value in row] for row in M_or] # creates a copy of M to remove reference
    u = len(M)    # agents
    v = len(M[0]) # tasks
    A = [[0] * v for _ in range(u)] 
    A_row = [0] * u
    A_column = [0] * v
    
    # Step 1: Assign a feasible set of u values (reduce by row)
    for i in range(u):
        row     = M[i]
        min_row = min(row)
        M[i]    = list(map(lambda x: x - min_row, row))
        
    # Step 2: Assign a feasible set of v values (reduce by column)
    for j in range(v):
        column      = [row[j] for row in M]
        min_column  = min(column)
        mod_column  = map(lambda x: x - min_column, column)
        for i in range(u):
            M[i][j] = mod_column[i]      
            
    # Step 3.1: attempt assignments on value 0 cells on rows 
    for i in range(u):
        row = M[i]
        # this task has already been assigned
        if A_row[i] != 0: continue
        
        zeros = row.count(0)
        # skip this row if it contains multiple zeros, it will always contain at least one zero
        if zeros > 1: continue
            
        # we know there is a zero
        pos = row.index(0)
        A[i][pos] = 1
        # assign the value in the fast arrays
        A_row[i] = pos
        A_column[pos] = i
        # we want to mark off all other columns with this assignment
        for j in range(v):
            if M[i][j] == 0 and A[i][j] == 0: 
                A[i][j] = -1

    # Step 3.2: attempt assignments on value 0 cells on columns 
    for j in range(v):
        column = [row[j] for row in M]
        # this task has already been assigned
        if A_column[j] != 0: continue
        
        zeros = column.count(0)
        # skip this row if it contains multiple zeros, it will always contain at least one zero
        if zeros > 1: continue
            
        # we know there is a zero
        pos = column.index(0)
        
        # additional check to see if this row has already been assigned
        if A_row[pos] != 0: continue
         
        A[pos][j] = 1
        # assign the value in the fast arrays
        A_column[j] = pos
        A_row[pos] = j
        # we want to mark off all other rows with this assignment
        for i in range(u):
            if M[i][j] == 0 and A[i][j] == 0: 
                A[i][j] = -1
    
    # Step 3.21: Choose arbitrary solutions for rows with no assignment TODO
    unassigned_rows    = [i for i in range(u) if A_row[i]    == 0]
    
    # Step 3.22: Choose arbitrary solutions for column with no assignment TODO
    unassigned_columns = [j for j in range(v) if A_column[i] == 0]
    
    # Step 3.3: Iterate until assignments are complete TODO
    
    # calculate the cost
    cost = 0
    for i in range(u):
        for j in range(v):
            v = M_or[i][j]
            if v == 1: cost += v
    return cost, A
    