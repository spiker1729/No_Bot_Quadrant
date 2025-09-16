
import unittest
from main import calculate_sum, calculate_product

class TestMain(unittest.TestCase):
    def test_calculate_sum(self):
        self.assertEqual(calculate_sum(2, 3), 5)
    
    def test_calculate_product(self):
        self.assertEqual(calculate_product(2, 3), 6)

if __name__ == "__main__":
    unittest.main()
