import unittest
import numpy as np
from needleman_wunsch import (
    load_substitution_matrix,
    initialize_matrix,
    fill_matrix,
    traceback_all_alignments,
    initialize_matrix_sw,
    fill_matrix_sw, 
    traceback_sw, 
    smith_waterman
)

class TestNeedlemanWunsch(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.seq1 = "TATA"
        cls.seq2 = "ATAT"
        cls.gap_penalty = -2
        cls.substitution_matrix = {
            ('A', 'A'): 5, ('A', 'G'): -4, ('A', 'C'): -4, ('A', 'T'): -1,
            ('G', 'A'): -4, ('G', 'G'): 5, ('G', 'C'): -4, ('G', 'T'): -1,
            ('C', 'A'): -4, ('C', 'G'): -4, ('C', 'C'): 5, ('C', 'T'): -1,
            ('T', 'A'): -1, ('T', 'G'): -1, ('T', 'C'): -1, ('T', 'T'): 5
        }
    # _______ Needleman-Wunsch algorithm
    def test_fill_matrix(self):
        # tests if the matrix was filled correctly
        scoring_matrix = initialize_matrix(self.seq1, self.seq2, self.gap_penalty)
        scoring_matrix = fill_matrix(self.seq1, self.seq2, scoring_matrix, self.substitution_matrix, self.gap_penalty)
        expected_score = 11  
        self.assertEqual(scoring_matrix[len(self.seq1)][len(self.seq2)], expected_score)
    
    def test_traceback_all_alignments(self):
         # tests whether test_traceback_all_alignments returns correct alignments
        scoring_matrix = initialize_matrix(self.seq1, self.seq2, self.gap_penalty)
        scoring_matrix = fill_matrix(self.seq1, self.seq2, scoring_matrix, self.substitution_matrix, self.gap_penalty)
        
        alignments = traceback_all_alignments(self.seq1, self.seq2, scoring_matrix, self.substitution_matrix, self.gap_penalty, 2)
        expected_alignments = [
            ('-ATAT', 'TATA-', 11),
            ('ATAT-', '-TATA', 11)
        ]
        for expected in expected_alignments:
            self.assertIn(expected, alignments)
        
    def test_initialize_matrix(self):
        # test if matrix is initialize correctly
        scoring_matrix = initialize_matrix(self.seq1, self.seq1, self.gap_penalty)
        self.assertEqual(scoring_matrix[0][1], -2)
        self.assertEqual(scoring_matrix[1][0], -2)
        self.assertEqual(scoring_matrix[2][0], -4)
        self.assertEqual(scoring_matrix[0][2], -4)

    def test_fill_matrix(self):
        # test if matrix is filled correct
        scoring_matrix = initialize_matrix(self.seq1, self.seq2, self.gap_penalty)
        scoring_matrix = fill_matrix(self.seq1, self.seq2, scoring_matrix, self.substitution_matrix, self.gap_penalty)
        
        expected_score = 11  
        self.assertEqual(scoring_matrix[len(self.seq1)][len(self.seq2)], expected_score)
    
    def test_load_substitution_matrix(self):
        # tests if matrix is loaded from csv
        filepath = "sub_matrix.csv"
        
        substitution_matrix = load_substitution_matrix(filepath)
        self.assertEqual(substitution_matrix[('A', 'A')], 5)
        self.assertEqual(substitution_matrix[('G', 'G')], 5)
        self.assertEqual(substitution_matrix[('C', 'C')], 5)
        self.assertEqual(substitution_matrix[('T', 'T')], 5)
        self.assertEqual(substitution_matrix[('A', 'G')], -4)
        self.assertEqual(substitution_matrix[('A', 'C')], -4)
        self.assertEqual(substitution_matrix[('C', 'G')], -4)
        self.assertEqual(substitution_matrix[('C', 'A')], -5)
        self.assertEqual(substitution_matrix[('G', 'A')], -5)
        self.assertEqual(substitution_matrix[('T', 'C')], -1)
        self.assertEqual(substitution_matrix[('A', 'T')], -1)
        self.assertEqual(substitution_matrix[('T', 'G')], -1)

    # _______ Smith-Waterman algorithm
    def test_initialize_matrix_sw(self):
        # tests if sw matrix was initialized correctly
        scoring_matrix = initialize_matrix_sw(self.seq1, self.seq2)
        rows, cols = len(self.seq1) + 1, len(self.seq2) + 1
        
        self.assertEqual(scoring_matrix.shape, (rows, cols))
        self.assertTrue(np.all(scoring_matrix == 0))
    
    def test_fill_matrix_sw(self):
        # tests if sw matrix was filled correctly
        scoring_matrix = initialize_matrix_sw(self.seq1, self.seq2)
        scoring_matrix, max_score, max_pos = fill_matrix_sw(
            self.seq1, self.seq2, scoring_matrix, self.substitution_matrix, self.gap_penalty
        )
        expected_max_score = 15
        expected_max_pos = [(4, 3),(3,4)] # possibility for two positions

        self.assertEqual(max_score, expected_max_score)
        self.assertIn(max_pos, expected_max_pos)
    
    def test_traceback_sw(self):
        # tests traceback alignments
        scoring_matrix = initialize_matrix_sw(self.seq1, self.seq2)
        scoring_matrix, max_score, max_pos = fill_matrix_sw(
            self.seq1, self.seq2, scoring_matrix, self.substitution_matrix, self.gap_penalty
        )
        expected_max_score = 15
        expected_alignment_1 = "TAT"
        expected_alignment_2 = "TAT"

        aligned_seq1, aligned_seq2 = traceback_sw(self.seq1, self.seq2, scoring_matrix, max_pos, self.substitution_matrix, self.gap_penalty)

        self.assertEqual(aligned_seq1, expected_alignment_1)
        self.assertEqual(aligned_seq2, expected_alignment_2)
        self.assertEqual(max_score, expected_max_score)

    def test_smith_waterman(self):
        # tests if smith_waterman algorithm was ran correctly
        aligned_seq1, aligned_seq2, max_score = smith_waterman(self.seq1, self.seq2, "sub_matrix.csv", self.gap_penalty)

        expected_alignment_1 = "TAT"
        expected_alignment_2 = "TAT"
        expected_max_score = 15

        self.assertEqual(aligned_seq1, expected_alignment_1)
        self.assertEqual(aligned_seq2, expected_alignment_2)
        self.assertEqual(max_score, expected_max_score)
