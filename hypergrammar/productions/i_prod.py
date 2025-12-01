from abc import ABC, abstractmethod
from hypergrammar.hypergraph import Hypergraph


class IProd(ABC):
    @abstractmethod
    def apply(self, graph: Hypergraph) -> Hypergraph | None:
        pass
