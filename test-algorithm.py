"""
Unit Tests for Edit Distance Algorithm
Author: ALİ ÇAĞAN CEBECİ
Course: Algorithms and Programming II - Semester Capstone Project
"""

import unittest
from algorithm import edit_distance, get_alignment_path, apply_operations


class TestEditDistance(unittest.TestCase):
    """Test cases for the edit distance algorithm."""
    
    def test_identical_strings(self):
        """Test edit distance between identical strings."""
        self.assertEqual(edit_distance("hello", "hello"), 0)
        self.assertEqual(edit_distance("", ""), 0)
        self.assertEqual(edit_distance("a", "a"), 0)
    
    def test_empty_strings(self):
        """Test edit distance with empty strings."""
        self.assertEqual(edit_distance("", "hello"), 5)
        self.assertEqual(edit_distance("hello", ""), 5)
        self.assertEqual(edit_distance("abc", ""), 3)
        self.assertEqual(edit_distance("", "xyz"), 3)
    
    def test_classic_examples(self):
        """Test classic edit distance examples."""
        # kitten -> sitting: substitute k->s, substitute e->i, insert g
        self.assertEqual(edit_distance("kitten", "sitting"), 3)
        
        # saturday -> sunday: delete a, delete t, substitute r->n
        self.assertEqual(edit_distance("saturday", "sunday"), 3)
        
        # intention -> execution: many operations
        self.assertEqual(edit_distance("intention", "execution"), 5)
    
    def test_single_character_strings(self):
        """Test edit distance with single character strings."""
        self.assertEqual(edit_distance("a", "b"), 1)  # substitute
        self.assertEqual(edit_distance("a", ""), 1)   # delete
        self.assertEqual(edit_distance("", "b"), 1)   # insert
    
    def test_substitution_only(self):
        """Test cases requiring only substitutions."""
        self.assertEqual(edit_distance("abc", "def"), 3)
        self.assertEqual(edit_distance("cat", "bat"), 1)
        self.assertEqual(edit_distance("abc", "axc"), 1)
    
    def test_insertion_only(self):
        """Test cases requiring only insertions."""
        self.assertEqual(edit_distance("ac", "abc"), 1)
        self.assertEqual(edit_distance("a", "abc"), 2)
        self.assertEqual(edit_distance("", "abc"), 3)
    
    def test_deletion_only(self):
        """Test cases requiring only deletions."""
        self.assertEqual(edit_distance("abc", "ac"), 1)
        self.assertEqual(edit_distance("abc", "a"), 2)
        self.assertEqual(edit_distance("abc", ""), 3)
    
    def test_complex_transformations(self):
        """Test complex transformation cases."""
        self.assertEqual(edit_distance("algorithm", "altruistic"), 6)
        self.assertEqual(edit_distance("horse", "ros"), 3)
        self.assertEqual(edit_distance("distance", "difference"), 5)
    
    def test_return_steps_functionality(self):
        """Test that return_steps parameter works correctly."""
        # Without steps
        distance = edit_distance("cat", "bat")
        self.assertEqual(distance, 1)
        
        # With steps
        distance, dp_table, steps = edit_distance("cat", "bat", return_steps=True)
        self.assertEqual(distance, 1)
        self.assertIsNotNone(dp_table)
        self.assertIsNotNone(steps)
        self.assertTrue(len(steps) > 0)
        
        # Check DP table dimensions
        self.assertEqual(len(dp_table), 4)  # len("cat") + 1
        self.assertEqual(len(dp_table[0]), 4)  # len("bat") + 1
    
    def test_dp_table_structure(self):
        """Test the structure of the DP table."""
        distance, dp_table, steps = edit_distance("ab", "cd", return_steps=True)
        
        # Check dimensions
        self.assertEqual(len(dp_table), 3)  # 2 + 1
        self.assertEqual(len(dp_table[0]), 3)  # 2 + 1
        
        # Check base cases
        self.assertEqual(dp_table[0][0], 0)
        self.assertEqual(dp_table[0][1], 1)
        self.assertEqual(dp_table[0][2], 2)
        self.assertEqual(dp_table[1][0], 1)
        self.assertEqual(dp_table[2][0], 2)
        
        # Check final result
        self.assertEqual(dp_table[2][2], 2)
    
    def test_alignment_path(self):
        """Test the alignment path generation."""
        distance, dp_table, _ = edit_distance("cat", "bat", return_steps=True)
        operations = get_alignment_path("cat", "bat", dp_table)
        
        self.assertIsNotNone(operations)
        self.assertTrue(len(operations) > 0)
        
        # Should have some operations
        op_types = [op['operation'] for op in operations]
        self.assertIn('replace', op_types)  # c -> b replacement
    
    def test_apply_operations(self):
        """Test applying operations to transform strings."""
        distance, dp_table, _ = edit_distance("cat", "bat", return_steps=True)
        operations = get_alignment_path("cat", "bat", dp_table)
        transformations = apply_operations("cat", operations)
        
        self.assertIsNotNone(transformations)
        self.assertTrue(len(transformations) > 0)
        self.assertEqual(transformations[0], "cat")  # Original string
        self.assertEqual(transformations[-1], "bat")  # Final string
    
    def test_edge_cases(self):
        """Test edge cases and potential error conditions."""
        # Very short strings
        self.assertEqual(edit_distance("", "a"), 1)
        self.assertEqual(edit_distance("a", ""), 1)
        
        # Longer strings (within reasonable limits)
        long_str1 = "a" * 10
        long_str2 = "b" * 10
        self.assertEqual(edit_distance(long_str1, long_str2), 10)
        
        # Mixed case shouldn't matter for our algorithm (case sensitive)
        self.assertEqual(edit_distance("Hello", "hello"), 1)
    
    def test_symmetry(self):
        """Test that edit distance is symmetric."""
        test_pairs = [
            ("hello", "world"),
            ("kitten", "sitting"),
            ("abc", "def"),
            ("test", "")
        ]
        
        for str1, str2 in test_pairs:
            dist1 = edit_distance(str1, str2)
            dist2 = edit_distance(str2, str1)
            self.assertEqual(dist1, dist2, f"Distance not symmetric for '{str1}' and '{str2}'")


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2) 