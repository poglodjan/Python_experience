import unittest
import numpy as np
from needleman_wunsch import (
    initialize_matrix,
    fill_matrix,
    traceback_all_alignments
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
    
    def test_fill_matrix(self):
        # Tests if the matrix was filled correctly
        scoring_matrix = initialize_matrix(self.seq1, self.seq2, self.gap_penalty)
        scoring_matrix = fill_matrix(self.seq1, self.seq2, scoring_matrix, self.substitution_matrix, self.gap_penalty)
        expected_score = 11  
        self.assertEqual(scoring_matrix[len(self.seq1)][len(self.seq2)], expected_score)
    
    def test_traceback_all_alignments(self):
         # Tests whether test_traceback_all_alignments returns correct alignments
        scoring_matrix = initialize_matrix(self.seq1, self.seq2, self.gap_penalty)
        scoring_matrix = fill_matrix(self.seq1, self.seq2, scoring_matrix, self.substitution_matrix, self.gap_penalty)
        
        alignments = traceback_all_alignments(self.seq1, self.seq2, scoring_matrix, self.substitution_matrix, self.gap_penalty, 2)
        expected_alignments = [
            ('-ATAT', 'TATA-', 11),
            ('ATAT-', '-TATA', 11)
        ]
        for expected in expected_alignments:
            self.assertIn(expected, alignments)