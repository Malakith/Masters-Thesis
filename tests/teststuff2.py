from owlready2 import *
import sys
set_log_level(1)
onto_path.append("/gist")
onto = get_ontology('file://gist/gistMerged.owl')
onto.load()
time.sleep(1)
for c in onto.classes():
    print(c)
    print(c.label)

print(onto.search(iri="*e"))
with onto:
    sync_reasoner()