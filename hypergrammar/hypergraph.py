import xgi
from hypergrammar.edge import Edge


class Hypergraph:
    def __init__(self) -> None:
        self._edges: frozenset[Edge] = frozenset()
        self._node_parameters: dict[str, dict[str, int]] = {}

    def add_edge(self, edge: Edge) -> None:
        self._edges = self._edges.union(frozenset([edge]))

    def remove_edge(self, edge: Edge) -> None:
        self._edges = self._edges.difference(frozenset([edge]))

    def set_vertex_parameter(self, vertex: str, parameter: dict[str, int]) -> None:
        self._node_parameters[vertex] = parameter

    def get_edges(self) -> frozenset[Edge]:
        return self._edges

    def get_vertex_parameters(self, vertex: str) -> dict[str, int]:
        return self._node_parameters.get(vertex, {})

    def draw(self, use_positional_parameters: bool = False) -> None:
        xgi_h = xgi.Hypergraph()

        edges_to_draw: list[frozenset[str]] = []
        pos = {}
        edge_labels = {}
        for edge in self.get_edges():
            edge_labels[len(edges_to_draw)] = str(edge)
            edges_to_draw.append(edge.get_vertices())

            if use_positional_parameters:
                for node in edge.get_vertices():
                    if node not in pos:
                        if "x" in self.get_vertex_parameters(
                            node
                        ) and "y" in self.get_vertex_parameters(node):
                            pos[node] = (
                                self.get_vertex_parameters(node)["x"],
                                self.get_vertex_parameters(node)["y"],
                            )
                        else:
                            raise ValueError(
                                "All vertices must have 'x' and 'y' params for positional drawing."
                            )
        for i, edges_vertices in enumerate(edges_to_draw):
            xgi_h.add_edge(edges_vertices, id=i)

        if use_positional_parameters:
            xgi.draw(xgi_h, pos=pos, hyperedge_labels=edge_labels)
        else:
            xgi.draw(xgi_h, hyperedge_labels=edge_labels)
