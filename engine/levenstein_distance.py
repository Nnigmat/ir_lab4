def levenstein_distance(w1, w2):
    # Matrix initialization
    matrix = [[0] * (len(w2)+1) for i in range(len(w1)+1)] 
    
    for i in range(len(w1)+1):
        matrix[i][0] = i
    for i in range(len(w2)+1):
        matrix[0][i] = i
    

    for i in range(1, len(w1)+1):
        for j in range(1, len(w2)+1):
            # Expression 1
            exp1 = 0 if w1[i-1] == w2[j-1] else 1
            exp1 += matrix[i-1][j-1]    
            
            # Expression 2
            exp2 = matrix[i-1][j] + 1 
            
            # Expression 3
            exp3 = matrix[i][j-1] + 1
            matrix[i][j] = min(exp1, exp2, exp3)
    
    return matrix[len(w1)][len(w2)]
