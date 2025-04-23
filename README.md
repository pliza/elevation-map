# 🗺️ Elevation-Based Route Planner

A Python project that calculates hiking or cycling routes based on elevation data. Originally designed to find paths that are either the most direct or have the least elevation gain — ended up being an exercise in debugging, API issues, and emotional resilience.

## Goal

- Use OpenStreetMap data to generate route graphs
- Incorporate elevation data to calculate elevation gain along paths
- Implement DFS traversal to explore different routing options
- Visualize routes using `folium`, with elevation markers

## Tech Stack

- Python
- OSMnx (OpenStreetMap data)
- folium (interactive map rendering)
- elevation API (aka the pain source)
- networkx

## Challenges

- Buggy API responses that failed silently
- Broken DFS due to stack behavior vs expected route sorting
- Paths not connecting properly on maps
- Elevation markers either not rendering or showing up in the wrong location
- Spent more time debugging than coding

## Wins

- Got route visualization working (after days of crying)
- Custom marker rendering for elevation gain/loss
- Learned way too much about why map data hates me

## What I Learned

- Graph traversal and route planning aren’t just about algorithms — visualization, data accuracy, and clean structure matter  
- Stack vs queue behavior in DFS has real consequences  
- I am capable of debugging things I don’t understand until they somehow work

## Status

Emotionally complete. Technically functional.
