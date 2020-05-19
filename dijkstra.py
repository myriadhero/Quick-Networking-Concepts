
    # doToo:
    #     1. populate unvisited at discovery rather than all at start, 
    #         so don't have to take up memory for short paths

"""
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

"""
from collections import OrderedDict

# graph = {node:(edges_from_node)} where an edge is (target_node, cost)
g = {
        1:((2,2),(3,5),(4,1)),
        2:((1,3),(3,3),(4,2)),
        3:((1,8),(2,6),(4,4),(5,1),(6,5)),
        4:((1,7),(2,2),(3,3),(5,1)),
        5:((3,1),(4,1),(6,2)),
        6:((3,8),(5,4)),
        7:((1,1),),
        8:((3,1),),
    }

def dijkstra(graph, start, end):
    unvisited = {node: {"cost": float("inf"), "prev_node": None} for node in g.keys()}
    curr_cost = 0
    unvisited[start]["cost"] = curr_cost
    visited = OrderedDict()
    current = start

    while True:
        visited[current] = {"cost": curr_cost, 
                            "prev_node": unvisited[current]["prev_node"]}
        if end in visited: break

        for target, cost in g[current]:
            if target not in unvisited: continue
            
            new_cost = curr_cost + cost
            if new_cost < unvisited[target]["cost"]:
                unvisited[target] = {"cost": new_cost, "prev_node":current}
    
        del unvisited[current]

        current, curr_cost = next(iter(sorted(unvisited.items(), 
                            key = lambda x: x[1]["cost"])))
        curr_cost = curr_cost["cost"]
        if (curr_cost == float("inf")): 
            visited[end] = unvisited[end]
            break
    
    path = []
    if visited[end]['prev_node']:
        path = [end]
        while True:
            if path[-1] == start: break
            path.append(visited[path[-1]]['prev_node'])
        
    
    return (reversed(path) if path else [None], visited)

path, visited = dijkstra(g,8,1)

print("Visited during search:\n"+"\n".join([str(s) for s in visited.items()]))
print("Best path:","->".join(list(str(s) for s in path)))
