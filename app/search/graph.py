from typing import List
from collections import defaultdict
from datetime import timedelta
from sqlalchemy.engine import Row
from app.database.database import Route


class BaseGraph:
    def __init__(self, raw_data: List[Row]) -> None:
        self.graph = defaultdict(list)
        self._process_data(raw_data)

    def _process_data(self, raw_data: List[Row]) -> None:
        for record in raw_data:
            self._add_node(record)

        for node_a in raw_data:
            for node_b in raw_data:
                if node_a.destination == node_b.origin:
                    self._add_edge(node_a, node_b)

    def _add_edge(self, node_a: Row, node_b: Row) -> None:
        self.graph[node_a].append(node_b)

    def _add_node(self, node: Row) -> None:
        self.graph[node] = list()

    def __getitem__(self, item):
        return iter(self.graph[item])

    @property
    def nodes(self):
        self.graph.keys()

    @nodes.getter
    def nodes(self):
        return iter(self.graph.keys())


class Graph:
    def __init__(self, raw_data: List[Route]) -> None:
        self.graph = defaultdict(list)
        self._process_data(raw_data)

    def _process_data(self, raw_data: List[Route]) -> None:
        for record in raw_data:
            self._add_node(record)

        for node_a in raw_data:
            for node_b in raw_data:
                layover = node_b.departure - node_a.arrival
                if node_a.destination == node_b.origin and \
                        timedelta(hours=1) <= layover <= timedelta(hours=6):
                    self._add_edge(node_a, node_b)

    def _add_edge(self, node_a: Route, node_b: Route) -> None:
        self.graph[node_a].append(node_b)

    def _add_node(self, node: Route) -> None:
        self.graph[node] = list()

    def __getitem__(self, item):
        return iter(self.graph[item])

    @property
    def nodes(self):
        self.graph.keys()

    @nodes.getter
    def nodes(self):
        return iter(self.graph.keys())
