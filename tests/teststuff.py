import spacy
import re

def custom_pipeline(nlp):
    return (fix_html_tags, nlp.tagger)


def insert_spaces_around_tags(html):
    def f(match):
        print(match)
        result = match.group(2)
        if match.group(1) != "":
            result = match.group(1) + " " + result
        if match.group(3) != "":
            result += " " + match.group(3)
        return result
    return re.sub(r'(\S?)(<.*?>)(\S?)', f, html).strip()


def fix_html_tags(doc):
    print(doc.text)
    indexes = [m.span() for m in re.finditer(r'(?<!\\)(<.*?>)', doc.text)]
    for start, end in indexes:
        token = doc.merge(start, end)



nlp = spacy.load('en', create_pipeline=custom_pipeline)

html = insert_spaces_around_tags(r"<p class='something' id='test'> something</br> </p>")
print(html)
doc = nlp(html)

print(doc.is_tagged)
print(doc.is_parsed)

for word in doc:
    print(word.text, word.lemma, word.lemma_, word.tag, word.tag_, word.pos, word.pos_)

