import unittest
import json
import tempfile
import os
from main import CheapestFlightsFinder, load_input_from_json

class TestCheapestFlights(unittest.TestCase):
    
    def test_example_1(self):
        # Example 1 from the problem statement
        n = 4
        flights = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]
        src, dst, k = 0, 3, 1
        
        finder = CheapestFlightsFinder(n, flights)
        result = finder.find_cheapest_price(src, dst, k)
        
        self.assertEqual(result, 700)
    
    def test_example_2(self):
        # Example 2 from the problem statement
        n = 3
        flights = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
        src, dst, k = 0, 2, 1
        
        finder = CheapestFlightsFinder(n, flights)
        result = finder.find_cheapest_price(src, dst, k)
        
        self.assertEqual(result, 200)
    
    def test_example_3(self):
        # Example 3 from the problem statement
        n = 3
        flights = [[0, 1, 100], [1, 2, 100], [0, 2, 500]]
        src, dst, k = 0, 2, 0
        
        finder = CheapestFlightsFinder(n, flights)
        result = finder.find_cheapest_price(src, dst, k)
        
        self.assertEqual(result, 500)
    
    def test_no_path(self):
        # Test when there is no path from src to dst
        n = 3
        flights = [[0, 1, 100], [1, 2, 100]]
        src, dst, k = 0, 2, 0
        
        finder = CheapestFlightsFinder(n, flights)
        result = finder.find_cheapest_price(src, dst, k)
        
        self.assertEqual(result, -1)
    
    def test_circular_path(self):
        # Test with circular paths
        n = 3
        flights = [[0, 1, 100], [1, 0, 100], [0, 2, 500], [1, 2, 100]]
        src, dst, k = 0, 2, 2
        
        finder = CheapestFlightsFinder(n, flights)
        result = finder.find_cheapest_price(src, dst, k)
        
        self.assertEqual(result, 200)
    
    def test_large_graph(self):
        # Test with a larger graph
        n = 5
        flights = [
            [0, 1, 100], [0, 2, 500], [1, 2, 100], 
            [1, 3, 600], [2, 3, 200], [2, 4, 350], 
            [3, 4, 100]
        ]
        src, dst, k = 0, 4, 2
        
        finder = CheapestFlightsFinder(n, flights)
        result = finder.find_cheapest_price(src, dst, k)
        
        # Corrected expected result: 0->1->2->4 = 100+100+350 = 550
        self.assertEqual(result, 550)
    
    def test_max_stops_constraint(self):
        # Test where path exists but exceeds k stops
        n = 4
        flights = [[0, 1, 100], [1, 2, 100], [2, 3, 100]]
        src, dst, k = 0, 3, 1
        
        finder = CheapestFlightsFinder(n, flights)
        result = finder.find_cheapest_price(src, dst, k)
        
        self.assertEqual(result, -1)  # Path exists but requires 2 stops (0->1->2->3)
    
    def test_load_input_from_json(self):
        # Test loading input from JSON file
        test_data = {
            "n": 4,
            "flights": [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]],
            "src": 0,
            "dst": 3,
            "k": 1
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            json.dump(test_data, temp_file)
            temp_file_path = temp_file.name
        
        try:
            n, flights, src, dst, k = load_input_from_json(temp_file_path)
            
            self.assertEqual(n, 4)
            self.assertEqual(flights, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]])
            self.assertEqual(src, 0)
            self.assertEqual(dst, 3)
            self.assertEqual(k, 1)
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)
    
    def test_edge_cases(self):
        # Test minimum and maximum constraints
        
        # Minimum valid case (n=2, src=0, dst=1)
        n = 2
        flights = [[0, 1, 100]]
        src, dst, k = 0, 1, 0
        
        finder = CheapestFlightsFinder(n, flights)
        result = finder.find_cheapest_price(src, dst, k)
        
        self.assertEqual(result, 100)
        
        # Test with maximum price
        n = 2
        flights = [[0, 1, 10000]]  # Maximum price as per constraint
        src, dst, k = 0, 1, 0
        
        finder = CheapestFlightsFinder(n, flights)
        result = finder.find_cheapest_price(src, dst, k)
        
        self.assertEqual(result, 10000)

if __name__ == '__main__':
    unittest.main()