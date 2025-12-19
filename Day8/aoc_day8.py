"""
--- Advent of Code 2025 ---
--- Day 8:  ---
https://adventofcode.com/2025/day/8
"""

from time import perf_counter
from math import sqrt
from pprint import pprint

TEST = False

DAY = "8"
REAL_INPUT = "Advent-of-Code-2025/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2025/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
    CONNECTION_LIMIT = 10
else:
    FILENAME = REAL_INPUT
    CONNECTION_LIMIT = 1000


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    total_nodes = len(data)
    junction_box_locations = process_data(data)
    junction_box_locations.sort()
    total_distance_data = get_distance_data(junction_box_locations)
    distance_data = total_distance_data[:CONNECTION_LIMIT]
    connection_data = [x[0] for x in distance_data]
    adjacency_data = get_adjacency_data(connection_data)
    sorted_sub_graphs = sorted(
        get_sub_graph_members(adjacency_data), key=len, reverse=True
    )
    print(
        f"Junction Box Size Multiplication Part I {multiply_sub_graph_sizes(sorted_sub_graphs[:3])}"
    )
    total_connection_data = [x[0] for x in total_distance_data]
    last_edge = fully_connect_nodes(
        total_connection_data,
        total_nodes,
        find_min_edges_required(total_connection_data, total_nodes),
    )
    print(f"X coord product Part II {x_coord_product(last_edge)}")


def x_coord_product(edge):
    """Return the product of the x coordinates"""
    return edge[0][0] * edge[1][0]


def fully_connect_nodes(total_connection_data, total_nodes, i):
    """Connect nodes until all nodes are connected returning the last edge that completes the connection"""
    adjacency_data = get_adjacency_data(total_connection_data[:i])
    connected = len(dfs(adjacency_data, list(adjacency_data.keys())[0]))
    while connected < total_nodes:
        i += 1
        adjacency_data = get_adjacency_data(total_connection_data[:i])
        connected = len(dfs(adjacency_data, list(adjacency_data.keys())[0]))
    return total_connection_data[i - 1]


def find_min_edges_required(total_connection_data, total_nodes):
    """Return the index value for the first edge in the connection data that might allow the graph to be complete"""
    nodes = set()
    for i, edge in enumerate(total_connection_data):
        nodes.add(edge[0])
        nodes.add(edge[1])
        if len(nodes) == total_nodes:
            return i
    return None


def multiply_sub_graph_sizes(graph_list):
    """Multiply together the sizes of the sub-graphs"""
    product_result = 1
    for graph in graph_list:
        product_result *= len(graph)
    return product_result


def get_sub_graph_members(adjacency_data):
    """for the graph defined by the adjacency data return a list of the members of each sub-graph (closed connected set of nodes where there are no connections between sub-graphs)"""
    sub_graphs = []
    all_nodes = set([x for x in adjacency_data.keys()])
    for node in adjacency_data:
        if node in all_nodes:
            sub_graphs.append(dfs(adjacency_data, node))
            all_nodes.difference_update(sub_graphs[-1])
    return sub_graphs


def dfs(adjacency_data, node, visited=None):
    """Starting at the node return a list of all the nodes that can be reached by following the neighbours of the node"""
    if visited == None:
        visited = set()
    visited.add(node)
    for neighbour in adjacency_data[node]:
        if neighbour not in visited:
            visited.update(dfs(adjacency_data, neighbour, visited))
    return visited


def get_adjacency_data(edge_list):
    """given the list of edges produce a dictionary where the keys are the nodes and the values are the list of nodes adjacent ot eh key node"""
    adjacency_data = {}
    for node in get_all_nodes(edge_list):
        adjacency_data[node] = get_adjacent_nodes(edge_list, node)
    return adjacency_data


def get_adjacent_nodes(edge_list, node):
    """return a list of all the nodes that are adjacent (connected) to the give node"""
    adjacencies = []
    for edge in edge_list:
        node1, node2 = edge
        if node1 == node:
            adjacencies.append(node2)
        elif node2 == node:
            adjacencies.append(node1)
    return adjacencies


def get_all_nodes(edge_list):
    """return a set containing all the nodes from the edge_list"""
    node_set = set()
    for edge in edge_list:
        node_set.update(edge)
    return node_set


def find_all_edges(connection_data, location):
    """return a list containing all the edges that start or end at the given location"""
    edge_list = []
    for pair in connection_data:
        location1, location2 = pair
        if location1 == location or location2 == location:
            edge_list.append(pair)
    return edge_list


def get_distance_data(locations):
    """Given a collection of points, return a dictionary where keys are pairs of different points and the values are the euclidean distance between those points"""
    distance_data = {}
    for i in range(len(locations)):
        for j in range(i, len(locations)):
            if i == j:
                continue
            else:
                distance_data[(locations[i], locations[j])] = euclid_distance(
                    locations[i], locations[j]
                )
    return sorted(distance_data.items(), key=lambda item: item[1])


def euclid_distance(point1, point2):
    """return the euclidean distance between two points"""
    sqr_sum = 0
    for i in range(len(point1)):
        sqr_sum += abs(point1[i] - point2[i]) ** 2
    return sqrt(sqr_sum)


def process_data(data):
    """Process the input data to return a list of tuples. Each tuple is the x, y, z coordinate"""
    locations = []
    for line in data:
        locations.append(tuple([int(x) for x in line.split(",")]))
    return locations


def get_input_data(filename):
    """function to read in the input data"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))
    return file_data


if __name__ == "__main__":
    start_time = perf_counter()
    main()
    print(f"-- Time Taken {perf_counter() - start_time}")
