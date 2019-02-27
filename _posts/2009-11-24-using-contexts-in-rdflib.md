Using contexts in rdflib
========================

I am playing with [rdflib](http://rdflib.net), a fantastic python
library to handle RDF data. I had trouble understanding how to use
contexts so to partition my ConjunctiveGraph into independent subgraphs.
Here is the code

```python
import rdflib
from rdflib.Graph import Graph

conj=rdflib.ConjunctiveGraph()

NS=rdflib.Namespace("http://example.com/#")
NS_CTX=rdflib.Namespace("http://example.com/context/#")

alice=NS.alice
bob=NS.bob
charlie=NS.charlie

pizza=NS.pizza
meat=NS.meat
chocolate=NS.chocolate

loves=NS.loves
hates=NS.hates
likes=NS.likes
dislikes=NS.dislikes

love_ctx=Graph(conj.store, NS_CTX.love)
food_ctx=Graph(conj.store, NS_CTX.food)

love_ctx.add( (alice, loves, bob) )
love_ctx.add( (alice, loves, charlie) )
love_ctx.add( (bob, hates, charlie) )
love_ctx.add( (charlie, loves, bob) )

food_ctx.add( (alice, likes, chocolate) )
food_ctx.add( (alice, likes, meat) )
food_ctx.add( (alice, dislikes, pizza) )

print "Full context"
for t in conj:
    print t

print ""
print "Contexts"
for c in conj.contexts():
    print c

print "love context"
for t in love_ctx:
    print t

print "food context"
for t in food_ctx:
    print t
```

Running this script will produce the full graph (printing the triples in
`ConjunctiveGraph`) but also the subgraphs as assigned for each context.
