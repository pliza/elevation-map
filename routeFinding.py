import networkx as nx
from collections import deque
import colorsys
import random

# At each intersection, should we try to go as straight as possible?
# Set to False for task 1, then switch to True for task 2.
STRAIGHTER_PATH = True

# =================================
# Workout planning with length, bearing, and elevation
# You will debug and complete our implementation, including the following features:
# 1) find any path in the UBC graph whose total distance is > target using dfs
# 2) above plus: take the "straightest" direction out of any vertex
# 3) above plus: report total elevation gain

# Helper function that determines if edge (v,w) is a valid candidate for adding to the graph
def good(gst, d, v, w, graph, goal_dist):
    # Check if edge from v to w doesn't exist yet in our path
    # Check if the edge exists in the original graph
    # Check if adding this edge keeps us under goal distance
    return ((v, w) not in gst.edges 
            and (v, w, 0) in graph.edges
            and graph.edges[v, w, 0]['length'] > 0)

# Helper function that returns the absolute difference between any 2 given directions.
# Note that the value should never be more than 180, since a left turn of x is
# equivalent to a right turn of (360 - x).
def get_bearing_diff(b1, b2):
    bdiff = abs(b1-b2) % 360  # allows for neg and large bearings
    # Make sure the difference is at most 180 degrees
    if bdiff > 180:
        bdiff = 360 - bdiff
    return bdiff

# Main dfs function. Given a start node, goal distance, and graph of distances,
# solve these 2 related questions:
# Part 1: return a subgraph whose edges are a trail with distance at least goal_distance
# Part 2: return a subgraph with the characteristics from Part 1, but change the definition
# of "neighbors" so that at every node, the direction of the next edge is as close as possible
# to the current direction. This feature changes the order in which the neighbors are considered.
def find_route(start, goal_dist, graph):
    print(f"Starting route search from node {start} with goal distance {goal_dist}")
    
    # distances and feasible edges will come from 'graph', solution built in 'gstate'
    gstate = nx.DiGraph()
    gstate.add_nodes_from([start])  # Add at least the start node
    
    # Make sure the start node exists in the graph
    if start not in graph:
        print(f"Start node {start} not found in graph")
        # Return a minimal graph with just the start node and no edges
        return gstate, 0
    
    # Create a distance accumulator to keep track of the total distance
    total_distance = 0
    
    # Initialize the stack with (current node, current path graph, distance so far, clock)
    stack = deque([(start, gstate, total_distance, 0)])
    
    # Keep track of visited nodes to avoid cycles
    visited = set([start])
    
    # Keep track of the best path found so far
    best_path = None
    best_distance = 0
    best_clock = 0
    
    while stack:
        curr, path_graph, dist_so_far, clock = stack.pop()
        
        if dist_so_far > best_distance:
            best_distance = dist_so_far
            best_path = path_graph.copy()
            best_clock = clock
            print(f"New best path found: {dist_so_far} meters, {clock} edges")
        
        # Check if we've reached the target distance
        if dist_so_far >= goal_dist:
            print(f"Found path with distance {dist_so_far} >= {goal_dist}")
            return path_graph, clock
        
        # Get neighbors to explore
        if STRAIGHTER_PATH and len(list(path_graph.edges())) > 0:
            # Find the previous node that connects to the current node
            prev = None
            for u, v in path_graph.edges():
                if v == curr:
                    prev = u
                    break
            
            if prev is not None and (prev, curr, 0) in graph.edges:
                prev_bearing = graph.edges[prev, curr, 0].get('bearing', 0)
                
                # Sort neighbors by bearing difference to continue in the straightest direction
                neighbors = []
                for nbr in graph.neighbors(curr):
                    if (curr, nbr, 0) in graph.edges:
                        bearing = graph.edges[curr, nbr, 0].get('bearing', 0)
                        diff = get_bearing_diff(prev_bearing, bearing)
                        neighbors.append((nbr, diff))
                
                # Sort by bearing difference (smaller = straighter)
                neighbors.sort(key=lambda x: x[1])
                neighbors = [n[0] for n in neighbors]
            else:
                neighbors = list(graph.neighbors(curr))
        else:
            # For part 1, just get all neighbors
            neighbors = list(graph.neighbors(curr))
        
        # Explore each neighbor
        for neighbor in reversed(neighbors):
            # Skip if this neighbor creates a cycle
            if neighbor in visited:
                continue
                
            # Check if this edge exists in the original graph
            if (curr, neighbor, 0) not in graph.edges:
                continue
                
            # Get the edge length
            edge_length = graph.edges[curr, neighbor, 0].get('length', 0)
            
            # Skip edges with no length
            if edge_length <= 0:
                continue
            
            # Create a new graph for this path
            new_path = path_graph.copy()
            new_path.add_edge(curr, neighbor, time=clock)
            
            # Add to stack with updated distance and clock
            visited.add(neighbor)
            stack.append((neighbor, new_path, dist_so_far + edge_length, clock + 1))
            
    
    # If we couldn't find a path that meets the goal, return the best one we found
    print(f"Could not find path >= {goal_dist}. Best distance: {best_distance}")
    
    # If we didn't find any path at all, create a minimal graph with just the start node
    if best_path is None:
        best_path = gstate
        
    return best_path, best_clock

# returns the total elevation gain in gr, over the route described by rt (list of vertices).
# edges whose elevation gain is negative should be ignored.
# you can refer to a node's elevation by: gr.nodes[rt[k]]['elevation'], where k is the kth element
# of the rt list.
def total_elevation_gain(gr, rt):
    if not rt or len(rt) < 2:
        return 0
        
    total_gain = 0
    
    # Iterate through the route vertices (except the last one)
    for i in range(len(rt) - 1):
        # Make sure both nodes exist in the graph
        if rt[i] not in gr.nodes or rt[i+1] not in gr.nodes:
            continue
            
        # Get elevations
        current_elev = gr.nodes[rt[i]].get('elevation', 0)
        next_elev = gr.nodes[rt[i+1]].get('elevation', 0)
        
        # Calculate elevation difference
        elev_diff = next_elev - current_elev
        
        # Only add positive elevation changes (uphill segments)
        if elev_diff > 0:
            total_gain += elev_diff
            
    return total_gain

# hsv color representation gives a rainbow from red and back to red over values 0 to 1.
# this function returns the color in rgb hex, given the current and total edge numbers
def shade_given_time(k, n):
    # Prevent division by zero
    if n == 0:
        n = 1
    col = colorsys.hsv_to_rgb(k / n, 1.0, 1.0)
    # Fix the tuple conversion - multiply by 255 instead of 256
    tup = tuple(int(x * 255) for x in col)
    st = f"#{tup[0]:02x}{tup[1]:02x}{tup[2]:02x}"
    return st