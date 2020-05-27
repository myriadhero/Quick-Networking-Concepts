"""
SEE312, Deakin Uni, Kirill Duplyakin
____________

https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Algorithm

1. Mark all nodes unvisited. Create a set of all 
the unvisited nodes called the unvisited set.

2. Assign to every node a tentative distance value: 
set it to zero for our initial node and to infinity for all other nodes. 
Set the initial node as current.

3. For the current node, consider all of its unvisited 
neighbours and calculate their tentative distances through the current node. 
Compare the newly calculated tentative distance to the current assigned 
value and assign the smaller one. For example, if the current 
node A is marked with a distance of 6, and the edge connecting 
it with a neighbour B has length 2, then the distance to B through A will be 6 + 2 = 8. 
If B was previously marked with a distance greater than 8 then change it to 8. 
Otherwise, the current value will be kept.

4. When we are done considering all of the unvisited neighbours of the current node, 
mark the current node as visited and remove it from the unvisited set. 
A visited node will never be checked again.

5. If the destination node has been marked visited 
(when planning a route between two specific nodes) or if the smallest tentative 
distance among the nodes in the unvisited set is infinity 
(when planning a complete traversal; occurs when there is no connection between the 
initial node and remaining unvisited nodes), then stop. The algorithm has finished.

6. Otherwise, select the unvisited node that is marked with the smallest tentative distance,
set it as the new "current node", and go back to step 3.

When planning a route, it is actually not necessary to wait until the destination 
node is "visited" as above: the algorithm can stop once the destination node has 
the smallest tentative distance among all "unvisited" nodes 
(and thus could be selected as the next "current").

____________

to do:
    test for edge cases
    raise exceptions for improper use

"""
from collections import OrderedDict, defaultdict
from math import inf

# graph = {node:(edges_from_node)} where an edge is (target_node, cost)
g = {
        1:((2,2),(3,5),(4,1)),
        2:((1,3),(3,3),(4,2)),
        3:((1,8),(2,6),(4,4),(5,1),(6,5)),
        4:((1,7),(2,2),(3,3),(5,1)),
        5:((3,1),(4,1),(6,2)),
        6:((3,8),(5,4)),
    }

def dijkstra(graph, start, end):
    if not ((start in graph) and (end in graph)): 
        raise ValueError("Start or end node not in graph")
    unvisited = defaultdict(lambda: {"cost": inf, "prev_node": None})
    curr_cost = 0
    unvisited[start]["cost"] = curr_cost
    visited = OrderedDict()
    current = start

    while True:
        visited[current] = {"cost": curr_cost, 
                            "prev_node": unvisited[current]["prev_node"]}
        if (end in visited): break

        for target, cost in graph[current]:
            if target in visited: continue # means we've been there via the shortest path
            
            new_cost = curr_cost + cost
            if new_cost < unvisited[target]["cost"]:
                unvisited[target] = {"cost": new_cost, "prev_node":current}
    
        del unvisited[current]
        # if (len(unvisited) == 1):
        #     pass
        # if (len(unvisited) == 0): 
        #     break
        current, curr_cost = next(iter(sorted(unvisited.items(), 
                            key = lambda x: x[1]["cost"])))
        curr_cost = curr_cost["cost"]
        if (curr_cost == inf): 
            visited[end] = unvisited[end]
            break
    
    path = []
    if visited[end]['prev_node']:
        path = [end]
        while path[-1] != start:
            path.append(visited[path[-1]]['prev_node'])
        
    return (path[::-1] if path else [None], visited)

g1 = {
        1:((2,2),(3,5),(4,1),(11,11)),
        2:((1,3),(3,3),(4,2),(7,6)),
        3:((1,8),(2,6),(4,4),(5,1),(6,5),(12,6)),
        4:((1,7),(2,2),(3,3),(5,1),(14,9)),
        5:((3,1),(4,1),(6,2),(8,8),(10,5)),
        6:((3,8),(5,4),(9,4),(11,3),(12,13)),
        7:((1,1),(3,5),(4,1),(12,9),(13,12)),
        8:((3,1),(4,1),(6,2)),
        9:((1,1),(4,4),(5,1),(6,5)),
        10:((3,1),(3,8),(5,4)),
        11:((1,1),(2,2),(3,5),(10,10)),
        12:((3,1),(13,6)),
        13:((1,1),(14,7)),
        14:((3,1),(3,5),(4,1),(9,5),(11,9)),
    }

path, visited = dijkstra(g1,1,11)

print("Visited during search:\n"+"\n".join([str(s) for s in visited.items()]))
print("Best path:","->".join(list(str(s) for s in path)), 
            f"for total cost of {visited[path[-1]]['cost']}.")
