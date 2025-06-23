"""
Edit Distance (Levenshtein Distance) Algorithm Implementation
Author: ALİ ÇAĞAN CEBECİ
Course: Algorithms and Programming II - Semester Capstone Project
"""

def edit_distance(str1, str2, return_steps=False):
    """
    Calculate the Edit Distance (Levenshtein Distance) between two strings.
    
    Args:
        str1 (str): First string
        str2 (str): Second string
        return_steps (bool): If True, returns steps for visualization
    
    Returns:
        int: Edit distance if return_steps=False
        tuple: (edit_distance, dp_table, steps) if return_steps=True
    
    Time Complexity: O(m*n) where m and n are lengths of strings
    Space Complexity: O(m*n) for the DP table
    """
    m, n = len(str1), len(str2)
    
    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Track steps for visualization
    steps = [] if return_steps else None
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    if return_steps:
        steps.append({
            'step': 'initialization',
            'description': 'Initialize DP table with base cases',
            'dp_table': [row[:] for row in dp],
            'i': -1, 'j': -1
        })
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                # Characters match, no operation needed
                dp[i][j] = dp[i-1][j-1]
                operation = "match"
            else:
                # Characters don't match, find minimum of three operations
                insert = dp[i][j-1] + 1      # Insert
                delete = dp[i-1][j] + 1      # Delete
                replace = dp[i-1][j-1] + 1   # Replace
                
                dp[i][j] = min(insert, delete, replace)
                
                # Determine which operation was used
                if dp[i][j] == replace:
                    operation = "replace"
                elif dp[i][j] == insert:
                    operation = "insert"
                else:
                    operation = "delete"
            
            if return_steps:
                steps.append({
                    'step': f'({i},{j})',
                    'description': f'Processing str1[{i-1}]="{str1[i-1]}" vs str2[{j-1}]="{str2[j-1]}" -> {operation}',
                    'dp_table': [row[:] for row in dp],
                    'i': i, 'j': j,
                    'operation': operation,
                    'char1': str1[i-1] if i <= len(str1) else '',
                    'char2': str2[j-1] if j <= len(str2) else ''
                })
    
    if return_steps:
        return dp[m][n], dp, steps
    return dp[m][n]


def get_alignment_path(str1, str2, dp_table):
    """
    Backtrack through the DP table to find the alignment path.
    
    Args:
        str1 (str): First string
        str2 (str): Second string
        dp_table (list): Completed DP table
    
    Returns:
        list: List of operations to transform str1 to str2
    """
    m, n = len(str1), len(str2)
    i, j = m, n
    
    operations = []
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and str1[i-1] == str2[j-1]:
            # Characters match
            operations.append({
                'operation': 'match',
                'char1': str1[i-1],
                'char2': str2[j-1],
                'position': (i-1, j-1)
            })
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp_table[i][j] == dp_table[i-1][j-1] + 1:
            # Replace operation
            operations.append({
                'operation': 'replace',
                'char1': str1[i-1],
                'char2': str2[j-1],
                'position': (i-1, j-1)
            })
            i -= 1
            j -= 1
        elif j > 0 and dp_table[i][j] == dp_table[i][j-1] + 1:
            # Insert operation
            operations.append({
                'operation': 'insert',
                'char1': '',
                'char2': str2[j-1],
                'position': (i, j-1)
            })
            j -= 1
        elif i > 0 and dp_table[i][j] == dp_table[i-1][j] + 1:
            # Delete operation
            operations.append({
                'operation': 'delete',
                'char1': str1[i-1],
                'char2': '',
                'position': (i-1, j)
            })
            i -= 1
    
    return operations[::-1]  # Reverse to get forward direction


def apply_operations(str1, operations):
    """
    Apply the sequence of operations to transform str1.
    
    Args:
        str1 (str): Original string
        operations (list): List of operations from get_alignment_path
    
    Returns:
        list: Step-by-step transformation
    """
    result = list(str1)
    transformations = [str1]
    
    offset = 0
    for op in operations:
        if op['operation'] == 'match':
            # No change needed
            continue
        elif op['operation'] == 'replace':
            pos = op['position'][0] + offset
            if pos < len(result):
                result[pos] = op['char2']
        elif op['operation'] == 'insert':
            pos = op['position'][0] + offset
            result.insert(pos, op['char2'])
            offset += 1
        elif op['operation'] == 'delete':
            pos = op['position'][0] + offset
            if pos < len(result):
                result.pop(pos)
                offset -= 1
        
        transformations.append(''.join(result))
    
    return transformations
