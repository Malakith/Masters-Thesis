import spacy
import re
import rdflib

nlp = spacy.load('en')

doc = nlp('Tomorrow is the first of december. At 10pm I have to call my mother.')

for word in doc:
    print(word.text, word.lemma, word.lemma_, word.tag, word.tag_, word.pos, word.pos_)

g = rdflib.Graph()
result = g.parse("schema.rdf")

print(result)

print("graph has %s statements." % len(g))
# prints graph has 8427 statements.
i = 0
blogPost = None
for s in g.subjects():
    print("------------------------")
    print()
    for _, p, o in g.triples((s, None, None)):
        print("%s %s %s" % (s, p, o))
    i += 1
    if i > 30:
        break

thing = rdflib.URIRef('Na5692971c9534c6899cc0fe10a7be025')
print(list(g.predicate_objects(thing)))

print()
print()
print()

query = """ select ?label
            where {
                ?x <http://www.w3.org/2000/01/rdf-schema#label> ?label .
                filter contains(LCASE(?label), "event")
            }
            """

qres = g.query(query)

for row in qres:
    print(row)
