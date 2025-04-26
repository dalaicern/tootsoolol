# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
#


# ____________

#   Graph iin Node- oor bid barilgiig durselj bolno. Harin Edge bol neg barilgaas nuguud hureh
#   zam ym. Harin WeightedEdge iin weight- eer zaig ilerhiilne. 
# _____________

# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """
    dgraph = Digraph()
    
    with open(map_filename, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            # print(line.strip())
            
            parts = line.split()
            if len(parts) == 4:
                src_name, dest_name, total_dist, outdoor_dist = parts
                
                total_dist = int(total_dist)
                outdoor_dist = int(outdoor_dist)

                src_node = Node(src_name)
                dest_node = Node(dest_name)

                if not dgraph.has_node(src_node):
                    dgraph.add_node(src_node)
                if not dgraph.has_node(dest_node):
                    dgraph.add_node(dest_node)
                
                edge = WeightedEdge(src_node, dest_node, total_dist, outdoor_dist)
                dgraph.add_edge(edge)
            
    return dgraph


# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out

# _____________Test_____________
# 8 6 39 0
# 6 8 39 0
# 39 37 32 0
# 37 39 32 0
# 39 13 70 50
# 13 39 70 50
# 31 13 30 25
# 13 31 30 25
# 8 4 47 0
# 4 8 47 0
# 6 2 41 0
# 2 6 41 0
# _____________Result_____________
# 13->31 (30, 25)
# 13->39 (70, 50)
# 2->6 (41, 0)
# 31->13 (30, 25)
# 37->39 (32, 0)
# 39->13 (70, 50)
# 39->37 (32, 0)
# 4->8 (47, 0)
# 6->2 (41, 0)
# 6->8 (39, 0)
# 8->4 (47, 0)
# 8->6 (39, 0)

def test_load_map():
    graph = load_map("test_load_map.txt")
    print(graph)
    
#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
#
#   2 oroin hoorond baih zaig hamgiin baga baihaar holboson zamiig oloh. 
#
#   1. Outdoor distance <= max outdoot distance
#   2. Gadaa yavah zam <= max gadaa yavah zam
#   3. niit yavah zam <= max zam


# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, max_total_dist, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    current_path_nodes, current_total_dist, current_outdoor_dist = path
    
    current_path_nodes = current_path_nodes + [start]
    
    
    if not digraph.has_node(start) or not digraph.has_node(end):
        raise ValueError("start, end oroinii ali neg Graph d baihgui baina.")
    elif start == end:
        if current_total_dist < best_dist:
            return current_path_nodes, current_total_dist
        else:
            return best_path, best_dist
    else:
        for nei in digraph.get_edges_for_node(start):
            neighbor = nei.get_destination()
            nei_total_dist = nei.get_total_distance()
            nei_outdoor_dist = nei.get_outdoor_distance()

            if neighbor in current_path_nodes:
                continue
            
            new_total_dist = current_total_dist + nei_total_dist
            new_outdoor_dist = current_outdoor_dist + nei_outdoor_dist

            if new_outdoor_dist > max_dist_outdoors:
                continue

            if new_total_dist > max_total_dist:
                continue
            
            if new_total_dist >= best_dist:
                continue 
            
            new_path_data = [current_path_nodes, new_total_dist, new_outdoor_dist]

            result_path, result_dist = get_best_path(digraph, neighbor, end, new_path_data,
                                                        max_dist_outdoors, max_total_dist, best_dist, best_path)

            if result_dist < best_dist:
                best_dist = result_dist
                best_path = result_path

            
    return best_path, best_dist


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    start_node = Node(start)
    end_node = Node(end)
    
    if not digraph.has_node(start_node) or not digraph.has_node(end_node):
        raise ValueError("Ug oroinuud graph-d alga")
    
    initial_path_data = [[], 0, 0]
    best_dist = float('inf')
    best_path = None

    final_path, _ = get_best_path(digraph, start_node, end_node, initial_path_data,
                                           max_dist_outdoors, max_total_dist,
                                           best_dist, best_path)

    if final_path is None:
        raise ValueError("Nuhtsul hangah zam oldsongui.")
    else:
        return [edge.name for edge in final_path]

# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps5Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps5Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps5Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    # test_load_map()
    unittest.main()

