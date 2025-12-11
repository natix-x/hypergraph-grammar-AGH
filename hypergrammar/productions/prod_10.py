import itertools
from hypergrammar.hypergraph import Hypergraph
from hypergrammar.edge import Edge, EdgeType

class Prod10:
    """
    P10: Propagacja oznaczenia refinacji z Q na krawędzie E.
    Wymaga pełnego dopasowania topologicznego (cykl krawędzi E).
    """
    
    def apply(self, graph: Hypergraph) -> Hypergraph | None:
        # 1. Znajdź "kotwicę": Q z R=1
        q_edges = [
            e for e in graph.get_edges()
            if e.get_type() == EdgeType.Q and e.get_parameters().get("R") == 1
        ]

        for q_edge in q_edges:
            vertices = list(q_edge.get_vertices())
            if len(vertices) != 6:
                continue

            # 2. Znajdź właściwą kolejność wierzchołków tworzącą cykl E
            # Sprawdzamy permutacje, aby znaleźć taką, która układa się w krawędzie E
            valid_cycle = None

            for perm in itertools.permutations(vertices):
                if self._check_cycle(graph, perm):
                    valid_cycle = perm
                    break
            
            if valid_cycle is None:
                continue # Nie znaleziono pełnego obwodu E wokół tego Q

            # 3. Zbierz krawędzie z tego cyklu
            boundary_edges = self._get_edges_from_cycle(graph, valid_cycle)

            # 4. Sprawdź czy jakakolwiek zmiana jest potrzebna
            if all(e.get_parameters().get("R") == 1 for e in boundary_edges):
                continue

            # 5. Aplikacja zmian (Ustawienie R=1 dla krawędzi E)
            for edge in boundary_edges:
                if edge.get_parameters().get("R", 0) == 0:
                    new_params = edge.get_parameters().copy()
                    new_params["R"] = 1
                    new_e = Edge(EdgeType.E, edge.get_vertices(), new_params)
                    
                    graph.remove_edge(edge)
                    graph.add_edge(new_e)

            return graph

        return None

    def _e_edges_match(self, graph: Hypergraph, edges_vertices: frozenset[str]) -> bool:
        """Sprawdza czy istnieje krawędź E o zadanych wierzchołkach."""
        for edge in graph.get_edges():
            if edge.get_type() == EdgeType.E and edge.get_vertices() == edges_vertices:
                return True
        return False

    def _check_cycle(self, graph: Hypergraph, cycle: tuple[str, ...]) -> bool:
        """Sprawdza czy podana sekwencja wierzchołków tworzy zamknięty cykl krawędzi E."""
        for i in range(len(cycle)):
            v1 = cycle[i]
            v2 = cycle[(i + 1) % len(cycle)] # % len zapewnia zamknięcie pętli (ostatni z pierwszym)
            if not self._e_edges_match(graph, frozenset([v1, v2])):
                return False
        return True

    def _get_edges_from_cycle(self, graph: Hypergraph, cycle: tuple[str, ...]) -> list[Edge]:
        """Pobiera obiekty krawędzi dla zweryfikowanego cyklu."""
        found_edges = []
        for i in range(len(cycle)):
            v1 = cycle[i]
            v2 = cycle[(i + 1) % len(cycle)]
            target = frozenset([v1, v2])
            
            # Znajdź konkretny obiekt krawędzi w grafie
            for edge in graph.get_edges():
                if edge.get_type() == EdgeType.E and edge.get_vertices() == target:
                    found_edges.append(edge)
                    break
        return found_edges