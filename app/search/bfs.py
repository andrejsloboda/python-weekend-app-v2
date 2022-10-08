from collections import deque, defaultdict
from slugify import slugify
from typing import List, Any
from copy import deepcopy
from sqlalchemy.engine import Row
from app.database.database import Route
from app.search.graph import Graph, BaseGraph


def construct_route(route: List[Route]) -> defaultdict[Any, list]:
    route_out = defaultdict()
    route_out['routes'] = route
    return route_out


def visited_cities(route: List[Route], node: Route) -> bool:
    for n in route:
        if node.destination == n.origin or n.destination == node.destination:
            return True
    return False


def find_routes(graph: Graph, origin: str, destination: str) -> List[dict[str, List[Row]]]:
    graph = graph
    q = deque([node] for node in graph.nodes if node.origin == slugify(origin))

    result = list()
    visited_routes = list()

    while q:
        route = q.pop()
        if route[-1].destination == slugify(destination):
            result.append(construct_route(route))
            visited_routes.append(route)
        else:
            for nbr in graph[route[-1]]:
                if nbr not in route and not visited_cities(route, nbr):
                    new_route = deepcopy(route)
                    new_route.append(nbr)
                    q.append(new_route)
                else:
                    continue
    return result


def find_base_routes(graph: BaseGraph, origin: str, destination: str) -> List[List[Row]]:
    graph = graph
    q = deque([node] for node in graph.nodes if node.origin == slugify(origin))

    result = list()

    while q:
        route = q.pop()
        if route[-1].destination == slugify(destination):
            result.append(route)
        else:
            for nbr in graph[route[-1]]:
                if nbr not in route and not visited_cities(route, nbr):
                    new_route = deepcopy(route)
                    new_route.append(nbr)
                    q.append(new_route)
                else:
                    continue
    return result

