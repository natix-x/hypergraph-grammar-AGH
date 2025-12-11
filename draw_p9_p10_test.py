from hypergrammar.edge import Edge, EdgeType
from hypergrammar.hypergraph import Hypergraph
from hypergrammar.productions.prod_9 import Prod9
from hypergrammar.productions.prod_10 import Prod10
import matplotlib.pyplot as plt

def draw_with_labels(self, filename=None):
    plt.figure(figsize=(6,6))
    ax = plt.gca()
    xgi_h = Hypergraph()
    xgi_h = None

    pos = {}
    for node in {v for e in self.get_edges() for v in e.get_vertices()}:
        params = self.get_vertex_parameters(node)
        pos[node] = (params.get("x", 0), params.get("y", 0))

    for edge in self.get_edges():
        verts = list(edge.get_vertices())
        r_val = edge.get_parameters().get("R", 0)
        label = f"{edge.get_type().name}\nR={r_val}"

        if edge.get_type() == EdgeType.Q:
            color = "blue"
        else:
            color = "red" if r_val == 1 else "gray"

        for i in range(len(verts)):
            for j in range(i+1, len(verts)):
                x = [pos[verts[i]][0], pos[verts[j]][0]]
                y = [pos[verts[i]][1], pos[verts[j]][1]]
                ax.plot(x, y, color=color, linewidth=2)

        x_mean = sum(pos[v][0] for v in verts)/len(verts)
        y_mean = sum(pos[v][1] for v in verts)/len(verts)
        ax.text(x_mean, y_mean, label, ha="center", va="center",
                fontsize=10, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))

    for node, (x, y) in pos.items():
        ax.scatter(x, y, color="black")
        ax.text(x, y+0.05, node, ha="center", va="bottom", fontsize=10)

    ax.axis("off")
    if filename:
        plt.savefig(filename, bbox_inches='tight')
    plt.show()

Hypergraph.draw = draw_with_labels

hg = Hypergraph()
hg.add_edge(Edge(EdgeType.E, frozenset({"A","B"}), {"R":0}))
hg.add_edge(Edge(EdgeType.E, frozenset({"B","C"}), {"R":0}))
hg.add_edge(Edge(EdgeType.E, frozenset({"C","D"}), {"R":0}))
hg.add_edge(Edge(EdgeType.E, frozenset({"D","E"}), {"R":0}))
hg.add_edge(Edge(EdgeType.E, frozenset({"E","F"}), {"R":0}))
hg.add_edge(Edge(EdgeType.E, frozenset({"F","A"}), {"R":0}))

hg.add_edge(Edge(EdgeType.Q, frozenset({"A","B","C","D","E","F"}), {"R":0}))

hg.set_vertex_parameter("A", {"x":0, "y":1})
hg.set_vertex_parameter("B", {"x":1, "y":2})
hg.set_vertex_parameter("C", {"x":2, "y":1})
hg.set_vertex_parameter("D", {"x":2, "y":0})
hg.set_vertex_parameter("E", {"x":1, "y":-1})
hg.set_vertex_parameter("F", {"x":0, "y":0})

print("=== Początkowy graf ===")
hg.draw("initial.png")
print("Graf początkowy zapisany jako initial.png")

print("=== P9 ===")
prod9 = Prod9()
hg_p9 = prod9.apply(hg)
if hg_p9:
    hg_p9.draw("p9.png")
    print("Graf po P9 zapisany jako p9.png")
else:
    print("P9 could not be applied")

print("=== P10 ===")
prod10 = Prod10()
hg_p10 = prod10.apply(hg)
if hg_p10:
    hg_p10.draw("p10.png")
    print("Graf po P10 zapisany jako p10.png")
else:
    print("P10 could not be applied")
