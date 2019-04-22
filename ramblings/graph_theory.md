<script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML' async></script>

# group theory and graph theory

Automorphism: maps a structure to itself. The structure (and the topology) is
preserved.

<p>
$$aut(R^3) -> R^3$$

$$aut(graph) -> graph$$
</p>

identity is always present 

A graph G describes a topology. This topology is then adorned with
descriptors (D), which associate a given value to each topological element of
the graph. Descriptors are classified depending on the type of topological
element they describe, therefore we have vertex descriptors, edge
descriptors, face descriptors and so on.

each topological element has an absolute identifier, which must be unique.
The uniqueness of the identifier must be accurately preserved when writing
on the file: identifiers are stored, and when they are loaded back, they
have to be mapped in some way, otherwise they could overwrite the already
present ids.

we have a graph G. the graph has a multiplicity of vertexes, of links, of
faces and so on. A vertex is identified by a vertex id. A link is identified
by a 2-tuple of vertex ids. FIXME face ?

the graph provides only topology, nothing else. On top of the graph,
descriptors are attached. We have vertex descriptors (that describe
vertexes) link descriptors and so on. The descriptors must have the same
multiplicity of the entities they are describing (therefore, if the vertex
multiplicity is 5, the vertex descriptors must provide 5 values)

to express an n-solid, we need n+1 primitives.
we can define a face between two vertexes, or even with one (monogon).
Special case ?

a face is defined by a path (eg, a collection of contiguous links)


## Descriptors

Color descriptor: returns the color as it thinks it fits (either from a
table, or programmatically)

use the absolute vertex id in links, not the relative of the collection.

all the descriptor have a graph bt not all graphs have descriptors.

vertex images (copies of a vertex into another graph) can be used but they
do not have their own identity. They have the same identifier as the
original one.

## external edges 

Optional approach:
have graphs referring to described elements. for example G1 refers to
vertex1 (which has descriptor 1, 2 and 3 attached) and vertex2 (having only
D2 attached). You can have also vertexcollection (holding 50 vertices)
referring to a descriptor for 50 units. Advantage is that you can create
multiple graphs referring to the same entities which bring their info
together. Graphs can be mutable.

The other approach has immutable graphs, adorned by descriptors.
each vertex is a row in a database. each descriptor is a column.

The multiplicity graph/descriptor could match after the application of a symmetry operation.
for example, if you have only three vertexes but a sym op can generate a
fourth, then you could provide only three information, and let the symmetry
operation handle the generation of the remaining vertex and data associated
to it. This could be done from a table, or programmatically. it is
interesting to note that a symmetry operation acts on the topology level and
on the descriptor level, and these two operations are almost unrelated.

## Symmetry operations in graph theory

A symmetry operation is an operation that acts on a graph and the associated
descriptors. The action of a symmetry operation $$O$$ on the graph purely acts on
the topology. The action of $$O$$ on the descriptors acts on the values of the
descriptors. Obviously, the action of $$O$$ can change the number of elements
(creating new vertexes, for example), so the multiplicity of the descriptors
must match this change appropriately.

A symmetry operation $$O$$ has an order $$k$$. The order is the number of
applications of the symmetry "step" needed to come back to the starting
situation. (FIXME reformulate with group theory names). therefore, a $$C_3$$
rotation has $$k=3$$ because after three rotations of 120 degrees, we go back
to the starting condition.

The topological part of the symmetry operation $$O^{T}$$ acts only on the topology.
<p>
$$O^{T} G = \tilde{G}$$
</p>
$$O^{T}$$ is defined by its axis (the number of vertexes which won't duplicate
under its application) and its order $$k$$. The final number of vertexes in
$$\tilde{G}$$ is $$k*(nvert(G) - nvert(axis)) + nvert(axis)$$.

When symmetry is involved, it is possible to describe edges, faces and so
on, involving vertexes created by the symmetry operation. These edges are
called "external edges". Their specification should reside together with the
operation $$O^{T}$$.

The descriptor values for the generated elements can in principle be
generated from the $$O^{D}$$ part of the operation. this part is descriptor
dependent. each descriptor knows how to act in response to application of
symmetry. what about external edges descriptors ?

external edges must be specified on the operation, not on the generating
graph (which knows nothing about the operation)

the vertexes on the axis keep the same values in the descriptor.
At the level of descriptor, the axis vertexes are determined by the
topological operation. there's a relationship between the operation at the
level of descriptor and at the level of topology.

symmetry operations never remove vertexes. operations in general can, but
this is a more complex thing.



```
graph + descriptor -> operation + 
                      additional relationships + 
                      additional descriptors      -> new (Graph + Descriptor)
```                                                  

The action of an operation on a descriptor depends on the original value,
the referred entity (vertex, link...), the change algorithm and the number
of applications of the basic operation.

for example, if you have three vertexes, 1,2,3 and links 1-2 and 2-3,
describing for example a molecule, you can perform a 3-fold rotation. This
operation is performed by an $$O^{T}$$ having as axis vertex 1 and 2, and
degree 3. vertex 3 will be mapped to (3,(0)), (3,(1)), and (3,(2)), where we
indicate the number of applications of the operation basic step in
parenthesis. The descriptor (for example, xyz coordinate) will change the
coordinate of 3 so to respect the folding. New links will be created between
2 and (3,(n)). Please note that these links are internal links, not
external (FIXME is it true?).

In general, there's no difference between a 6-fold rotation and a 6-times
translation, from the topological point of view.

application of multiple operations, one after another?

avoid selflinking because it's a mess.

graph descriptors describe the graph as a whole, not topological elements.

descriptors: vertex

isotope descriptor (int)
atom charge (int)
color (rgb)
name (string)
cartesian pos (vector)
velocity (vector)


Suppose to have a graph with five vertexes and some descriptors associated
to it. if you delete a vertex, the multiplicity of the descriptors must
change from 5 to 4. the corresponding values must be removed. Also the links
and faces are readapted, and the corresponding descriptors.

Should we use relative ids or absolute ids? ex vertex 118 and vertex 134 are
used in a graph as vertex 1 and 2. A link between them should be described
as (1,2) or (118, 134)? seems better the relative scheme.

alternativa per la descrizione dei link esterni e' una dangling reference,
che punta ad un vertice "virtuale" che sara' creato con l'operazione di
simmetria.

l'ordine dell'operazione puo' essere legato alla topologia, tipico caso, una
rotazione spinorica 3-fold, in 3d l'ordine e' 3, ma in 4d l'ordine e' 6.
Questo vale ogni volta che il descrittore ha una ripetizione diversa dalla
topologia. (FIXME e' possibile cio'?)

```
operation (preserve vertexes, creates new vertexes and other topological elements)
    / \
     |
     | translation
       rotation
       reflection  (work on a geometrical description of the system)
```

se la rotazione fosse sqrt(2), l'ordine e' infinito. 

la traslazione e' invertibile, ci sono operazioni per le quali l'operazione
e' invertibile.

descriptors belonging to the same description should point to the same
graph.

identificativo con (id, numero applicazioni operazione)


## traversing

in a forest, we need to have starting vertexes for each block.

matching a molecule for changes. fingerprinting. smiles.

```
tree-like

world - molecule - atom
                   functional group - atom
                                      atom
                                      bond
                   atom
                   bond
        
        molecule
```

use cases

- add an atom, bond
- remove an atom
- walk the molecule
- merge moolecules
- split a molecule into parts
- select
- match search pattern


## graph datatype representation

- Adjacency matrix representation: graph[i][j] = True iff there's an
edge between vertex $$i$$ and $$j$$. Space complexity $$O(n_{v}^2)$$
- r adjacency list representation: graph[i] = list([j,k,l]). express the
vertexes $$(i,j), (i,k), (i,l)$$. Space complexity $$O(e)$$


## traversal algorithms

depending on the border node selection criterium:

- breadth first search. uses a FIFO. enqueue the root and start the
algorithm. The algorithm dequeues a vertex, enqueues its unmarked children,
visit the vertex and mark it visited. Repeated until the queue is empty.
- depth first search. Uses a list depth number for each vertex. the list
contains -1 if the vertex was not visited, otherwise the level of descent
when visited (root is 0, children of root 1 etc...). The vertex is visited,
then the children if not already visited (depth number == -1), recursively.
- others.

## topological sort

## cycle detection

```
int n; // num of nodes
int dfn[n] // ordinal number for graph visited nodes
int v,w; // represent vertexes
int k=1 // ordinal number for the node to be visited next
boolean inProg[n] // keep track if the search on a given node is in progress

foreach v in V:
    dfn[v] = 0
    inProg[v] = False

foreach v in V:
    if dfn[v] == 0:
        dfs(v)

def dfs(v):
    dfn[v] = k++
    inProg[v] = True
    foreach w in V so that (v,w) is an edge:
        if inProg[w]:
            cycleFound()
        elseif dfn[w] == 0:
            dfs(w)
    inProg[v] = False
```

## detecting connected components

perform a traversal of the tree. all the unvisited nodes after the traversal
belong to a different component. start from one of these nodes. go on until
all the nodes have a component.

## Prim's algorithm

minimum cost spanning tree. returns a set of edges:

```
set of vertices V
set of vertices U
vertex x,y
set of edges T = 0

U={A} // A is a vertex
while U != V
    be (x, y) the lowest cost edge with x in U and y in V-U
    T += (x,y)
    U += y
    
return T
```

Kruskal works by selecting the edges with lower weight, creating subgraphs.
every time an edge connects two subgraphs, they are merged as a single
subraph

```
start with only the vertexes.
set of edges T = 0

while there's more than one set
    be (x, y) the lowest cost edge connecting two different sets
    T += (x,y)
    merge the two sets x and y are belonging to in a single set
return T
```

<p>Prim's algorithm runs in $$O(n^2)$$, while Kruskal's algorithm takes $$n log n$$
time. Thus Prim's algorithm is faster on dense graphs, while Kruskal's is
faster on sparse graphs.</p>

## transitive closure: warshall algorithm

```
graph A expressed as Adjacency matrix 
copy A in C
for k,i,j in A.shape:
    C[i,j] = C[i,j] || (C[i,k] && C[k,j])
```


## shortest path: dijkstra algorithm

be C[v,w] the cost of the edge (v,w). The cost must be non negative, and the
cost of a unexistent edge is +infinite. The dijkstra algorithm finds the
cost of the cheapest path between a starting vertex A and every other vertex in the
graph. (FIXME: the cost, but the path ?)

```
foreach v in V
    D[v] = C[A,v]

S = {A}
for i in xrange(len(V)):
    choose w from V-S such that D[w] is minimum
    add w to S
    foreach w in V-S
        D[v] = min(D[v], D[w] + C[w,v])

S : set of vertices from the graph for which the shortest path has already
been calculated
V-S : set of vertices from the graph for which the shortest path has not
been calculated
D = set of distances 
```

generated graph and generated descriptor are matched by cardinality.

a symmetry operation creates new vertexes and links or preserve vertexes or
links

a graph cannot contain the same vertex twice
a set of context specific algorithms have to be provided for each descriptor
and each alteration concept (ex: color -> preserve or change Hue)

the value of a descriptor after an operation depends on original value,
algorithm and number of applications of the operation.

the behavior of an operation on a graph and the associated descriptors can
depend on some descriptor.

generation is at the graph level
an operation does not introduce additional descriptors.
operations modify topology and descriptor values
all operations have an order
if two descriptors refer to the same graph, the operation preserve this
relationship.
operations do not alter the identifiers, only the values
if the operation is neutral on the topology is neutral to the descriptor.

to produce an operation some descriptor can be involved in the production

alternatives: operations generate a new topology from a base topology or operations introduce new vertexes or edges or preserve the existing ones
alternatives: generation is at the descriptor level or at the graph level

operation provides a descriptor from an existing descriptor.

topology and descriptor are related only on cardinality.

n operatoin does not define additional descriptors.
operations modify topology and desc values.
external links can be defined only on the irreducible graph?
what about a face made of links from 2 operations?

suppose g is a graph and d is a xyz descriptor. $$G^T_d$$ is a generator for
translation operation on the descriptor, $$G^T_t$$ is a generator for
translation on the topology

<p>
$$d_1 = G^T_d(distance = (1.0,0.0,0.0), G^T_t)(d)$$
</p>

the distance parameter is the value generator for the translation operation.

<p>
$$g_1 = G^T_t(links = (indexes of the identifiers), axis = (indexes of the
vertex axis))(g)$$
</p>

<p>
$$d_1^{color} = G^{identity}T_d(distance = (1.0,0.0,0.0), G^T_t)(d^{color})$$
</p>

rotation of two vertexes linked together. one of them forms an axis.
indexes of the vertexes on the axis: $$Z=(1,)$$
external links: $$R=()$$

<p>$$l_{G_g} = G_g(Z,R)$$</p>
<p>$$l_{G_v^{rot}} = G_v^{rot} (order = 3)$$</p>
<p>$$d_{xyz} = G_D(l_{G_v^{rot}}, l_G_g)(d_{xyz})$$</p>

example for R: (1, (1,1)) means a link between 1 and 1 after the application
of the operation one time.

how to refer to the links ? by progressive index?

double linking to go from graph to descriptors?

combined operations. we can combine different operations. suppose for
example to combine a translation and a rotation into a single operation. 
The application of this operation one time is remapped to a given number of
applications of each of the suboperations. 
