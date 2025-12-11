from typing import Optional
from hypergrammar.hypergraph import Hypergraph
from hypergrammar.edge import Edge, EdgeType
from hypergrammar.rfc import RFC

class Prod9:
    """
    P9: Oznaczenie elementu (Q) do refinacji.
    """
    def __init__(self, rfc: Optional[RFC] = None):
        self._rfc = rfc

    def apply(self, graph: Hypergraph) -> Hypergraph | None:
        # 1. Znajdź kandydatów: Q z R=0
        candidates = [
            e for e in graph.get_edges()
            if e.get_type() == EdgeType.Q and e.get_parameters().get("R", 0) == 0
        ]

        for edge in candidates:
            # 2. Walidacja topologiczna (heksagon = 6 wierzchołków)
            if len(edge.get_vertices()) != 6:
                continue

            # 3. Walidacja RFC (używając metody pomocniczej)
            if not self._validate_edge(edge, graph):
                continue

            # 4. Aplikacja produkcji (Zmiana R=0 -> R=1)
            new_params = edge.get_parameters().copy()
            new_params["R"] = 1
            new_edge = Edge(EdgeType.Q, edge.get_vertices(), new_params)

            graph.remove_edge(edge)
            graph.add_edge(new_edge)
            return graph

        return None

    def _validate_edge(self, q_edge: Edge, graph: Hypergraph) -> bool:
        """Sprawdza kryteria refinacji (Lokalne -> Globalne -> Domyślne True)."""
        # 1. Sprawdź lokalne RFC wstrzyknięte do produkcji
        if self._rfc is not None:
            return self._rfc.is_valid(q_edge, graph)

        # 2. Sprawdź globalne RFC grafu
        res = graph.edge_rfc_is_valid(q_edge)

        # 3. Jeśli żadne RFC nie jest ustawione, domyślnie zezwól na podział
        if res is None:
            return True

        return res