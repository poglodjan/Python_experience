import numpy as np
import pandas as pd

# inputs
input_seq1 = "TATA"
input_seq2 = "ATAT"
input_gap_penualty = -2
input_max_optimal_alignments = 2
input_sub_matrix = "sub_matrix.csv"
output_file = "output.txt"

def load_substitution_matrix(filepath):
    """_summary_
    reads csv and saves each pair with its substitution rule

    Returns:
        <dictionary>  loaded subsiturion matrix
    """
    df = pd.read_csv(filepath,sep=';', index_col=0)
    substitution_matrix = {(row, col): df.loc[row, col] for row in df.index for col in df.columns} # saving each pair
    return substitution_matrix

def initialize_matrix(seq1, seq2, gap_penalty):
    """_summary_
    firstible fills matrix with zeros
    then fills the first row and the first column using gap_penalty

    Returns: 
        <array [][]> matrix filled with zeros and with filled rows/columns 
    """
    rows, cols = len(seq1) + 1, len(seq2) + 1
    scoring_matrix = np.zeros((rows, cols), dtype=int)
    for i in range(1, rows):
        scoring_matrix[i][0] = scoring_matrix[i-1][0] + gap_penalty
    for j in range(1, cols):
        scoring_matrix[0][j] = scoring_matrix[0][j-1] + gap_penalty
    return scoring_matrix

def fill_matrix(seq1, seq2, scoring_matrix, substitution_matrix, gap_penalty):
    """ _summary_
    uses the algorithm:
        (1) H(i,j) = max(
            H(i-1,j-1) + S(A(i), B(i)) 
            H(i-1,j) + GP
            H(i,j-1) + GP
                )
        returns: <array [][]> scoring matrix 
    """
    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            match = scoring_matrix[i-1][j-1] + substitution_matrix[seq1[i-1], seq2[j-1]] # (1)
            delete = scoring_matrix[i-1][j] + gap_penalty
            insert = scoring_matrix[i][j-1] + gap_penalty
            scoring_matrix[i][j] = max(match, delete, insert)
    return scoring_matrix

def traceback_all_alignments(seq1, seq2, scoring_matrix, substitution_matrix, gap_penalty, n):
    """_summary_
    Finds the best possible global matches 
    by tracing paths from the bottom right corner (scoring_matrix[-1, -1])
      => top left corner (scoring_matrix[0, 0])

    Returns:
        n tuples which each equals (n = max_optimal_alignments)
        to the optimal alignment and score ex. ('-TATA', 'ATAT-', 11) 
    """
    alignments = [] 
    stack = [((len(seq1), len(seq2)), "", "")]  # Stack stores ((i, j), aligned_seq1, aligned_seq2) at current move (from [end,end])
    score = scoring_matrix[len(seq1)][len(seq2)]  # Score is the [end,end] value
    while stack and len(alignments) < n: # if stack empty or n alignmets => finish
        (i, j), aligned_seq1, aligned_seq2 = stack.pop()

        if i == 0 and j == 0: # if we are at the beginning => finish, save alignment and do next one
            alignments.append((aligned_seq1[::-1], aligned_seq2[::-1], score))  # reversing sequens
            continue

        # Checking different movements in the matrix
        if i > 0 and j > 0 and scoring_matrix[i][j] == scoring_matrix[i-1][j-1] + substitution_matrix[seq1[i-1], seq2[j-1]]:
            stack.append(((i-1, j-1), seq1[i-1] + aligned_seq1, seq2[j-1] + aligned_seq2)) # diagonal match (we add diagonal move)

        if i > 0 and scoring_matrix[i][j] == scoring_matrix[i-1][j] + gap_penalty:
            stack.append(((i-1, j), seq1[i-1] + aligned_seq1, '-' + aligned_seq2)) # move up in seq1 (we add the gap '-' in aligned_seq2)

        if j > 0 and scoring_matrix[i][j] == scoring_matrix[i][j-1] + gap_penalty:
            stack.append(((i, j-1), '-' + aligned_seq1, seq2[j-1] + aligned_seq2)) # move left in seq2 (we add the gap '-' in aligned_seq1)

    return alignments

def save_alignments_to_file(alignments, filename):
    with open(filename, 'w') as file:
        for i, (aligned_seq1, aligned_seq2, score) in enumerate(alignments):
            file.write(f"Global alignment no. {i+1}:\n")
            file.write(f"{aligned_seq1}\n{aligned_seq2}\n")
            file.write(f"Score: {score}\n\n")

def needleman_wunsch(seq1, seq2, n, filepath, gap_penalty=-2, output_filename="output.txt"):
    substitution_matrix = load_substitution_matrix(filepath) 
     # initialize and fill scoring matrix
    scoring_matrix = initialize_matrix(seq1, seq2, gap_penalty)
    scoring_matrix = fill_matrix(seq1, seq2, scoring_matrix, substitution_matrix, gap_penalty)
     # do optimal alignments
    alignments = traceback_all_alignments(seq1, seq2, scoring_matrix, substitution_matrix, gap_penalty, n) 
    
    save_alignments_to_file(alignments, output_filename) # Save alignments to file

def initialize_matrix_sw(seq1, seq2):
    rows, cols = len(seq1) + 1, len(seq2) + 1
    scoring_matrix = np.zeros((rows, cols), dtype=int)
    return scoring_matrix

def fill_matrix_sw(seq1, seq2, scoring_matrix, substitution_matrix, gap_penalty):
    """ _summary_
    uses the algorithm:
        (1) H(i,j) = max(0,
            H(i-1,j-1) + S(A(i), B(i)) 
            H(i-1,j) + GP
            H(i,j-1) + GP
                )
    
    and saves the max_score with its position
        returns: <array [][]> scoring matrix, <int> max_score, <tuple (i,j)> max_pos 
    """
    max_score = 0
    max_pos = (0, 0)
    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
             # as in Needleman Wunsch: 
            match = scoring_matrix[i-1][j-1] + substitution_matrix[seq1[i-1], seq2[j-1]]
            delete = scoring_matrix[i-1][j] + gap_penalty
            insert = scoring_matrix[i][j-1] + gap_penalty
             # but reset to zero if all scores are negative (local alignment)
            scoring_matrix[i][j] = max(0, match, delete, insert)

            # Track the maximum score and its position for traceback
            if scoring_matrix[i][j] > max_score:
                max_score = scoring_matrix[i][j]
                max_pos = (i, j)
    return scoring_matrix, max_score, max_pos

def traceback_sw(seq1, seq2, scoring_matrix, max_pos, substitution_matrix, gap_penalty):
    """_summary_
    Starts at the cell with the highest score and continues tracing back until 
    it reaches a cell with zero, constructing the aligned sequences along the way

    Returns: 
        <string> aligned_seq1, <string> aligjed_seq2 
    """
    aligned_seq1 = ""
    aligned_seq2 = ""
    i, j = max_pos
    while i > 0 and j > 0 and scoring_matrix[i][j] > 0:
        score = scoring_matrix[i][j]
        diag_score = scoring_matrix[i-1][j-1]
        up_score = scoring_matrix[i-1][j]
        left_score = scoring_matrix[i][j-1]
        
        if score == diag_score + substitution_matrix[seq1[i-1], seq2[j-1]]: # diagonal move
            aligned_seq1 = seq1[i-1] + aligned_seq1
            aligned_seq2 = seq2[j-1] + aligned_seq2
            i -= 1
            j -= 1
        elif score == up_score + gap_penalty: # up move
            aligned_seq1 = seq1[i-1] + aligned_seq1
            aligned_seq2 = "-" + aligned_seq2
            i -= 1
        elif score == left_score + gap_penalty: #left move
            aligned_seq1 = "-" + aligned_seq1
            aligned_seq2 = seq2[j-1] + aligned_seq2
            j -= 1

    return aligned_seq1, aligned_seq2

def smith_waterman(seq1, seq2, filepath, gap_penalty):
    # initialize the algorithm:
    substitution_matrix = load_substitution_matrix(filepath)
    scoring_matrix = initialize_matrix_sw(seq1, seq2)
    scoring_matrix, max_score, max_pos = fill_matrix_sw(seq1, seq2, scoring_matrix, substitution_matrix, gap_penalty)
    aligned_seq1, aligned_seq2 = traceback_sw(seq1, seq2, scoring_matrix, max_pos, substitution_matrix, gap_penalty)
    
    return aligned_seq1, aligned_seq2, max_score

