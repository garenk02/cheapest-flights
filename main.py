# Required library imports
import json
import sys
from collections import defaultdict
from typing import List, Tuple

class CheapestFlightsFinder:
    def __init__(self, n: int, flights: List[List[int]]):
        """
        Initialize the flight graph.
        
        Args:
            n: Total number of cities in the network
            flights: List of flights where each flight contains [source_city, destination_city, price]
        
        The graph is built using an adjacency list where:
        - Each node represents a city
        - Each edge represents a flight with its weight being the price
        """
        self.n = n
        self.graph = defaultdict(list)
        
        # Build adjacency list
        for from_city, to_city, price in flights:
            self.graph[from_city].append((to_city, price))
    
    def find_cheapest_price(self, src: int, dst: int, k: int) -> int:
        """
        Find cheapest route using modified Bellman-Ford algorithm.

        How it works:
        1. Initialize all distances as infinite (unreachable)
        2. Set distance to source city as 0 (starting point)
        3. Try all possible routes k+1 times (k stops means k+1 edges)
        4. For each iteration:
           - Copy current distances to avoid using new distances in same iteration
           - For each city, update distances to neighbors if cheaper route found
        5. Return final distance to destination or -1 if no route exists

        Args:
            src: Source city
            dst: Destination city
            k: Maximum number of stops allowed
        
        Returns:
            Cheapest price found or -1 if no valid route exists
        """
        # Step 1: Initialize all distances to infinity (very expensive)
        # This is like assuming initially "there is no route to anywhere"
        distances = [float('inf')] * self.n
        
        # Step 2: Set distance to source city = 0
        # Because it costs nothing to reach the source city
        distances[src] = 0
        
        # Step 3: Try all possible routes k+1 times
        # k is the number of allowed stops
        for i in range(k + 1):
            # Make a temporary copy of distances
            # This is important to avoid using new distances in the same iteration
            temp_distances = distances.copy()
            
            # Step 4: For each source city
            for from_city in range(self.n):
                # Skip cities that are not reachable yet
                if distances[from_city] == float('inf'):
                    continue
                
                # Step 5: Check all flights from this city
                for to_city, price in self.graph[from_city]:
                    # Calculate: cost_to_source_city + flight_cost
                    new_price = distances[from_city] + price
                    # Save the new cost if it's cheaper than the existing one
                    temp_distances[to_city] = min(temp_distances[to_city], new_price)
            
            # Update distances with the latest results
            distances = temp_distances
        
        # Return the cost to the destination city
        # If still infinity, it means no route was found
        return distances[dst] if distances[dst] != float('inf') else -1

def load_input_from_json(file_path: str) -> Tuple[int, List[List[int]], int, int, int]:
    """
    Load input data from JSON file.
    
    Expected JSON format:
    {
        "n": total_cities,
        "flights": [[from_city, to_city, price], ...],
        "src": source_city,
        "dst": destination_city,
        "k": max_stops
    }
    
    Error handling:
    - FileNotFoundError if file doesn't exist
    - JSONDecodeError if invalid JSON format
    - Generic exceptions for other errors
    
    Returns:
        Tuple of (n, flights, src, dst, k)
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            n = data.get('n')
            flights = data.get('flights')
            src = data.get('src')
            dst = data.get('dst')
            k = data.get('k')
            
            return n, flights, src, dst, k
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def main():
    """
    Main program function.
    
    How to use:
    1. Run program with: python main.py input.json
    2. Program reads flight data from JSON file
    3. Creates CheapestFlightsFinder instance
    4. Finds and displays cheapest route
    
    Exit codes:
    - 1: Invalid arguments or file reading errors
    """
    if len(sys.argv) != 2:
        print("Usage: python main.py input.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    n, flights, src, dst, k = load_input_from_json(input_file)
    
    finder = CheapestFlightsFinder(n, flights)
    result = finder.find_cheapest_price(src, dst, k)
    
    print(f"The cheapest price from city {src} to city {dst} with at most {k} stops is: {result}")

# Entry point program
if __name__ == "__main__":
    main()