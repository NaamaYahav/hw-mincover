import pytest
import networkx as nx
from mincover import mincover
from testcases import parse_testcases
import random
import time

testcases = parse_testcases("testcases.txt")

def run_testcase(input:str):
    graph = nx.Graph(input)
    cover = mincover(graph)
    return len(cover)

@pytest.mark.parametrize("testcase", testcases, ids=[testcase["name"] for testcase in testcases])
def test_cases(testcase):
    actual_output = run_testcase(testcase["input"])
    assert actual_output == testcase["output"], f"Expected {testcase['output']}, got {actual_output}"

def is_vertex_cover(graph, cover):
    return all(u in cover or v in cover for u, v in graph.edges)


def brute_force_min_cover_size(graph):
    from itertools import combinations
    nodes = list(graph.nodes())
    for k in range(len(nodes) + 1):
        for subset in combinations(nodes, k):
            if is_vertex_cover(graph, set(subset)):
                return k
    return len(nodes)

def test_new_cases():
    # Basic cases
    g = nx.Graph([(1,2),(2,3)])
    cover = mincover(g)
    assert is_vertex_cover(g, cover)
    assert len(cover) == 1

    g = nx.Graph([(1,2),(2,3),(3,1)])
    cover = mincover(g)
    assert is_vertex_cover(g, cover)
    assert len(cover) == 2

    g = nx.Graph([])
    cover = mincover(g)
    assert len(cover) == 0

    #
    g = nx.cycle_graph(5)
    cover = mincover(g)
    assert is_vertex_cover(g, cover)
    assert len(cover) == 3

    # Random cases
    for _ in range(10):
        n = random.randint(5, 10)
        p = random.random()
        g = nx.gnp_random_graph(n, p)

        cover = mincover(g)
        assert is_vertex_cover(g, cover)

        optimal = brute_force_min_cover_size(g)
        assert len(cover) == optimal
    
    for _ in range(5):
        g = nx.gnp_random_graph(20, 0.3)
        cover = mincover(g)
        assert is_vertex_cover(g, cover)
    

    g = nx.gnm_random_graph(50, 1000)
    start = time.time()
    cover = mincover(g)
    end = time.time()

    assert is_vertex_cover(g, cover)
    assert end - start < 1.0, f"Too slow: {end-start} seconds"

    # Clique
    g = nx.complete_graph(6)
    cover = mincover(g)
    assert len(cover) == 5

    # Star graph
    g = nx.star_graph(5)
    cover = mincover(g)
    assert len(cover) == 1